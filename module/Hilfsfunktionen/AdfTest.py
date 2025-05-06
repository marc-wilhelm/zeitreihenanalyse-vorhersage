import pandas as pd
from statsmodels.tsa.stattools import adfuller

def AdfTest(data):
    """
    Führt den Augmented Dickey-Fuller (ADF) Test auf den monatlichen Durchschnittstemperaturen durch.
    
    Parameters:
    data (pd.DataFrame): DataFrame mit den Spalten 'Datum' und 'MonatlicheDurchschnittsTemperatur'.
    
    Returns:
    None: Gibt die Ergebnisse des ADF-Tests aus.
    """
    # Stelle sicher, dass 'Datum' als Datetime-Objekt interpretiert wird
    data['Datum'] = pd.to_datetime(data['Datum'])
    
    # Setze 'Datum' als Index, falls das noch nicht erfolgt ist
    data.set_index('Datum', inplace=True)
    
    # Extrahiere die Temperaturdaten
    temperature_data = data['MonatlicheDurchschnittsTemperatur']
    
    # Führe den ADF-Test auf den Originaldaten durch
    adf_result = adfuller(temperature_data)
    
    print(f"ADF-Test auf den Originaldaten:")
    print(f'ADF Statistic: {adf_result[0]}')
    print(f'p-value: {adf_result[1]}')
    print('Critical Values:')
    for key, value in adf_result[4].items():
        print(f'   {key}: {value}')