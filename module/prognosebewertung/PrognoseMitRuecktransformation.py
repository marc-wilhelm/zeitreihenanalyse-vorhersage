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

# === Zentrale Konfiguration importieren ===
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

# Projektpfade initialisieren
config.init_project_paths()

def load_model_params(city):
    """Lädt die Modellparameter für eine Stadt"""
    param_path = os.path.join(config.OUTPUT_MODEL_PARAMETERS, f"{city}_params.py")
    if not os.path.exists(param_path):
        raise FileNotFoundError(f"Modellparameter für {city} nicht gefunden: {param_path}")

    spec = importlib.util.spec_from_file_location("model_params", param_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.order, module.seasonal_order

def load_stationarity_params(city):
    """Lädt die Stationaritätsparameter (d und D) für eine Stadt"""
    # Lade d-Parameter aus ADF-Ergebnissen
    adf_path = os.path.join(config.OUTPUT_STATIONARITAET, f"adf_result_{city}.py")
    d = 0
    if os.path.exists(adf_path):
        local_vars = {}
        with open(adf_path, encoding="utf-8") as f:
            exec(f.read(), {}, local_vars)
        d = local_vars.get("d", 0)

    # Lade D-Parameter aus Kruskal-Ergebnissen
    kruskal_path = os.path.join(config.OUTPUT_STATIONARITAET, f"kruskal_result_{city}.py")
    D = 0
    if os.path.exists(kruskal_path):
        local_vars = {}
        with open(kruskal_path, encoding="utf-8") as f:
            exec(f.read(), {}, local_vars)
        D = local_vars.get("D", 0)

    return d, D

def sarima_forecast_with_backtransform(city, diff_data, original_data, order, seasonal_order, d_trans, D_trans, forecast_steps=10):
    """
    Führt SARIMA-Prognose durch und transformiert die Ergebnisse zurück
    """
    print(f"\n=== SARIMA-Prognose für {city.capitalize()} ===")
    print(f"Modell: SARIMA{order}x{seasonal_order}")
    print(f"Differenzierungsgrad: d={d_trans}, D={D_trans}")

    # Temperatur-Serie aus den Originaldaten
    temp_series = original_data['MonatlicheDurchschnittsTemperatur']

    # SARIMA-Modell anpassen
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

    # === Rücktransformation basierend auf d und D ===
    m = seasonal_order[3] if seasonal_order[3] > 0 else 12  # Saisonale Periode

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
        print(f"⚠️ Warnung: Differenzierungsgrad d={d_trans}, D={D_trans} - verwende direkte Prognose")
        if d_trans == 0 and D_trans == 0:
            # Direkte Prognose ohne Rücktransformation
            absolute_forecast = forecast_df['Prognose_Differenziert'].values
            lower_bound = forecast_df['Unteres_PI_Differenziert'].values
            upper_bound = forecast_df['Oberes_PI_Differenziert'].values
        else:
            # Fallback: Einfache kumulative Summierung
            last_value = temp_series.iloc[-1]
            absolute_forecast = last_value + np.cumsum(forecast_df['Prognose_Differenziert'].values)
            lower_bound = last_value + np.cumsum(forecast_df['Unteres_PI_Differenziert'].values)
            upper_bound = last_value + np.cumsum(forecast_df['Oberes_PI_Differenziert'].values)

    # Absolute Werte zum DataFrame hinzufügen
    forecast_df['Absolute_Prognose'] = absolute_forecast
    forecast_df['Absolutes_Unteres_PI'] = lower_bound
    forecast_df['Absolutes_Oberes_PI'] = upper_bound

    return forecast_df

def create_forecast_plot(city, original_data, forecast_df, forecast_steps=10):
    """Erstellt und speichert eine Prognose-Visualisierung"""
    temp_series = original_data['MonatlicheDurchschnittsTemperatur']

    plt.figure(figsize=(12, 8))

    # Historische Daten (letzte 24 Monate)
    historical_periods = min(24, len(temp_series))
    plt.plot(range(1, historical_periods + 1),
             temp_series.iloc[-historical_periods:].values,
             'b-', label='Historische Daten', linewidth=2)

    # Prognose
    plt.plot(range(historical_periods + 1, historical_periods + 1 + forecast_steps),
             forecast_df['Absolute_Prognose'],
             'r-', label='Prognose', linewidth=2)

    # Prognoseintervall
    plt.fill_between(range(historical_periods + 1, historical_periods + 1 + forecast_steps),
                     forecast_df['Absolutes_Unteres_PI'],
                     forecast_df['Absolutes_Oberes_PI'],
                     color='red', alpha=0.3, label='95% Prognoseintervall')

    # Trennlinie zwischen historischen Daten und Prognose
    plt.axvline(x=historical_periods + 0.5, color='gray', linestyle='--', alpha=0.7)

    # Beschriftung und Layout
    plt.title(f'SARIMA-Temperaturprognose für {city.capitalize()}', fontsize=16, fontweight='bold')
    plt.xlabel('Zeitperiode (Monate)', fontsize=12)
    plt.ylabel('Temperatur (°C)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Speichern
    output_dir = os.path.join(config.OUTPUT_FOLDER, "prognose_ergebnisse")
    os.makedirs(output_dir, exist_ok=True)
    plot_path = os.path.join(output_dir, f"prognose_visualisierung_{city}.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()

    return plot_path

def run_forecast_for_city(city, forecast_steps=10):
    """
    Führt eine komplette Prognose für eine Stadt durch

    Parameters:
    - city: str - Name der Stadt
    - forecast_steps: int - Anzahl der Prognosemonate

    Returns:
    - bool - True bei Erfolg, False bei Fehler
    """
    try:
        # Modellparameter laden
        order, seasonal_order = load_model_params(city)

        # Stationaritätsparameter laden
        d_trans, D_trans = load_stationarity_params(city)

        # Daten laden
        original_path = config.CITY_PATHS_CLEAN[city]
        stationary_path = config.get_stationary_data_path(city)

        if not os.path.exists(original_path):
            raise FileNotFoundError(f"Bereinigte Daten für {city} nicht gefunden: {original_path}")
        if not os.path.exists(stationary_path):
            raise FileNotFoundError(f"Stationäre Daten für {city} nicht gefunden: {stationary_path}")

        # Daten einlesen
        df_original = pd.read_csv(original_path)
        df_stationary = pd.read_csv(stationary_path)

        # Datum zu datetime konvertieren
        df_original['Datum'] = pd.to_datetime(df_original['Datum'])
        df_stationary['Datum'] = pd.to_datetime(df_stationary['Datum'])

        # Stationäre Zeitreihe extrahieren
        stationary_series = df_stationary['MonatlicheDurchschnittsTemperatur'].squeeze()

        # SARIMA-Prognose mit Rücktransformation
        forecast_df = sarima_forecast_with_backtransform(
            city, stationary_series, df_original, order, seasonal_order,
            d_trans, D_trans, forecast_steps
        )

        # Ergebnisse speichern
        output_dir = os.path.join(config.OUTPUT_FOLDER, "prognose_ergebnisse")
        os.makedirs(output_dir, exist_ok=True)

        csv_path = os.path.join(output_dir, f"prognose_werte_{city}.csv")
        forecast_df.to_csv(csv_path, index=False)
        print(f"   📄 Prognose gespeichert: {csv_path}")

        # Visualisierung erstellen
        plot_path = create_forecast_plot(city, df_original, forecast_df, forecast_steps)
        print(f"   🖼️ Plot gespeichert: {plot_path}")

        # Kurze Zusammenfassung der Prognose
        print(f"   📊 Prognosewerte für nächste {forecast_steps} Monate:")
        print(f"      Durchschnitt: {forecast_df['Absolute_Prognose'].mean():.2f}°C")
        print(f"      Min: {forecast_df['Absolute_Prognose'].min():.2f}°C")
        print(f"      Max: {forecast_df['Absolute_Prognose'].max():.2f}°C")

        return True

    except Exception as e:
        print(f"   ❌ Fehler bei Prognose für {city}: {e}")
        return False

def main():
    """
    Hauptfunktion für Prognose mit Rücktransformation
    """
    start_time = time.time()

    print("🔄 Starte SARIMA-Prognosen für alle Städte...")

    # Ausgabeordner erstellen
    output_dir = os.path.join(config.OUTPUT_FOLDER, "prognose_ergebnisse")
    os.makedirs(output_dir, exist_ok=True)

    successful_forecasts = 0
    failed_forecasts = []

    # Prognosen für alle Städte erstellen
    for city in config.CITIES:
        print(f"\n🔍 Stadt: {city.capitalize()}")
        success = run_forecast_for_city(city, forecast_steps=10)
        if success:
            successful_forecasts += 1
        else:
            failed_forecasts.append(city)

    # Detaillierte Zusammenfassung
    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "="*80)
    print("🎯 PROGNOSEPIPELINE ABGESCHLOSSEN! 🎯")
    print(f"⏱️ Gesamtdauer: {duration:.2f} Sekunden")
    print(f"✅ Erfolgreiche Prognosen: {successful_forecasts}/{len(config.CITIES)}")

    if failed_forecasts:
        print(f"❌ Fehlgeschlagene Prognosen: {failed_forecasts}")

    print(f"\n📁 Alle Prognoseergebnisse in: {output_dir}")

    # Zeige tatsächlich erstellte Dateien
    print("📋 Erstellte Dateien:")
    if os.path.exists(output_dir) and os.listdir(output_dir):
        created_files = sorted(os.listdir(output_dir))
        csv_files = [f for f in created_files if f.endswith('.csv')]
        png_files = [f for f in created_files if f.endswith('.png')]

        if csv_files:
            print("   📊 Prognosewerte:")
            for file in csv_files:
                print(f"      • {file}")

        if png_files:
            print("   📈 Visualisierungen:")
            for file in png_files:
                print(f"      • {file}")
    else:
        print("   ⚠️ Noch keine Dateien erstellt")

    print("="*80)
    print("✅ Alle Prognosen abgeschlossen.")

if __name__ == "__main__":
    main()