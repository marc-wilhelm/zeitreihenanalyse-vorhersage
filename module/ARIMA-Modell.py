import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tools.eval_measures import rmse, mse
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt

import sys
import os
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, skew, kurtosis  # Korrekte Imports hinzufügen
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox

# Übergeordnetes Verzeichnis zum Python-Pfad hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Jetzt sollte der Import von config funktionieren
import config

# Ordner für Plots anlegen (falls nicht vorhanden)
output_dir = "./ergebnisse"
os.makedirs(output_dir, exist_ok=True)

input_file = config.temp_abakan


def main(input_file):
    # 1. Daten einlesen
    #df = DatenEinlesen(input_file, sep=",")

    #if df is None:
        #print(f"Fehler beim Einlesen der Daten aus {input_file}. Überspringe diese Datei.")
        #return

    #print("Daten erfolgreich eingelesen!")

    # 2. Zeitreihe extrahieren
    #stat_ts = df['MonatlicheDurchschnittsTemperatur'].dropna().squeeze()
    stat_ts = config.temp_abakan.squeeze()

    # 3. K-Fold Cross-Validation
    k = 5
    kf = KFold(n_splits=k, shuffle=False)

    train_rmse_errors, test_rmse_errors = [], []
    train_mse_errors, test_mse_errors = [], []

    def find_best_arima(train, p_values, q_values):
        best_aic = float('inf')
        best_order = None
        d = 0
          # keine Differenzierung notwendig, da stationär
        for p in p_values:
            for q in q_values:
                try:
                    model = ARIMA(train.tolist(), order=(p, d, q))
                    result = model.fit()
                    if result.aic < best_aic:
                        best_aic = result.aic
                        best_order = (p, d, q)
                except:
                    continue
        return best_order

    p_values = range(0, 5)
    q_values = range(0, 3)

    fold = 1
    for train_idx, test_idx in kf.split(stat_ts):
        train, test = stat_ts.iloc[train_idx], stat_ts.iloc[test_idx]

        best_order = find_best_arima(train, p_values, q_values)
        model = ARIMA(train.tolist(), order=best_order)
        result = model.fit()

        pred_train = result.predict(start=0, end=len(train) - 1)
        pred_test = result.predict(start=len(train), end=len(train) + len(test) - 1)

        train_rmse_errors.append(rmse(train, pred_train))
        train_mse_errors.append(mse(train, pred_train))
        test_rmse_errors.append(rmse(test, pred_test))
        test_mse_errors.append(mse(test, pred_test))

        print(f"Fold {fold}: Best ARIMA{best_order}")
        print(f"Train RMSE: {train_rmse_errors[-1]:.4f}, Test RMSE: {test_rmse_errors[-1]:.4f}")

        # --------------------
        # Residuenanalyse
        # --------------------
        resid = result.resid

        fig, axs = plt.subplots(1, 3, figsize=(14, 4))

        # 1. Zeitplot der Residuen
        axs[0].plot(resid)
        axs[0].set_title(f'Residuen – Fold {fold}')
        axs[0].set_xlabel('Zeit')
        axs[0].set_ylabel('Residuum')
        axs[0].grid(True)

        # 2. ACF der Residuen
        plot_acf(resid, ax=axs[1], lags=20)
        axs[1].set_title('ACF der Residuen')

        # 3. Histogramm mit Normalverteilung
        sns.histplot(resid, kde=True, stat="density", bins=20, color="skyblue", ax=axs[2])
        xmin, xmax = axs[2].get_xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, resid.mean(), resid.std())
        axs[2].plot(x, p, 'r', linewidth=2)
        axs[2].set_title('Histogramm der Residuen')

        plt.tight_layout()

        # → Speichern statt anzeigen
        plot_path = os.path.join(output_dir, f"residuen_fold_{fold}.png")
        plt.savefig(plot_path)
        plt.close(fig)

        # Ljung-Box-Test
        lb_test = acorr_ljungbox(resid, lags=[10], return_df=True)
        print(f"Ljung-Box-Test p-Wert (Fold {fold}): {lb_test['lb_pvalue'].values[0]:.4f}")

        # Shapiro-Wilk-Test für Normalität der Residuen
        stat, p_value = shapiro(resid)
        print(f"Shapiro-Wilk-Test p-Wert (Fold {fold}): {p_value:.4f}")

        # Berechne Schiefe (Skewness) und Kurtosis der Residuen
        resid_skew = skew(resid)
        resid_kurtosis = kurtosis(resid)
        print(f"Schiefe der Residuen (Fold {fold}): {resid_skew:.4f}")
        print(f"Kurtosis der Residuen (Fold {fold}): {resid_kurtosis:.4f}")

        fold += 1

    # 4. Durchschnittliche Fehler ausgeben
    print("\n--- Durchschnittliche Fehler ---")
    print(f"Train RMSE: {np.mean(train_rmse_errors):.4f}, MSE: {np.mean(train_mse_errors):.4f}")
    print(f"Test RMSE: {np.mean(test_rmse_errors):.4f}, MSE: {np.mean(test_mse_errors):.4f}")

    # Zusammenfassung der Testergebnisse
    print("\n--- Zusammenfassung der Ergebnisse ---")
    for f in range(1, fold):
        print(f"\nFold {f}:")
        print(f"Ljung-Box-Test p-Wert: {lb_test['lb_pvalue'].values[0]:.4f}")
        print(f"Shapiro-Wilk-Test p-Wert: {p_value:.4f}")
        print(f"Schiefe der Residuen: {resid_skew:.4f}")
        print(f"Kurtosis der Residuen: {resid_kurtosis:.4f}")

# Beispielaufruf
main(input_file)