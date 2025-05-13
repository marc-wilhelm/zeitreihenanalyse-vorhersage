import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tools.eval_measures import rmse, mse
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, skew, kurtosis
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox
import os
import sys
import time
import warnings
warnings.filterwarnings("ignore")


# Projektkonfiguration laden
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
import results.model_parameters.berlin_params

class SARIMAProgressive:
    """Progressive Forward Validation für SARIMA-Modelle"""

    def __init__(self, ts_data, ts_name, order, seasonal_order):
        self.ts_data = ts_data
        self.ts_name = ts_name
        self.order = order
        self.seasonal_order = seasonal_order
        self.output_dir = f"./ergebnisse/{ts_name}"
        os.makedirs(self.output_dir, exist_ok=True)

    def _fit_and_predict(self, train_data, test_size):
        """Fittet SARIMA-Modell und erstellt Vorhersagen"""
        try:
            model = SARIMAX(
                train_data,
                order=self.order,
                seasonal_order=self.seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            result = model.fit(disp=False, low_memory=True)

            # Vorhersagen erstellen
            pred_train = result.predict(start=0, end=len(train_data) - 1)
            pred_test = result.predict(start=len(train_data), end=len(train_data) + test_size - 1)

            return result, pred_train, pred_test
        except Exception as e:
            print(f"Fehler beim Modell-Fitting: {e}")
            return None, None, None

    def _calculate_metrics(self, actual, predicted):
        """Berechnet RMSE, MSE und MAPE, behandelt NaN-Werte"""
        if len(actual) == 0 or len(predicted) == 0:
            return np.nan, np.nan, np.nan  # Jetzt 3 Werte zurückgeben

        # Remove NaN values
        mask = ~(np.isnan(actual) | np.isnan(predicted))
        if not mask.any():
            return np.nan, np.nan, np.nan

        actual_clean = actual[mask]
        predicted_clean = predicted[mask]

        if len(actual_clean) == 0:
            return np.nan, np.nan, np.nan

        try:
            rmse_val = rmse(actual_clean, predicted_clean)
            mse_val = mse(actual_clean, predicted_clean)

            # MAPE berechnen - nur wenn actual_clean keine Nullen enthält
            if (actual_clean != 0).all():
                mape_val = np.mean(np.abs((actual_clean - predicted_clean) / actual_clean)) * 100
            else:
                mape_val = np.nan

            return rmse_val, mse_val, mape_val
        except:
            return np.nan, np.nan, np.nan

    def _analyze_residuals(self, residuals):
        """Analysiert Residuen und gibt Statistiken zurück"""
        if len(residuals) == 0 or residuals.isna().all():
            return np.nan, np.nan, np.nan, np.nan

        # Remove NaN values
        clean_resid = residuals.dropna()

        if len(clean_resid) < 3:  # Mindestens 3 Werte für Tests
            return np.nan, np.nan, np.nan, np.nan

        try:
            # Ljung-Box Test
            lb_test = acorr_ljungbox(clean_resid, lags=[min(12, len(clean_resid)//3)], return_df=True)
            lb_pvalue = lb_test['lb_pvalue'].iloc[0]

            # Shapiro-Wilk Test (max 5000 Samples)
            if len(clean_resid) > 5000:
                clean_resid_sample = clean_resid.sample(5000, random_state=42)
            else:
                clean_resid_sample = clean_resid

            _, shapiro_pvalue = shapiro(clean_resid_sample)

            # Schiefe und Kurtosis
            resid_skewness = skew(clean_resid)
            resid_kurtosis = kurtosis(clean_resid)

            return lb_pvalue, shapiro_pvalue, resid_skewness, resid_kurtosis
        except:
            return np.nan, np.nan, np.nan, np.nan

    def _plot_residuals(self, residuals, step, data_percentage):
        """Erstellt Residuenplots"""
        if residuals.isna().all():
            return

        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Residuenanalyse - Schritt {step} ({data_percentage}% der Daten)')

        # Zeitplot der Residuen
        axs[0, 0].plot(residuals, color='steelblue')
        axs[0, 0].set_title('Residuen über Zeit')
        axs[0, 0].set_xlabel('Zeit')
        axs[0, 0].set_ylabel('Residuum')
        axs[0, 0].grid(True, alpha=0.3)

        # ACF der Residuen
        if len(residuals.dropna()) > 3:
            plot_acf(residuals.dropna(), ax=axs[0, 1], lags=min(20, len(residuals.dropna())//3))
        axs[0, 1].set_title('ACF der Residuen')
        axs[0, 1].grid(True, alpha=0.3)

        # Histogramm
        clean_resid = residuals.dropna()
        if len(clean_resid) > 0:
            sns.histplot(clean_resid, kde=True, stat="density", bins=20, ax=axs[1, 0])
            xmin, xmax = axs[1, 0].get_xlim()
            x = np.linspace(xmin, xmax, 100)
            p = stats.norm.pdf(x, clean_resid.mean(), clean_resid.std())
            axs[1, 0].plot(x, p, 'r', linewidth=2)
        axs[1, 0].set_title('Histogramm der Residuen')
        axs[1, 0].grid(True, alpha=0.3)

        # Q-Q Plot
        if len(clean_resid) > 0:
            stats.probplot(clean_resid, plot=axs[1, 1])
        axs[1, 1].set_title('Q-Q Plot der Residuen')
        axs[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f"residuen_schritt_{step}_{data_percentage}pct.png"),
                    dpi=300, bbox_inches='tight')
        plt.close()

    def run_progressive_validation(self, data_steps=[0.2, 0.4, 0.6, 0.8, 1.0], test_ratio=0.3):
        """
        Führt progressive Forward Validation durch

        Parameters:
        -----------
        data_steps : list, default=[0.2, 0.4, 0.6, 0.8, 1.0]
            Anteile der Originaldaten, die in jedem Schritt verwendet werden
        test_ratio : float, default=0.3
            Anteil der verfügbaren Daten, der für Tests verwendet wird
        """
        print(f"Starte progressive Forward Validation für '{self.ts_name}'...")
        print(f"Verwende SARIMA{self.order}x{self.seasonal_order}")
        print(f"Zeitreihe: {len(self.ts_data)} Datenpunkte")
        print(f"Schritte: {[f'{int(p*100)}%' for p in data_steps]}")

        results = []

        for step, data_percentage in enumerate(data_steps, 1):
            print(f"\n--- Schritt {step}: {int(data_percentage*100)}% der Daten ---")

            # Berechne Indizes basierend auf dem Prozentsatz der Originaldaten
            data_end = int(len(self.ts_data) * data_percentage)
            current_data = self.ts_data[:data_end]

            # Train-Test-Split innerhalb der verfügbaren Daten
            train_size = int(len(current_data) * (1 - test_ratio))

            # Mindesttrainingsset sicherstellen
            if train_size < 12:  # Mindestens 12 Datenpunkte für SARIMA
                print(f"Zu wenig Trainingsdaten ({train_size}). Überspringe Schritt {step}")
                continue

            train_data = current_data[:train_size]
            test_data = current_data[train_size:]

            print(f"Verfügbare Daten: {len(current_data)} ({int(data_percentage*100)}% von {len(self.ts_data)})")
            print(f"Training: {len(train_data)} ({int((1-test_ratio)*100)}%)")
            print(f"Test: {len(test_data)} ({int(test_ratio*100)}%)")

            # Modell fitten und vorhersagen
            result, pred_train, pred_test = self._fit_and_predict(train_data, len(test_data))

            if result is None:
                print(f"Fehler in Schritt {step}, überspringe...")
                continue

            # Metriken berechnen
            train_rmse, train_mse, train_mape = self._calculate_metrics(train_data, pred_train)
            test_rmse, test_mse, test_mape = self._calculate_metrics(test_data, pred_test)

            # Residuenanalyse
            residuals = result.resid
            lb_pvalue, shapiro_pvalue, resid_skew, resid_kurt = self._analyze_residuals(residuals)

            # Plots erstellen
            self._plot_residuals(residuals, step, int(data_percentage*100))

            # Ergebnisse speichern
            results.append({
                'step': step,
                'data_percentage': data_percentage,
                'available_data': len(current_data),
                'train_size': len(train_data),
                'test_size': len(test_data),
                'train_rmse': train_rmse,
                'test_rmse': test_rmse,
                'train_mse': train_mse,
                'test_mse': test_mse,
                'skewness': resid_skew,
                'kurtosis': resid_kurt
            })

            print(f"Train RMSE: {train_rmse:.4f}, Test RMSE: {test_rmse:.4f}, Test MAPE: {test_mape:.2f}%")

        return pd.DataFrame(results)

    def plot_results(self, results_df):
        """Erstellt Zusammenfassungsplots"""
        if results_df.empty:
            return

        # Erstelle eine Subplot-Figur
        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(16, 18))
        fig.suptitle(f'Progressive Forward Validation Ergebnisse - {self.ts_name}', fontsize=16)

        # 1. RMSE Verlauf
        ax1.plot(results_df['data_percentage']*100, results_df['train_rmse'],
                 marker='o', label='Train RMSE', color='blue', linewidth=2)
        ax1.plot(results_df['data_percentage']*100, results_df['test_rmse'],
                 marker='s', label='Test RMSE', color='red', linewidth=2)
        ax1.set_xlabel('Datenanteil (%)')
        ax1.set_ylabel('RMSE')
        ax1.set_title('RMSE Entwicklung')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. Datengrößen
        ax2.bar(results_df['data_percentage']*100 - 1, results_df['train_size'],
                width=2, label='Training', color='lightblue', alpha=0.7)
        ax2.bar(results_df['data_percentage']*100 + 1, results_df['test_size'],
                width=2, label='Test', color='lightcoral', alpha=0.7)
        ax2.set_xlabel('Datenanteil (%)')
        ax2.set_ylabel('Anzahl Datenpunkte')
        ax2.set_title('Train-/Testset Größen')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 3. Residuentests
        ax3.plot(results_df['data_percentage']*100, results_df['ljung_box_pvalue'],
                 marker='o', label='Ljung-Box p-value', color='green', linewidth=2)
        ax3.axhline(y=0.05, color='red', linestyle='--', alpha=0.7, label='α = 0.05')
        ax3.set_xlabel('Datenanteil (%)')
        ax3.set_ylabel('p-value')
        ax3.set_title('Ljung-Box Test')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(0, max(1, results_df['ljung_box_pvalue'].max() * 1.1))

        # 4. Normalitätstest
        ax4.plot(results_df['data_percentage']*100, results_df['shapiro_pvalue'],
                 marker='s', label='Shapiro-Wilk p-value', color='orange', linewidth=2)
        ax4.axhline(y=0.05, color='red', linestyle='--', alpha=0.7, label='α = 0.05')
        ax4.set_xlabel('Datenanteil (%)')
        ax4.set_ylabel('p-value')
        ax4.set_title('Shapiro-Wilk Test')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim(0, max(1, results_df['shapiro_pvalue'].max() * 1.1))

       

    def plot_validation_structure(self, data_steps=[0.2, 0.4, 0.6, 0.8, 1.0], test_ratio=0.3):
        """Visualisiert die Struktur der progressiven Validierung"""
        fig, ax = plt.subplots(figsize=(14, 8))

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

        for i, data_percentage in enumerate(data_steps):
            # Berechne Indizes
            data_end = int(len(self.ts_data) * data_percentage)
            train_size = int(data_end * (1 - test_ratio))
            test_size = data_end - train_size

            y_pos = len(data_steps) - i - 1

            # Trainingsdaten (blau/grün)
            ax.barh(y_pos, train_size, height=0.8, color=colors[0], alpha=0.7, label='Training' if i == 0 else "")

            # Testdaten (orange)
            ax.barh(y_pos, test_size, left=train_size, height=0.8, color=colors[1], alpha=0.7, label='Test' if i == 0 else "")

            # Nicht verwendete Daten (grau)
            unused = len(self.ts_data) - data_end
            if unused > 0:
                ax.barh(y_pos, unused, left=data_end, height=0.8, color='grey', alpha=0.3, label='Ungenutzt' if i == 0 else "")

            # Beschriftung
            ax.text(-20, y_pos, f'{int(data_percentage*100)}%', ha='right', va='center', fontsize=12, fontweight='bold')

        # Originaldatensatz oben
        ax.barh(len(data_steps), len(self.ts_data), height=0.8, color='orange', alpha=0.9,
                label='Originaldatensatz')
        ax.text(-20, len(data_steps), '100%', ha='right', va='center', fontsize=12, fontweight='bold')

        ax.set_xlabel('Anzahl Datenpunkte', fontsize=12)
        ax.set_ylabel('Validierungsschritt', fontsize=12)
        ax.set_title(f'Progressive Forward Validation Struktur - {self.ts_name}', fontsize=14)
        ax.set_yticks(range(len(data_steps) + 1))
        ax.set_yticklabels(['Schritt 1', 'Schritt 2', 'Schritt 3', 'Schritt 4', 'Schritt 5', 'Original'])
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f"validation_structure.png"),
                    dpi=300, bbox_inches='tight')
        plt.close()

    def save_results(self, results_df):
        """Speichert Ergebnisse als CSV"""
        results_df['model'] = f"SARIMA{self.order}x{self.seasonal_order}"
        results_file = os.path.join(self.output_dir, f"progressive_forward_validation_results.csv")
        results_df.to_csv(results_file, index=False)
        print(f"\nErgebnisse gespeichert in: {results_file}")


def run_sarima_progressive_validation(ts_name, order, seasonal_order):
    """Wrapper-Funktion für die progressive Forward Validation"""

    # Zeitreihe aus Config laden
    # Pfad zur CSV-Datei
    file_path = f"results/{ts_name}_differenced.csv"

    # Einlesen der Datei als DataFrame
    ts_data_df = pd.read_csv(file_path).squeeze()
    ts_data = ts_data_df['Differenzierte Zeitreihe']  # Stelle sicher, dass der Name der Spalte 'temperature' ist
    print(ts_data.head())  # Optional: zeigt die Serie an, um sicherzustellen, dass sie korrekt eingelesen wurde



    # Progressive Validierung durchführen
    validator = SARIMAProgressive(ts_data, ts_name, order, seasonal_order)

    start_time = time.time()
    results_df = validator.run_progressive_validation(
        data_steps=[0.2, 0.4, 0.6, 0.8, 1.0],  # 20%, 40%, 60%, 80%, 100% der Daten
        test_ratio=0.3  # 30% der verfügbaren Daten für Tests
    )

    # Visualisierung und Speicherung
    validator.plot_results(results_df)
    validator.plot_validation_structure()
    validator.save_results(results_df)

    # Zusammenfassung ausgeben
    if not results_df.empty:
        print("\n--- Zusammenfassung ---")
        print(f"Durchschnittlicher Test RMSE: {results_df['test_rmse'].mean():.4f}")
        print(f"Bester Test RMSE: {results_df['test_rmse'].min():.4f} bei {results_df.loc[results_df['test_rmse'].idxmin(), 'data_percentage']*100:.0f}% der Daten")
        
    total_time = time.time() - start_time
    print(f"\nGesamtlaufzeit: {total_time:.2f} Sekunden")

    return results_df


def main():
    # Parameter für verschiedene Städte laden
    try:
        # Angeles
        from results.model_parameters.angeles_params import order as angeles_order, seasonal_order as angeles_seasonal_order
        print(f"SARIMA-Parameter für 'abakan' geladen: {angeles_order}x{angeles_seasonal_order}")

        # Analyse durchführen
        results = run_sarima_progressive_validation('abakan', angeles_order, angeles_seasonal_order)

    except ImportError as e:
        print(f"Fehler beim Laden der Parameter: {e}")
        print("Bitte zuerst sarima_parameter_finder.py ausführen!")
        sys.exit(1)
    except Exception as e:
        print(f"Fehler bei der Analyse: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()