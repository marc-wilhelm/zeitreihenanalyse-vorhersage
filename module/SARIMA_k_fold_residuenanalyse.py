import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tools.eval_measures import rmse, mse
from sklearn.model_selection import KFold
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

# Importiere die zuvor bestimmten SARIMA-Parameter
try:
    from parameter.sarima_params_angeles import order as angeles_order, seasonal_order as angeles_seasonal_order
    print(f"SARIMA-Parameter für 'angeles' geladen: {angeles_order}x{angeles_seasonal_order}")
except ImportError:
    print("FEHLER: SARIMA-Parameter für 'angeles' nicht gefunden.")
    print("Bitte zuerst sarima_parameter_finder.py ausführen, um die Parameter zu bestimmen.")
    sys.exit(1)

def plot_residual_analysis(resid, fold, output_dir):
    """
    Erzeuge Plots zur Analyse der Residuen
    """
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    
    # Residualplot
    axs[0, 0].plot(resid, color='steelblue')
    axs[0, 0].set_title(f'Residuen - Fold {fold}')
    axs[0, 0].set_xlabel('Zeit')
    axs[0, 0].set_ylabel('Residuum')
    axs[0, 0].grid(True, alpha=0.3)
    
    # Autokorrelationsplot
    plot_acf(resid, ax=axs[0, 1], lags=24, alpha=0.05)
    axs[0, 1].set_title('ACF der Residuen')
    axs[0, 1].grid(True, alpha=0.3)
    
    # Histogramm
    sns.histplot(resid, kde=True, stat="density", bins=25, color="skyblue", ax=axs[1, 0])
    xmin, xmax = axs[1, 0].get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, resid.mean(), resid.std())
    axs[1, 0].plot(x, p, 'r', linewidth=2)
    axs[1, 0].set_title('Histogramm der Residuen mit Normalverteilung')
    axs[1, 0].grid(True, alpha=0.3)
    
    # Q-Q Plot
    stats.probplot(resid, plot=axs[1, 1])
    axs[1, 1].set_title('Q-Q Plot der Residuen')
    axs[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"sarima_residuen_fold_{fold}.png"), dpi=300)
    plt.close(fig)

def sarima_kfold_analysis(ts_data, ts_name, order, seasonal_order, k=5):
    """
    Führe K-Fold-Validierung und Residuenanalyse für SARIMA mit festgelegten Parametern durch
    
    Parameter:
    ----------
    ts_data : pandas.Series
        Die zu analysierende Zeitreihe
    ts_name : str
        Name der Zeitreihe (für die Ausgabedateien)
    order : tuple
        (p, d, q) - nicht-saisonaler Teil des SARIMA-Modells
    seasonal_order : tuple
        (P, D, Q, m) - saisonaler Teil des SARIMA-Modells
    k : int, default=5
        Anzahl der Folds für die Kreuzvalidierung
    """
    # Ausgabeverzeichnis erstellen
    output_dir = f"./ergebnisse/{ts_name}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Starte SARIMA-Analyse mit K-Fold-Validierung für '{ts_name}'...")
    print(f"Verwende SARIMA{order}x{seasonal_order}")
    
    kf = KFold(n_splits=k, shuffle=False)
    
    results = {
        'fold': [], 
        'train_rmse': [], 'test_rmse': [], 
        'train_mse': [], 'test_mse': [],
        'ljung_box_pvalue': [], 'shapiro_pvalue': [],
        'skewness': [], 'kurtosis': []
    }
    
    total_start_time = time.time()
    fold = 1
    
    for train_idx, test_idx in kf.split(ts_data):
        fold_start_time = time.time()
        print(f"\n--- Fold {fold}/{k} ---")
        
        train, test = ts_data.iloc[train_idx], ts_data.iloc[test_idx]
        print(f"Trainingsdaten: {len(train)}, Testdaten: {len(test)}")
        
        # SARIMA-Modell mit den vordefinierten Parametern fitten
        try:
            model = SARIMAX(
                train,
                order=order,
                seasonal_order=seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            result = model.fit(disp=False, low_memory=True)
            
            # Vorhersagen
            pred_train = result.predict(start=0, end=len(train) - 1)
            pred_test = result.predict(start=len(train), end=len(train) + len(test) - 1)
            
            # Fehlermetriken berechnen
            train_rmse_val = rmse(train, pred_train)
            test_rmse_val = rmse(test, pred_test)
            train_mse_val = mse(train, pred_train)
            test_mse_val = mse(test, pred_test)
            
            # Residuenanalyse
            resid = result.resid
            lb_test = acorr_ljungbox(resid, lags=[12], return_df=True)
            stat, p_value = shapiro(resid)
            resid_skew = skew(resid)
            resid_kurtosis = kurtosis(resid)
            
            # Ergebnisse speichern
            results['fold'].append(fold)
            results['train_rmse'].append(train_rmse_val)
            results['test_rmse'].append(test_rmse_val)
            results['train_mse'].append(train_mse_val)
            results['test_mse'].append(test_mse_val)
            results['ljung_box_pvalue'].append(lb_test['lb_pvalue'].values[0])
            results['shapiro_pvalue'].append(p_value)
            results['skewness'].append(resid_skew)
            results['kurtosis'].append(resid_kurtosis)
            
            # Residuenplots erstellen
            plot_residual_analysis(resid, fold, output_dir)
            
            fold_time = time.time() - fold_start_time
            print(f"Fold {fold} abgeschlossen in {fold_time:.2f}s")
            print(f"Train RMSE: {train_rmse_val:.4f}, Test RMSE: {test_rmse_val:.4f}")
            
        except Exception as e:
            print(f"Fehler in Fold {fold}: {e}")
            import traceback
            traceback.print_exc()
        
        fold += 1
    
    # Zusammenfassung in CSV speichern
    summary_df = pd.DataFrame(results)
    summary_df['model'] = f"SARIMA{order}x{seasonal_order}"
    summary_file = os.path.join(output_dir, f"sarima_{ts_name}_results_summary.csv")
    summary_df.to_csv(summary_file, index=False)
    
    # Zusammenfassung der Metriken ausgeben
    print("\n--- Durchschnittliche Fehler ---")
    print(f"Train RMSE: {np.mean(results['train_rmse']):.4f}, Test RMSE: {np.mean(results['test_rmse']):.4f}")
    print(f"Train MSE: {np.mean(results['train_mse']):.4f}, Test MSE: {np.mean(results['test_mse']):.4f}")
    
    print("\n--- Durchschnittliche Residuenstatistiken ---")
    print(f"Ljung-Box-Test p-Wert: {np.mean(results['ljung_box_pvalue']):.4f}")
    print(f"Shapiro-Wilk-Test p-Wert: {np.mean(results['shapiro_pvalue']):.4f}")
    print(f"Schiefe der Residuen: {np.mean(results['skewness']):.4f}")
    print(f"Kurtosis der Residuen: {np.mean(results['kurtosis']):.4f}")
    
    # RMSE-Vergleichsplot erstellen
    plt.figure(figsize=(10, 6))
    plt.bar(range(1, k+1), results['test_rmse'], color='royalblue')
    plt.axhline(y=np.mean(results['test_rmse']), color='r', linestyle='-', 
                label=f'Durchschnittlicher Test RMSE: {np.mean(results["test_rmse"]):.4f}')
    plt.xlabel('Fold')
    plt.ylabel('Test RMSE')
    plt.title(f'Test RMSE für jeden Fold - {ts_name}')
    plt.xticks(range(1, k+1))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"sarima_{ts_name}_test_rmse_comparison.png"), dpi=300)
    
    total_time = time.time() - total_start_time
    print(f"\nGesamtlaufzeit: {total_time:.2f} Sekunden")
    
    return summary_df

def main():
    # Zeitreihe aus Config laden
    stat_ts = config.seasonal_diff_angeles.squeeze()
  


    print(f"Zeitreihe geladen: {len(stat_ts)} Datenpunkte")
    
    # K-Fold-Validierung und Residuenanalyse durchführen
    try:
        summary = sarima_kfold_analysis(
            stat_ts,
            'angeles',
            order=angeles_order,
            seasonal_order=angeles_seasonal_order,
            k=5
        )
        print("\nSARIMA-Analyse erfolgreich abgeschlossen.")
    except Exception as e:
        print(f"Fehler bei der SARIMA-Analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()