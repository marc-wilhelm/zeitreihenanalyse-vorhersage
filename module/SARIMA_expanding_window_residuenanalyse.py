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
    output_dir = os.path.join("results", "sarima_residuen_auswertung", city)
    os.makedirs(output_dir, exist_ok=True)

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
    import seaborn as sns
    sns.histplot(residuals, kde=True, stat="density", bins=30, color='skyblue')
    plt.title("Histogramm der Residuen")

    plt.subplot(2, 2, 4)
    stats.probplot(residuals, dist="norm", plot=plt)
    plt.title("Q-Q-Plot der Residuen")

    plt.suptitle(f"Residuenanalyse – Fold {fold}", y=1.02)
    plt.tight_layout()
    plot_path = os.path.join(output_dir, f"residuen_fold_{fold}.png")
    plt.savefig(plot_path)
    plt.close()


def run_expanding_sarima_cv(city):
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # === Modellparameter laden ===
    param_module = f"results.model_parameters.{city}_params"
    params = importlib.import_module(param_module)
    order = params.order
    seasonal_order = params.seasonal_order

    # === Daten aus CSV laden ===
    input_path = os.path.join("daten", "stationäre-daten", f"stationaere_zeitreihe_{city}.csv")
    df = pd.read_csv(input_path)
    series = df["MonatlicheDurchschnittsTemperatur"].squeeze()

    print(f"\n📍 Stadt: {city}")
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

            forecast = fit.forecast(steps=len(test))
            pred_train = fit.get_prediction(start=0, end=len(train)-1).predicted_mean
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
        print(f"\n⚠️ Keine gültigen Folds ausgewertet für {city}.")

    return results_df


# === Hauptschleife über alle Städte ===
if __name__ == "__main__":
    for city in ["angeles", "abakan", "berlin"]:
        run_expanding_sarima_cv(city)
