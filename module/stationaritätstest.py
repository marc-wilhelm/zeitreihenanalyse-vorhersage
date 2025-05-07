# Importiere die entsprechenden Funktionen aus jedem Modul
from Hilfsfunktionen.DatenEinlesen import DatenEinlesen
from Hilfsfunktionen.CusumTest import cusum_test  
from Hilfsfunktionen.AdfTest import AdfTest
import sys
import os

# Übergeordnetes Verzeichnis hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Jetzt sollte config importiert werden können
import config

def main():
    # 1. Definiere die Eingabepfade
    file_path = config.datapathzeitreiheberlinbereinigt  # Pfad zu den bereinigten Daten
    
    # 2. Daten einlesen
    df = DatenEinlesen(file_path, sep=",")  # Daten einlesen, separiert durch Komma
    if df is None:
        print("Fehler beim Einlesen der Daten. Beende das Skript.")
        return
    
    print("Daten erfolgreich eingelesen!")
    print(f"Spalten in DataFrame: {df.columns.tolist()}")  # Zur Überprüfung der verfügbaren Spalten
    
    # 3. ADF-Test durchführen
    # Erstelle eine Kopie des DataFrames, damit der AdfTest den Index nicht permanent ändert
    df_adf = df.copy()
    AdfTest(df_adf)
    
    # 4. CUSUM-Test durchführen
    
    cusum_test(df, target_column='MonatlicheDurchschnittsTemperatur', date_column='Datum')



if __name__ == "__main__":
    main()

#Daten sind bereits stationär, Integrationsstufe ist 0 