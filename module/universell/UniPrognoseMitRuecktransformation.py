import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import os
import sys
import time
import importlib.util
import warnings
warnings.filterwarnings("ignore")

# === Projektstruktur einbinden ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

def load_params(city):
    """Lädt die universellen Modellparameter"""
    param_path = os.path.join(config.OUTPUT_MODEL_PARAMETERS_UNIVERSELL, "gemeinsame_parameter.py")
    if not os.path.exists(param_path):
        raise FileNotFoundError(f"Universelle Parameter nicht gefunden: {param_path}")

    spec = importlib.util.spec_from_file_location("model_params", param_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.order, module.seasonal_order

def load_d(city):
    """Lädt den d-Parameter aus den ADF-Ergebnissen"""
    adf_path = os.path.join(config.OUTPUT_STATIONARITAET, f"adf_result_{city}.py")
    local_vars = {}
    with open(adf_path, encoding="utf-8") as f:
        exec(f.read(), {}, local_vars)
    return local_vars.get("d", 0)

def load_D(city):
    """Lädt den D-Parameter aus den Kruskal-Ergebnissen"""
    kruskal_path = os.path.join(config.OUTPUT_STATIONARITAET, f"kruskal_result_{city}.py")
    local_vars = {}
    with open(kruskal_path, encoding="utf-8") as f:
        exec(f.read(), {}, local_vars)
    return local_vars.get("D", 0)

def sarima_forecast(city, diff_data, original_data, order, seasonal_order, forecast_steps=10):
    """Führt SARIMA-Prognose mit universellen Parametern durch und transformiert zurück"""
    print(f"\n=== SARIMA-Prognose für {city.capitalize()} ===")
    print(f"Modell: SARIMA{order}x{seasonal_order}")

    temp_series = original_data['MonatlicheDurchschnittsTemperatur']

    # SARIMA-Modell mit universellen Parametern anpassen
    model = SARIMAX(diff_data, order=order, seasonal_order=seasonal_order,
                    enforce_stationarity=False, enforce_invertibility=False)
    result = model.fit(disp=False)

    # Prognose erstellen
    forecast = result.get_forecast(steps=forecast_steps)
    mean_forecast = forecast.predicted_mean
    conf_int = forecast.conf_int(alpha=0.05)

    # DataFrame für differenzierte Prognose
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

    print(f"Differenzierungsgrad: d={d_trans}, D={D_trans}")

    if d_trans == 1 and D_trans == 1:
        # Doppelte Differenzierung rücktransformieren
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
        # Nur erste Differenz rücktransformieren
        last_value = temp_series.iloc[-1]
        absolute_forecast = last_value + np.cumsum(forecast_df['Prognose_Differenziert'].values)
        lower_bound = last_value + np.cumsum(forecast_df['Unteres_PI_Differenziert'].values)
        upper_bound = last_value + np.cumsum(forecast_df['Oberes_PI_Differenziert'].values)

    elif d_trans == 0 and D_trans == 1:
        # Nur saisonale Differenz rücktransformieren
        season_values = temp_series.iloc[-m:].values if len(temp_series) >= m else np.zeros(m)
        absolute_forecast = [season_values[i % m] + val for i, val in enumerate(forecast_df['Prognose_Differenziert'])]
        lower_bound = [season_values[i % m] + val for i, val in enumerate(forecast_df['Unteres_PI_Differenziert'])]
        upper_bound = [season_values[i % m] + val for i, val in enumerate(forecast_df['Oberes_PI_Differenziert'])]

    else:
        # Keine Rücktransformation nötig oder unbekannte Kombination
        print(f"⚠️ Warnung: Differenzierungsgrad d={d_trans}, D={D_trans} wird nicht explizit unterstützt.")
        last_value = temp_series.iloc[-1]
        absolute_forecast = last_value + np.cumsum(forecast_df['Prognose_Differenziert'].values)
        lower_bound = last_value + np.cumsum(forecast_df['Unteres_PI_Differenziert'].values)
        upper_bound = last_value + np.cumsum(forecast_df['Oberes_PI_Differenziert'].values)

    # Absolute Werte zum DataFrame hinzufügen
    forecast_df['Absolute_Prognose'] = absolute_forecast
    forecast_df['Absolutes_Unteres_PI'] = lower_bound
    forecast_df['Absolutes_Oberes_PI'] = upper_bound

    # === Ergebnisse speichern ===
    os.makedirs(config.OUTPUT_PROGNOSE_ERGEBNISSE_UNIVERSELL, exist_ok=True)

    csv_path = os.path.join(config.OUTPUT_PROGNOSE_ERGEBNISSE_UNIVERSELL, f"prognose_werte_{city}.csv")
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
    plt.title(f'Universelle SARIMA-Prognose für {city.capitalize()} (absolute Temperaturwerte)')
    plt.xlabel('Zeitperiode')
    plt.ylabel('Temperatur')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plot_path = os.path.join(config.OUTPUT_PROGNOSE_ERGEBNISSE_UNIVERSELL, f"prognose_visualisierung_{city}.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"🖼️ Prognoseplot gespeichert unter: {plot_path}")

    return forecast_df


def main():
    """Hauptfunktion für universelle SARIMA-Prognose mit Rücktransformation"""
    start_time = time.time()

    print("🔄 Starte universelle SARIMA-Prognosen für alle Städte...")

    # Ausgabeordner erstellen
    config.ensure_output_dirs()

    # Liste der Städte
    cities = config.CITIES

    successful_forecasts = 0
    failed_forecasts = []

    for city in cities:
        print(f"\n🔍 Stadt: {city.capitalize()}")

        try:
            # Modellparameter laden
            order, seasonal_order = load_params(city)

            # Daten laden
            original_path = config.CITY_PATHS_CLEAN[city]
            diff_path = config.get_stationary_data_path(city)

            if not os.path.exists(original_path):
                raise FileNotFoundError(f"Bereinigte Daten nicht gefunden: {original_path}")
            if not os.path.exists(diff_path):
                raise FileNotFoundError(f"Stationäre Daten nicht gefunden: {diff_path}")

            df_original = pd.read_csv(original_path)
            df_diff = pd.read_csv(diff_path)

            df_original['Datum'] = pd.to_datetime(df_original['Datum'])
            df_diff['Datum'] = pd.to_datetime(df_diff['Datum'])

            diff_series = df_diff['MonatlicheDurchschnittsTemperatur'].squeeze()

            # SARIMA-Prognose durchführen
            forecast_df = sarima_forecast(city, diff_series, df_original, order, seasonal_order)

            # Kurze Zusammenfassung ausgeben
            print(f"📊 Prognosezusammenfassung für {city}:")
            print(f"   Durchschnitt: {forecast_df['Absolute_Prognose'].mean():.2f}°C")
            print(f"   Min: {forecast_df['Absolute_Prognose'].min():.2f}°C")
            print(f"   Max: {forecast_df['Absolute_Prognose'].max():.2f}°C")

            successful_forecasts += 1

        except Exception as e:
            print(f"❌ Fehler bei {city}: {e}")
            failed_forecasts.append(city)
            continue

    # Zusammenfassung
    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "="*60)
    print("📋 ZUSAMMENFASSUNG - UNIVERSELLE SARIMA-PROGNOSEN")
    print("="*60)
    print(f"⏱️ Gesamtdauer: {duration:.2f} Sekunden")
    print(f"✅ Erfolgreiche Prognosen: {successful_forecasts}/{len(cities)}")

    if failed_forecasts:
        print(f"❌ Fehlgeschlagene Prognosen: {', '.join(failed_forecasts)}")

    print(f"\n📁 Alle Prognoseergebnisse in: {config.OUTPUT_PROGNOSE_ERGEBNISSE_UNIVERSELL}")
    print("="*60)
    print("\n✅ Alle Prognosen abgeschlossen.")


if __name__ == "__main__":
    main()