import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tools.eval_measures import rmse, mse
from sklearn.model_selection import KFold
from Hilfsfunktionen.DatenEinlesen import DatenEinlesen

import sys
import os

# Übergeordnetes Verzeichnis zum Python-Pfad hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Jetzt sollte der Import von config funktionieren
import config

input_file = config.PATH_TS_BERLIN_CLEAN

def main(input_file):
    # 1. Daten einlesen
    df = DatenEinlesen(input_file, sep=",")
    if df is None:
        print(f"Fehler beim Einlesen der Daten aus {input_file}.")
        return
    print("Daten erfolgreich eingelesen!")

    # 2. Datum als Index setzen und Frequenz sicherstellen
    df['Datum'] = pd.to_datetime(df['Datum'])
    df.set_index('Datum', inplace=True)
    df.index = pd.date_range(start=df.index[0], periods=len(df), freq='MS')

    # 3. Zeitreihe extrahieren
    ts = df['MonatlicheDurchschnittsTemperatur'].dropna().squeeze()

    # 4. K-Fold Cross-Validation
    k = 5
    kf = KFold(n_splits=k, shuffle=False)

    train_rmse_errors, test_rmse_errors = [], []
    train_mse_errors, test_mse_errors = [], []

    def find_best_sarima(train, p_values, q_values, P_values, Q_values, s):
        best_aic = float('inf')
        best_order = None
        best_seasonal_order = None
        d = 0  # keine Differenzierung notwendig
        D = 1  # saisonale Differenzierung ebenfalls erstmal nicht notwendig

        for p in p_values:
            for q in q_values:
                for P in P_values:
                    for Q in Q_values:
                        try:
                            model = SARIMAX(train,
                                            order=(p, d, q),
                                            seasonal_order=(P, D, Q, s),
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
                            result = model.fit(disp=False)
                            if result.aic < best_aic:
                                best_aic = result.aic
                                best_order = (p, d, q)
                                best_seasonal_order = (P, D, Q, s)
                        except:
                            continue
        return best_order, best_seasonal_order

    # Parameterbereiche
    p_values = range(0, 3)
    q_values = range(0, 3)
    P_values = range(0, 2)
    Q_values = range(0, 2)
    s = 12  # Saisonlänge (12 Monate)

    fold = 1
    for train_idx, test_idx in kf.split(ts):
        train, test = ts.iloc[train_idx], ts.iloc[test_idx]

        best_order, best_seasonal_order = find_best_sarima(train, p_values, q_values, P_values, Q_values, s)

        model = SARIMAX(train,
                        order=best_order,
                        seasonal_order=best_seasonal_order,
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        result = model.fit(disp=False)

        pred_train = result.predict(start=train.index[0], end=train.index[-1])
        pred_test = result.forecast(steps=len(test))

        train_rmse_errors.append(rmse(train, pred_train))
        train_mse_errors.append(mse(train, pred_train))
        test_rmse_errors.append(rmse(test, pred_test))
        test_mse_errors.append(mse(test, pred_test))

        print(f"Fold {fold}: Best SARIMA{best_order} x {best_seasonal_order}")
        print(f"Train RMSE: {train_rmse_errors[-1]:.4f}, Test RMSE: {test_rmse_errors[-1]:.4f}")
        fold += 1

    # 5. Durchschnittliche Fehler ausgeben
    print("\n--- Durchschnittliche Fehler ---")
    print(f"Train RMSE: {np.mean(train_rmse_errors):.4f}, MSE: {np.mean(train_mse_errors):.4f}")
    print(f"Test RMSE: {np.mean(test_rmse_errors):.4f}, MSE: {np.mean(test_mse_errors):.4f}")

# Beispielaufruf
main(input_file)
