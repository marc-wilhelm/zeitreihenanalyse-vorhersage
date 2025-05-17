import os
import sys
import importlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tools.eval_measures import rmse, mse

# === Zentrale Konfiguration importieren ===
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

# Projektpfade initialisieren
config.init_project_paths()

# === Expanding-Window-Klasse ===
class expanding_window(object):
    def __init__(self, initial=1, horizon=1, period=1):
        self.initial = initial
        self.horizon = horizon
        self.period = period

    def split(self, data):
        self.data = data
        self.counter = 0
        data_length = data.shape[0]
        data_index = list(np.arange(data_length))
        output_train = []
        output_test = []

        output_train.append(list(np.arange(self.initial)))
        progress = [x for x in data_index if x not in list(np.arange(self.initial))]
        output_test.append([x for x in data_index if x not in output_train[self.counter]][:self.horizon])

        while len(progress) != 0:
            temp = progress[:self.period]
            to_add = output_train[self.counter] + temp
            output_train.append(to_add)
            self.counter += 1
            to_add_test = [x for x in data_index if x not in output_train[self.counter]][:self.horizon]
            output_test.append(to_add_test)
            progress = [x for x in data_index if x not in output_train[self.counter]]

        output_train = output_train[:-1]
        output_test = output_test[:-1]
        return list(zip(output_train, output_test))

def plot_residuals(residuals, city, fold):
    """Erstellt Residuenanalyse-Plots für einen Fold"""
    output_dir = config.get_city_output_dir(config.OUTPUT_SARIMA_RESIDUEN, city)

    plt.figure(figsize=(10, 8))

    plt.subplot(2, 2, 1)
    plt.plot(residuals)
    plt.title("Residuen über Zeit")
    plt.xlabel("Zeit")
    plt.ylabel("Residuum")

    plt.subplot(2, 2, 2)
    plot_acf(residuals, ax=plt.gca(), alpha=0.05)
    plt.title("ACF der Residuen")

    plt.subplot(2, 2, 3)
    try:
        import seaborn as sns
        sns.histplot(residuals, kde=True, stat="density", bins=30, color='skyblue')
    except ImportError:
        plt.hist(residuals, bins=30, density=True, alpha=0.7, color='skyblue')
    plt.title("Histogramm der Residuen")

    plt.subplot(2, 2, 4)
    stats.probplot(residuals, dist="norm", plot=plt)
    plt.title("Q-Q-Plot der Residuen")

    plt.suptitle(f"Residuenanalyse – Fold {fold}", y=1.02)
    plt.tight_layout()
    plot_path = os.path.join(output_dir, f"residuen_fold_{fold}.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"📊 Residuenanalyse gespeichert: residuen_fold_{fold}.png")

def append_residual_analysis_summary(city, results_df, avg_ljung_pvalue):
    """Fügt Residuenanalyse-Zusammenfassung zur Evaluation-Datei hinzu"""
    file_path = os.path.join(config.OUTPUT_EVALUATIONS_METRIKEN, f"{city}_evaluation.py")
    header = "# === Residuenanalyse nach Test des gefundenen SARIMA-Modells ==="

    summary_lines = [f"\n{header}"]
    summary_lines.append(f"# Folds ausgewertet: {len(results_df)}")
    summary_lines.append(f"# Durchschnittlicher Train-RMSE: {results_df['train_rmse'].mean():.4f}")
    summary_lines.append(f"# Durchschnittlicher Test-RMSE:  {results_df['test_rmse'].mean():.4f}")
    summary_lines.append(f"# Durchschnittlicher Train-MSE:  {results_df['train_mse'].mean():.4f}")
    summary_lines.append(f"# Durchschnittlicher Test-MSE:   {results_df['test_mse'].mean():.4f}")
    summary_lines.append(f"# Durchschnittlicher Ljung-Box p-Wert (Lag 10): {avg_ljung_pvalue:.4f}")

    summary_text = "\n".join(summary_lines) + "\n"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if header in content:
            pre_content = content.split(header)[0].rstrip()
            new_content = pre_content + summary_text
        else:
            new_content = content.rstrip() + summary_text
    else:
        new_content = summary_text

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"📁 Zusammenfassung für {city} gespeichert unter: {file_path}")

def run_expanding_sarima_cv(city):
    """Führt Expanding-Window Cross-Validation für SARIMA-Modell durch"""
    print(f"\n📍 Stadt: {city}")

    # === Modellparameter laden ===
    param_module = f"ergebnisse.model_parameters.{city}_params"
    try:
        params = importlib.import_module(param_module)
        order = params.order
        seasonal_order = params.seasonal_order
    except ImportError:
        print(f"❌ Keine Parameter-Datei gefunden für {city}")
        return pd.DataFrame()

    # === Daten aus CSV laden ===
    input_path = config.get_stationary_data_path(city)
    try:
        df = pd.read_csv(input_path)
        series = df["MonatlicheDurchschnittsTemperatur"].squeeze()
    except Exception as e:
        print(f"❌ Fehler beim Laden der Daten für {city}: {e}")
        return pd.DataFrame()

    print(f"🔧 Verwende SARIMA{order}x{seasonal_order}")
    print(f"📄 Anzahl Datenpunkte: {len(series)}")

    splitter = expanding_window(initial=800, horizon=160, period=160)
    splits = splitter.split(series)

    results = []
    ljung_pvalues = []

    for fold, (train_idx, test_idx) in enumerate(splits):
        train = series.iloc[train_idx]
        test = series.iloc[test_idx]

        print(f"\n🔁 Fold {fold + 1}")
        print(f"   → Trainingsdaten: {len(train)}")
        print(f"   → Testdaten:      {len(test)}")

        try:
            model = SARIMAX(train,
                            order=order,
                            seasonal_order=seasonal_order,
                            enforce_stationarity=False,
                            enforce_invertibility=False)
            fit = model.fit(disp=False)

            pred_train = fit.get_prediction(start=0, end=len(train)-1).predicted_mean
            forecast = fit.get_forecast(steps=len(test)).predicted_mean
            residuals = train - pred_train

            test_rmse = rmse(test.values, forecast.values)
            train_rmse = rmse(train.values, pred_train.values)
            test_mse = mse(test.values, forecast.values)
            train_mse = mse(train.values, pred_train.values)

            from statsmodels.stats.diagnostic import acorr_ljungbox
            ljung_result = acorr_ljungbox(residuals, lags=[10], return_df=True)
            ljung_pvalue = ljung_result["lb_pvalue"].iloc[0]
            ljung_pvalues.append(ljung_pvalue)

            results.append({
                "fold": fold + 1,
                "train_size": len(train),
                "test_size": len(test),
                "train_rmse": train_rmse,
                "test_rmse": test_rmse,
                "train_mse": train_mse,
                "test_mse": test_mse,
                "ljung_pvalue": ljung_pvalue
            })

            print(f"   ✅ Train-RMSE: {train_rmse:.4f} | Train-MSE: {train_mse:.4f}")
            print(f"   ✅ Test-RMSE:  {test_rmse:.4f} | Test-MSE:  {test_mse:.4f}")

            plot_residuals(residuals, city, fold + 1)

        except Exception as e:
            print(f"   ❌ Fehler in Fold {fold + 1}: {e}")
            continue

    results_df = pd.DataFrame(results)

    if not results_df.empty:
        print(f"\n📊 --- Zusammenfassung für {city} ---")
        print(f"Folds ausgewertet: {len(results_df)}")
        print(f"Durchschnittlicher Train-RMSE: {results_df['train_rmse'].mean():.4f}")
        print(f"Durchschnittlicher Test-RMSE:  {results_df['test_rmse'].mean():.4f}")
        print(f"Durchschnittlicher Train-MSE:  {results_df['train_mse'].mean():.4f}")
        print(f"Durchschnittlicher Test-MSE:   {results_df['test_mse'].mean():.4f}")

        if ljung_pvalues:
            avg_ljung_pvalue = sum(ljung_pvalues) / len(ljung_pvalues)
            print(f"Durchschnittlicher Ljung-Box p-Wert (Lag 10): {avg_ljung_pvalue:.4f}")
        else:
            avg_ljung_pvalue = float("nan")

        append_residual_analysis_summary(city, results_df, avg_ljung_pvalue)

    else:
        print(f"\n⚠️ Keine gültigen Folds ausgewertet für {city}.")

    return results_df

def main():
    """Führt SARIMA Expanding Window Residuenanalyse für alle Städte durch"""
    print("🔬 SARIMA Expanding Window Residuenanalyse wird gestartet...")

    for city in config.CITIES:
        try:
            run_expanding_sarima_cv(city)
        except Exception as e:
            print(f"❌ Fehler bei Stadt {city}: {e}")

    print(f"\n✅ SARIMA Residuenanalyse abgeschlossen.")
    print(f"📁 Ergebnisse gespeichert in: {config.OUTPUT_SARIMA_RESIDUEN}")

# === Hauptausführung ===
if __name__ == "__main__":
    main()