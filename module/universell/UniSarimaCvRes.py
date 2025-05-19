import os
import sys
import importlib.util
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tools.eval_measures import rmse, mse
import warnings
warnings.filterwarnings("ignore")

# === Projektstruktur einbinden ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

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
    """Erstellt Residuenanalyse-Plots für einen Fold mit universellen Parametern"""
    output_dir = config.get_city_output_dir(config.OUTPUT_SARIMA_RESIDUEN_UNIVERSELL, city)

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
    print(f"    Residuenanalyse gespeichert: {plot_path}")


def append_confidence_interval_summary(city, avg_conf_int, results_df, avg_ljung_pvalue):
    """Fügt Konfidenzintervall und Evaluationsmetriken zur Evaluation-Datei hinzu"""
    os.makedirs(config.OUTPUT_EVALUATIONS_METRIKEN_UNIVERSELL, exist_ok=True)
    file_path = os.path.join(config.OUTPUT_EVALUATIONS_METRIKEN_UNIVERSELL, f"{city}_evaluation.py")

    header_ci = "\n# === Konfidenzintervall ==="
    header_eval = "# === Durchschnittliche Evaluationsmetriken ==="

    summary_lines = [f"\n{header_eval}"]
    summary_lines.append(f"# Durchschnittlicher Train-RMSE: {results_df['train_rmse'].mean():.4f}")
    summary_lines.append(f"# Durchschnittlicher Test-RMSE:  {results_df['test_rmse'].mean():.4f}")
    summary_lines.append(f"# Durchschnittlicher Train-MSE:  {results_df['train_mse'].mean():.4f}")
    summary_lines.append(f"# Durchschnittlicher Test-MSE:   {results_df['test_mse'].mean():.4f}")
    summary_lines.append(f"# Durchschnittlicher Ljung-Box p-Wert (Lag 10): {avg_ljung_pvalue:.4f}\n")

    summary_lines.append(header_ci)
    for param, row in avg_conf_int.iterrows():
        summary_lines.append(f"# {param}: [{row[0]:.6f}, {row[1]:.6f}]")

    summary_text = "\n".join(summary_lines) + "\n"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = content.split("# === Durchschnittliche Evaluationsmetriken ===")[0].rstrip()
        new_content = content + summary_text
    else:
        new_content = summary_text

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f" Konfidenzintervall und Metriken gespeichert unter: {file_path}")


def run_expanding_sarima_cv(city):
    """Führt Expanding-Window Cross-Validation für SARIMA-Modell mit universellen Parametern durch"""
    # Universelle Parameter laden
    shared_param_path = os.path.join(config.OUTPUT_MODEL_PARAMETERS_UNIVERSELL, "gemeinsame_parameter.py")

    try:
        spec = importlib.util.spec_from_file_location("shared_params", shared_param_path)
        params = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(params)
        order = params.order
        seasonal_order = params.seasonal_order
    except Exception as e:
        print(f" Fehler beim Laden der universellen Parameter: {e}")
        return pd.DataFrame()

    # Daten aus stationärer Zeitreihe laden
    input_path = config.get_stationary_data_path(city)
    try:
        df = pd.read_csv(input_path)
        series = df["MonatlicheDurchschnittsTemperatur"].squeeze()
    except Exception as e:
        print(f" Fehler beim Laden der stationären Daten für {city}: {e}")
        return pd.DataFrame()

    print(f"\n Stadt: {city}")
    print(f" Verwende gemeinsame SARIMA{order}x{seasonal_order}")
    print(f" Anzahl Datenpunkte: {len(series)}")

    # CV mit Expanding Window
    splitter = expanding_window(initial=800, horizon=160, period=160)
    splits = splitter.split(series)

    results = []
    ljung_pvalues = []
    conf_int_list = []

    for fold, (train_idx, test_idx) in enumerate(splits):
        train = series.iloc[train_idx]
        test = series.iloc[test_idx]

        print(f"\n Fold {fold + 1}")
        print(f"   → Trainingsdaten: {len(train)}")
        print(f"   → Testdaten:      {len(test)}")

        try:
            model = SARIMAX(train,
                            order=order,
                            seasonal_order=seasonal_order,
                            enforce_stationarity=False,
                            enforce_invertibility=False)
            fit = model.fit(disp=False)

            conf_int_params = fit.conf_int(alpha=0.05)
            conf_int_list.append(conf_int_params)

            forecast_res = fit.get_forecast(steps=len(test))
            forecast = forecast_res.predicted_mean
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

            print(f"    Train-RMSE: {train_rmse:.4f} | Train-MSE: {train_mse:.4f}")
            print(f"    Test-RMSE:  {test_rmse:.4f} | Test-MSE:  {test_mse:.4f}")

            plot_residuals(residuals, city, fold + 1)

        except Exception as e:
            print(f"    Fehler in Fold {fold + 1}: {e}")
            continue

    results_df = pd.DataFrame(results)

    if conf_int_list and not results_df.empty:
        avg_conf_int = pd.concat(conf_int_list).groupby(level=0).mean()
        avg_ljung_pvalue = sum(ljung_pvalues) / len(ljung_pvalues) if ljung_pvalues else float("nan")
        append_confidence_interval_summary(city, avg_conf_int, results_df, avg_ljung_pvalue)

    return results_df


def main():
    """Hauptfunktion für universelle SARIMA Cross-Validation"""
    print(" Universelle SARIMA Cross-Validation wird gestartet...")

    # Ausgabeordner erstellen
    config.ensure_output_dirs()

    # CrossValidation für alle Städte durchführen
    cities = config.CITIES
    successful_cities = 0

    for city in cities:
        try:
            print("\n" + "="*50)
            print(f" Bearbeite Stadt: {city.upper()}")
            print("="*50)

            results_df = run_expanding_sarima_cv(city)

            if not results_df.empty:
                successful_cities += 1
                print(f"\n SARIMA CV für {city} erfolgreich durchgeführt.")
            else:
                print(f"\n Keine validen Ergebnisse für {city}.")

        except Exception as e:
            print(f" Fehler bei Stadt {city}: {str(e)[:150]}...")

    # Zusammenfassung ausgeben
    print("\n" + "="*60)
    print(" ZUSAMMENFASSUNG - UNIVERSELLE SARIMA CV")
    print("="*60)
    print(f" Erfolgreiche Städte: {successful_cities}/{len(cities)}")
    print(f" Ergebnisse gespeichert unter: {config.OUTPUT_SARIMA_RESIDUEN_UNIVERSELL}")
    print("="*60)


# === Hauptausführung ===
if __name__ == "__main__":
    main()