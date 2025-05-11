"""
Einfache und korrekte SARIMA-Prognose mit Konfidenzintervallen für die nächsten zehn Perioden (Aufgabe 7)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import os
import sys
import warnings
warnings.filterwarnings("ignore")

# Projektkonfiguration laden
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Parameter importieren
try:
    from parameter.sarima_params_angeles import order as angeles_order, seasonal_order as angeles_seasonal_order
    from parameter.sarima_params_abakan import order as abakan_order, seasonal_order as abakan_seasonal_order
    from parameter.sarima_params_berlin import order as berlin_order, seasonal_order as berlin_seasonal_order
    print("SARIMA-Parameter für alle Städte erfolgreich geladen")
except ImportError as e:
    print(f"Fehler beim Laden der SARIMA-Parameter: {e}")
    sys.exit(1)

# Ausgabeverzeichnis erstellen
output_dir = "./ergebnisse/prognosen"
os.makedirs(output_dir, exist_ok=True)

def sarima_forecast(city_name, diff_data, original_data, order, seasonal_order, forecast_steps=10):
    """
    Erstellt eine SARIMA-Prognose mit Konfidenzintervallen und korrekte Rücktransformation

    Parameters:
    -----------
    city_name : str
        Name der Stadt
    diff_data : pandas.Series
        Differenzierte Daten für SARIMA-Modell
    original_data : pandas.DataFrame
        Originaldaten mit Temperaturwerten
    order : tuple
        (p, d, q) - SARIMA-Parameter für nicht-saisonale Komponente
    seasonal_order : tuple
        (P, D, Q, m) - SARIMA-Parameter für saisonale Komponente
    forecast_steps : int
        Anzahl der Prognoseperioden
    """
    print(f"\n=== SARIMA-Prognose für {city_name} ===")
    print(f"Modell: SARIMA{order}x{seasonal_order}")

    # Extrahiere die Originaldaten
    temp_series = original_data['MonatlicheDurchschnittsTemperatur']

    # SARIMA-Modell fitten
    model = SARIMAX(
        diff_data,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    result = model.fit(disp=False)

    # Prognose für differenzierte Daten
    forecast = result.get_forecast(steps=forecast_steps)
    mean_forecast = forecast.predicted_mean
    conf_int = forecast.conf_int(alpha=0.05)

    # Speichere die Ergebnisse
    forecast_df = pd.DataFrame({
        'Prognose_Differenziert': mean_forecast,
        'Untere_KI_Differenziert': conf_int.iloc[:, 0],
        'Obere_KI_Differenziert': conf_int.iloc[:, 1]
    })

    # Rücktransformation gemäß dem SARIMA-Modell
    d = order[1]          # Nicht-saisonale Differenzierungsordnung
    D = seasonal_order[1] # Saisonale Differenzierungsordnung
    m = seasonal_order[3] # Saisonale Periodizität (12 für Monate)

    # Berechne absolute Temperaturwerte basierend auf Differenzierungsmethode
    # und setze Datum fort
    dates = pd.date_range(start=original_data['Datum'].iloc[-1], periods=forecast_steps+1, freq='MS')[1:]
    forecast_df['Datum'] = dates

    # Wir benötigen die letzten Werte als Basis für die Rücktransformation
    if d == 1 and D == 1:
        # Saisonale und reguläre Differenzierung
        # Benötigt: letzten Wert, Wert von vor 12 Monaten, und Wert von vor 13 Monaten
        last_value = temp_series.iloc[-1]
        season_value = temp_series.iloc[-m] if len(temp_series) > m else 0
        season_prev_value = temp_series.iloc[-m-1] if len(temp_series) > m+1 else 0

        # Erstelle Speicher für rücktransformierte Werte
        absolute_forecast = np.zeros(forecast_steps)
        lower_bound = np.zeros(forecast_steps)
        upper_bound = np.zeros(forecast_steps)

        # Initialisiere mit dem ersten Wert
        prev_value = last_value
        prev_season = season_value
        prev_season_minus1 = season_prev_value

        for i in range(forecast_steps):
            # Formel: y_t = y_{t-1} + y_{t-m} - y_{t-m-1} + Δ²_m y_t
            prediction = prev_value + prev_season - prev_season_minus1 + forecast_df['Prognose_Differenziert'].iloc[i]
            lower = prev_value + prev_season - prev_season_minus1 + forecast_df['Untere_KI_Differenziert'].iloc[i]
            upper = prev_value + prev_season - prev_season_minus1 + forecast_df['Obere_KI_Differenziert'].iloc[i]

            absolute_forecast[i] = prediction
            lower_bound[i] = lower
            upper_bound[i] = upper

            # Aktualisiere für den nächsten Schritt
            prev_season_minus1 = prev_season
            prev_season = prev_value
            prev_value = prediction

    elif d == 0 and D == 1:
        # Nur saisonale Differenzierung
        # Hole die letzten m Werte als Basis
        season_values = temp_series.iloc[-m:].values if len(temp_series) >= m else np.zeros(m)

        absolute_forecast = np.zeros(forecast_steps)
        lower_bound = np.zeros(forecast_steps)
        upper_bound = np.zeros(forecast_steps)

        for i in range(forecast_steps):
            season_idx = i % m
            absolute_forecast[i] = season_values[season_idx] + forecast_df['Prognose_Differenziert'].iloc[i]
            lower_bound[i] = season_values[season_idx] + forecast_df['Untere_KI_Differenziert'].iloc[i]
            upper_bound[i] = season_values[season_idx] + forecast_df['Obere_KI_Differenziert'].iloc[i]

    elif d == 1 and D == 0:
        # Nur reguläre Differenzierung
        last_value = temp_series.iloc[-1]

        # Kumulative Summe + letzter Wert
        absolute_forecast = last_value + np.cumsum(forecast_df['Prognose_Differenziert'].values)
        lower_bound = last_value + np.cumsum(forecast_df['Untere_KI_Differenziert'].values)
        upper_bound = last_value + np.cumsum(forecast_df['Obere_KI_Differenziert'].values)

    else:
        # Fallback für andere Fälle
        print(f"Warnung: Differenzierungsgrad (d={d}, D={D}) wird nicht direkt unterstützt.")
        last_value = temp_series.iloc[-1]
        absolute_forecast = last_value + np.cumsum(forecast_df['Prognose_Differenziert'].values)
        lower_bound = last_value + np.cumsum(forecast_df['Untere_KI_Differenziert'].values)
        upper_bound = last_value + np.cumsum(forecast_df['Obere_KI_Differenziert'].values)

    # Speichere die rücktransformierten Werte
    forecast_df['Absolute_Prognose'] = absolute_forecast
    forecast_df['Absolute_Untere_KI'] = lower_bound
    forecast_df['Absolute_Obere_KI'] = upper_bound

    # Ausgabe der Ergebnisse
    print("\nPrognosen für die nächsten 10 Perioden (differenzierte Werte):")
    print(forecast_df[['Datum', 'Prognose_Differenziert', 'Untere_KI_Differenziert', 'Obere_KI_Differenziert']])

    print("\nPrognosen für die nächsten 10 Perioden (absolute Temperaturwerte):")
    print(forecast_df[['Datum', 'Absolute_Prognose', 'Absolute_Untere_KI', 'Absolute_Obere_KI']])

    # Speichere Ergebnisse
    forecast_file = os.path.join(output_dir, f"sarima_{city_name.lower()}_prognose.csv")
    forecast_df.to_csv(forecast_file, index=False)

    # Erstelle Plots
    # Plot für differenzierte Werte
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 25), diff_data.iloc[-24:].values, 'b-', label='Historische Daten')
    plt.plot(range(25, 25 + forecast_steps), forecast_df['Prognose_Differenziert'].values, 'r-', label='Prognose')
    plt.fill_between(
        range(25, 25 + forecast_steps),
        forecast_df['Untere_KI_Differenziert'],
        forecast_df['Obere_KI_Differenziert'],
        color='r', alpha=0.2,
        label='95% Konfidenzintervall'
    )
    plt.axvline(x=24, color='gray', linestyle='--')
    plt.title(f'SARIMA-Prognose für {city_name} (differenzierte Werte)')
    plt.xlabel('Zeitperiode')
    plt.ylabel('Differenzierter Wert')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_dir, f"sarima_{city_name.lower()}_diff.png"))
    plt.close()

    # Plot für absolute Werte
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 25), temp_series.iloc[-24:].values, 'b-', label='Historische Daten')
    plt.plot(range(25, 25 + forecast_steps), forecast_df['Absolute_Prognose'].values, 'r-', label='Absolute Prognose')
    plt.fill_between(
        range(25, 25 + forecast_steps),
        forecast_df['Absolute_Untere_KI'],
        forecast_df['Absolute_Obere_KI'],
        color='r', alpha=0.2,
        label='95% Konfidenzintervall'
    )
    plt.axvline(x=24, color='gray', linestyle='--')
    plt.title(f'SARIMA-Prognose für {city_name} (absolute Temperaturwerte)')
    plt.xlabel('Zeitperiode')
    plt.ylabel('Temperatur')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_dir, f"sarima_{city_name.lower()}_abs.png"))
    plt.close()

    return forecast_df

def main():
    """Hauptfunktion für die SARIMA-Prognosen"""
    print("Berechne SARIMA-Prognosen mit Konfidenzintervallen...\n")

    # Angeles
    print("\nAnalyse für Angeles:")
    diff_angeles = config.seasonal_diff_angeles.squeeze()
    sarima_forecast("Angeles", diff_angeles, config.df_angeles,
                    angeles_order, angeles_seasonal_order)

    # Abakan
    print("\nAnalyse für Abakan:")
    diff_abakan = config.seasonal_diff_abakan.squeeze()
    sarima_forecast("Abakan", diff_abakan, config.df_abakan,
                    abakan_order, abakan_seasonal_order)

    # Berlin
    print("\nAnalyse für Berlin:")
    diff_berlin = config.seasonal_diff_berlin.squeeze()
    sarima_forecast("Berlin", diff_berlin, config.df_berlin,
                    berlin_order, berlin_seasonal_order)

    print("\nAlle SARIMA-Prognosen wurden erstellt und gespeichert.")

if __name__ == "__main__":
    main()