import os
import sys
import importlib
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tools.eval_measures import rmse

# === Verbesserte Expanding-Window-Klasse ===
class expanding_window(object):
    def __init__(self, ratio=0.7, horizon=160, period=160):
        self.ratio = ratio
        self.horizon = horizon
        self.period = period

    def split(self, data):
        data_length = len(data)

        initial_window = int(data_length * self.ratio)
        output_train = []
        output_test = []

        train_end = initial_window
        while train_end + self.horizon <= data_length:
            train_idx = list(range(train_end))
            test_idx = list(range(train_end, train_end + self.horizon))

            output_train.append(train_idx)
            output_test.append(test_idx)

            train_end += self.period

        return list(zip(output_train, output_test))


# === SARIMA Expanding Window Cross-Validation ===
def run_expanding_sarima_cv(city):
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # SARIMA-Parameter laden
    param_module = f"results.model_parameters.{city}_params"
    params = importlib.import_module(param_module)
    order = params.order
    seasonal_order = params.seasonal_order

    # Daten laden
   


    import config
    series = getattr(config, f'seasonal_diff_{city}').squeeze()
    print(series)
    
    


    print(f"\n📍 Stadt: {city}")
    print(f"🔧 Verwende SARIMA{order}x{seasonal_order}")
    print(f"📄 Anzahl Datenpunkte: {len(series)}")

    # Expanding Window mit stabiler Testgröße
    splitter = expanding_window(ratio=0.7, horizon=160, period=160)
    splits = splitter.split(series)

    results = []

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

            forecast = fit.forecast(steps=len(test))
            pred_train = fit.get_prediction(start=0, end=len(train)-1).predicted_mean

            test_rmse = rmse(test.values, forecast.values)
            train_rmse = rmse(train.values, pred_train.values)

            results.append({
                "fold": fold + 1,
                "train_size": len(train),
                "test_size": len(test),
                "train_rmse": train_rmse,
                "test_rmse": test_rmse
            })

            print(f"   ✅ Train-RMSE: {train_rmse:.4f}")
            print(f"   ✅ Test-RMSE:  {test_rmse:.4f}")

        except Exception as e:
            print(f"   ❌ Fehler in Fold {fold + 1}: {e}")
            continue

    results_df = pd.DataFrame(results)

    if not results_df.empty:
        print("\n📊 --- Zusammenfassung ---")
        print(f"Folds ausgewertet: {len(results_df)}")
        print(f"Durchschnittlicher Train-RMSE: {results_df['train_rmse'].mean():.4f}")
        print(f"Durchschnittlicher Test-RMSE:  {results_df['test_rmse'].mean():.4f}")
    else:
        print("\n⚠️ Keine gültigen Folds ausgewertet.")

    return results_df


# === Main ===
if __name__ == "__main__":
    run_expanding_sarima_cv("angeles")
