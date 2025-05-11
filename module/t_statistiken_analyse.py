"""
Berechnung der t-Statistiken für ARIMA und SARIMA Modelle mit automatischem Import der optimalen Parameter
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import sys
import os
import warnings
warnings.filterwarnings("ignore")

# Projektkonfiguration laden
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Importiere die berechneten SARIMA-Parameter aus dem parameter-Ordner
try:
    from parameter.sarima_params_angeles import order as angeles_order, seasonal_order as angeles_seasonal_order
    from parameter.sarima_params_abakan import order as abakan_order, seasonal_order as abakan_seasonal_order
    from parameter.sarima_params_berlin import order as berlin_order, seasonal_order as berlin_seasonal_order
    print("SARIMA-Parameter für alle Städte erfolgreich geladen")
except ImportError as e:
    print(f"Fehler beim Laden der SARIMA-Parameter: {e}")
    print("Stelle sicher, dass alle Parameter-Dateien vorhanden sind.")
    sys.exit(1)

def analyse_arima_koeffizienten(ts_data, city_name, order):
    """
    Berechnet die t-Statistiken für die Koeffizienten eines ARIMA-Modells
    """
    print(f"\n=== ARIMA Koeffizientenanalyse für {city_name} ===")
    print(f"Modell: ARIMA{order}")

    # ARIMA-Modell fitten
    model = ARIMA(ts_data, order=order)
    result = model.fit()

    # Statistiken extrahieren
    coefficients = result.params
    standard_errors = result.bse
    t_values = result.tvalues
    p_values = result.pvalues

    # DataFrame erstellen und ausgeben
    stats_df = pd.DataFrame({
        'Koeffizient': coefficients,
        'Std. Fehler': standard_errors,
        't-Wert': t_values,
        'p-Wert': p_values,
        'Signifikant (p<0.05)': p_values < 0.05
    })

    print("\nKoeffizientenstatistiken:")
    print(stats_df)

    return stats_df

def analyse_sarima_koeffizienten(ts_data, city_name, order, seasonal_order):
    """
    Berechnet die t-Statistiken für die Koeffizienten eines SARIMA-Modells
    """
    print(f"\n=== SARIMA Koeffizientenanalyse für {city_name} ===")
    print(f"Modell: SARIMA{order}x{seasonal_order}")

    # SARIMA-Modell fitten
    model = SARIMAX(
        ts_data,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    result = model.fit(disp=False, low_memory=True)

    # Statistiken extrahieren
    coefficients = result.params
    standard_errors = result.bse
    t_values = result.tvalues
    p_values = result.pvalues

    # DataFrame erstellen und ausgeben
    stats_df = pd.DataFrame({
        'Koeffizient': coefficients,
        'Std. Fehler': standard_errors,
        't-Wert': t_values,
        'p-Wert': p_values,
        'Signifikant (p<0.05)': p_values < 0.05
    })

    print("\nKoeffizientenstatistiken:")
    print(stats_df)

    return stats_df

def main():
    """Hauptfunktion zur Berechnung der t-Statistiken für alle Städte"""

    # Analysiere Angeles
    print("\nBerechne t-Statistiken für Angeles...")
    ts_data = config.seasonal_diff_angeles.squeeze()

    # ARIMA-Koeffizienten (verwende p und q aus SARIMA, da wir keine gespeicherten ARIMA-Parameter haben)
    arima_order = (angeles_order[0], angeles_order[1], angeles_order[2])
    analyse_arima_koeffizienten(ts_data, "Angeles", arima_order)

    # SARIMA-Koeffizienten (verwende die gespeicherten Parameter)
    analyse_sarima_koeffizienten(ts_data, "Angeles", angeles_order, angeles_seasonal_order)

    # Analysiere Abakan
    print("\nBerechne t-Statistiken für Abakan...")
    ts_data = config.seasonal_diff_abakan.squeeze()

    # ARIMA-Koeffizienten
    arima_order = (abakan_order[0], abakan_order[1], abakan_order[2])
    analyse_arima_koeffizienten(ts_data, "Abakan", arima_order)

    # SARIMA-Koeffizienten
    analyse_sarima_koeffizienten(ts_data, "Abakan", abakan_order, abakan_seasonal_order)

    # Analysiere Berlin
    print("\nBerechne t-Statistiken für Berlin...")
    ts_data = config.seasonal_diff_berlin.squeeze()

    # ARIMA-Koeffizienten
    arima_order = (berlin_order[0], berlin_order[1], berlin_order[2])
    analyse_arima_koeffizienten(ts_data, "Berlin", arima_order)

    # SARIMA-Koeffizienten
    analyse_sarima_koeffizienten(ts_data, "Berlin", berlin_order, berlin_seasonal_order)

if __name__ == "__main__":
    main()