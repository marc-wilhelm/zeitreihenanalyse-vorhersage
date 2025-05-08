import pandas as pd
from arch.unitroot import PhillipsPerron

def PhillipsPerronTest(data):
    """
    Führt den Phillips-Perron-Test auf den monatlichen Durchschnittstemperaturen durch.

    Parameters:
    data (pd.DataFrame): DataFrame mit den Spalten 'Datum' und 'MonatlicheDurchschnittsTemperatur'.

    Returns:
    None: Gibt die Ergebnisse des Tests aus.
    """
    data['Datum'] = pd.to_datetime(data['Datum'])
    data.set_index('Datum', inplace=True)
    
    temperature_data = data['MonatlicheDurchschnittsTemperatur'].dropna()
    
    pp_result = PhillipsPerron(temperature_data)
    print(pp_result.summary())


df = pd.read_csv("./daten/bereinigte-daten/zeitreihe_angeles_bereinigt.csv")
PhillipsPerronTest(df)
