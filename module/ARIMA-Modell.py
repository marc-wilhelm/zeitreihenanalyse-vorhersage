import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tools.eval_measures import rmse, mse
from sklearn.model_selection import KFold
from Hilfsfunktionen.DatenEinlesen import DatenEinlesen

import sys
import os

# Übergeordnetes Verzeichnis zum Python-Pfad hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Jetzt sollte der Import von config funktionieren
import config


input_file =config.temp_diff_angeles


def main(input_file):

    

    # 1. Daten einlesen
    #df = DatenEinlesen(input_file, sep=",")

    #if df is None:
        #print(f"Fehler beim Einlesen der Daten aus {input_file}. Überspringe diese Datei.")
        #return

    #print("Daten erfolgreich eingelesen!")

    # 2. Spalte 'Datum' in datetime umwandeln und als Index setzen
    #df['Datum'] = pd.to_datetime(df['Datum'])
    #df.set_index('Datum', inplace=True)

    # 3. Zeitreihe extrahieren
    #ts = df['MonatlicheDurchschnittsTemperatur'].dropna().squeeze()
    stat_ts = config.temp_diff_angeles.squeeze()


    # 4. K-Fold Cross-Validation
    k = 5
    kf = KFold(n_splits=k, shuffle=False)

    train_rmse_errors, test_rmse_errors = [], []
    train_mse_errors, test_mse_errors = [], []

    def find_best_arima(train, p_values, q_values):
        best_aic = float('inf')
        best_order = None
        d = 1  # keine Differenzierung notwendig, da stationär
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
        fold += 1

    # 5. Durchschnittliche Fehler ausgeben
    print("\n--- Durchschnittliche Fehler ---")
    print(f"Train RMSE: {np.mean(train_rmse_errors):.4f}, MSE: {np.mean(train_mse_errors):.4f}")
    print(f"Test RMSE: {np.mean(test_rmse_errors):.4f}, MSE: {np.mean(test_mse_errors):.4f}")

# Beispielaufruf
main(input_file)
