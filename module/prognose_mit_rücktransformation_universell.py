import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import os
import sys
import importlib.util
import warnings
warnings.filterwarnings("ignore")

# === Projektverzeichnis setzen ===
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(project_root)

# === Konfig ===
cities = ["abakan", "berlin", "angeles"]
output_dir = os.path.join("results", "prognose_ergebnisse_universell")
os.makedirs(output_dir, exist_ok=True)

def load_params(city):
    param_path = os.path.join("results", "model_parameters_universell", f"gemeinsame_parameter.py")
    spec = importlib.util.spec_from_file_location("model_params", param_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.order, module.seasonal_order

def load_d(city):
    adf_path = os.path.join("results", "stationarität-ergebnisse", f"adf_result_{city}.py")
    local_vars = {}
    with open(adf_path, encoding="utf-8") as f:
        exec(f.read(), {}, local_vars)
    return local_vars.get("d", 0)

def load_D(city):
    kruskal_path = os.path.join("results", "stationarität-ergebnisse", f"kruskal_result_{city}.py")
    local_vars = {}
    with open(kruskal_path, encoding="utf-8") as f:
        exec(f.read(), {}, local_vars)
    return local_vars.get("D", 0)

def sarima_forecast(city, diff_data, original_data, order, seasonal_order, forecast_steps=10):
    print(f"\n=== SARIMA-Prognose für {city.capitalize()} ===")
    print(f"Modell: SARIMA{order}x{seasonal_order}")

    temp_series = original_data['MonatlicheDurchschnittsTemperatur']

    model = SARIMAX(diff_data, order=order, seasonal_order=seasonal_order,
                    enforce_stationarity=False, enforce_invertibility=False)
    result = model.fit(disp=False)

    forecast = result.get_forecast(steps=forecast_steps)
    mean_forecast = forecast.predicted_mean
    conf_int = forecast.conf_int(alpha=0.05)

    forecast_df = pd.DataFrame({
        'Prognose_Differenziert': mean_forecast,
        'Unteres_PI_Differenziert': conf_int.iloc[:, 0],
        'Oberes_PI_Differenziert': conf_int.iloc[:, 1],
        'Datum': pd.date_range(start=original_data['Datum'].iloc[-1], periods=forecast_steps+1, freq='MS')[1:]
    })

    # === Rücktransformation mit d, D aus stationarität-ergebnisse ===
    d_trans = load_d(city)
    D_trans = load_D(city)
    m = seasonal_order[3]

    if d_trans == 1 and D_trans == 1:
        last_value = temp_series.iloc[-1]
        season_value = temp_series.iloc[-m] if len(temp_series) > m else 0
        season_prev_value = temp_series.iloc[-m - 1] if len(temp_series) > m + 1 else 0
        absolute_forecast, lower_bound, upper_bound = [], [], []
        prev_value, prev_season, prev_season_minus1 = last_value, season_value, season_prev_value

        for i in range(forecast_steps):
            val = prev_value + prev_season - prev_season_minus1 + forecast_df.iloc[i]['Prognose_Differenziert']
            l = prev_value + prev_season - prev_season_minus1 + forecast_df.iloc[i]['Unteres_PI_Differenziert']
            u = prev_value + prev_season - prev_season_minus1 + forecast_df.iloc[i]['Oberes_PI_Differenziert']
            absolute_forecast.append(val)
            lower_bound.append(l)
            upper_bound.append(u)
            prev_season_minus1, prev_season, prev_value = prev_season, prev_value, val
    elif d_trans == 1 and D_trans == 0:
        last_value = temp_series.iloc[-1]
        absolute_forecast = last_value + np.cumsum(forecast_df['Prognose_Differenziert'].values)
        lower_bound = last_value + np.cumsum(forecast_df['Unteres_PI_Differenziert'].values)
        upper_bound = last_value + np.cumsum(forecast_df['Oberes_PI_Differenziert'].values)
    elif d_trans == 0 and D_trans == 1:
        season_values = temp_series.iloc[-m:].values if len(temp_series) >= m else np.zeros(m)
        absolute_forecast = [season_values[i % m] + val for i, val in enumerate(forecast_df['Prognose_Differenziert'])]
        lower_bound = [season_values[i % m] + val for i, val in enumerate(forecast_df['Unteres_PI_Differenziert'])]
        upper_bound = [season_values[i % m] + val for i, val in enumerate(forecast_df['Oberes_PI_Differenziert'])]
    else:
        print(f"⚠️ Warnung: Differenzierungsgrad d={d_trans}, D={D_trans} wird nicht explizit unterstützt.")
        last_value = temp_series.iloc[-1]
        absolute_forecast = last_value + np.cumsum(forecast_df['Prognose_Differenziert'].values)
        lower_bound = last_value + np.cumsum(forecast_df['Unteres_PI_Differenziert'].values)
        upper_bound = last_value + np.cumsum(forecast_df['Oberes_PI_Differenziert'].values)

    forecast_df['Absolute_Prognose'] = absolute_forecast
    forecast_df['Absolutes_Unteres_PI'] = lower_bound
    forecast_df['Absolutes_Oberes_PI'] = upper_bound

    # === Ergebnisse speichern ===
    csv_path = os.path.join(output_dir, f"prognose_werte_{city}.csv")
    forecast_df.to_csv(csv_path, index=False)
    print(f"📄 Prognose gespeichert unter: {csv_path}")

    # === Visualisierung speichern ===
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 25), temp_series.iloc[-24:].values, 'b-', label='Historische Daten')
    plt.plot(range(25, 25 + forecast_steps), forecast_df['Absolute_Prognose'], 'r-', label='Absolute Prognose')
    plt.fill_between(range(25, 25 + forecast_steps),
                     forecast_df['Absolutes_Unteres_PI'],
                     forecast_df['Absolutes_Oberes_PI'],
                     color='r', alpha=0.3, label='95% Prognoseintervall')
    plt.axvline(x=24, color='gray', linestyle='--')
    plt.title(f'SARIMA-Prognose für {city.capitalize()} (absolute Temperaturwerte)')
    plt.xlabel('Zeitperiode')
    plt.ylabel('Temperatur')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plot_path = os.path.join(output_dir, f"prognose_visualisierung_{city}.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"🖼️ Prognoseplot gespeichert unter: {plot_path}")


def main():
    print("🔄 Starte SARIMA-Prognosen für alle Städte...")

    for city in cities:
        print(f"\n🔍 Stadt: {city.capitalize()}")
        order, seasonal_order = load_params(city)

        original_path = os.path.join("daten", "bereinigte-daten", f"bereinigt_zeitreihe_{city}.csv")
        diff_path = os.path.join("daten", "stationäre-daten", f"stationaere_zeitreihe_{city}.csv")

        df_original = pd.read_csv(original_path)
        df_diff = pd.read_csv(diff_path)

        df_original['Datum'] = pd.to_datetime(df_original['Datum'])
        df_diff['Datum'] = pd.to_datetime(df_diff['Datum'])

        diff_series = df_diff['MonatlicheDurchschnittsTemperatur'].squeeze()

        sarima_forecast(city, diff_series, df_original, order, seasonal_order)

    print("\n✅ Alle Prognosen abgeschlossen.")


if __name__ == "__main__":
    main()
