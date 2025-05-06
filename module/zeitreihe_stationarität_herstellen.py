import sys
import os
from Hilfsfunktionen.DatenEinlesen import DatenEinlesen
from statsmodels.tsa.stattools import adfuller

# Übergeordnetes Verzeichnis damit config Modul gefunden wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config


# 1. Definiere die Eingabe- und Ausgabepfade
file_path = config.datapathzeitreiheangelesbereinigt
    # 2. Daten einlesen
df = DatenEinlesen(file_path, sep= ",")
    
if df is None:
    print("Fehler beim Einlesen der Daten. Beende das Skript.")


temp_diff = df['MonatlicheDurchschnittsTemperatur'].diff(1).dropna()

adf_result_diff = adfuller(temp_diff)
print(f'ADF Statistic: {adf_result_diff[0]}')
print(f'p-value: {adf_result_diff[1]}')
print('Critical Values:')
for key, value in adf_result_diff[4].items():
    print(f'   {key}: {value}')

#Die Ordnung der Integration ist in dieser Zeitreihe I=1

