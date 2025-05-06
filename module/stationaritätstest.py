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
    # 1. Definiere die Eingabe- und Ausgabepfade
    file_path = config.datapathzeitreiheangelesbereinigt  # Pfad zu den bereinigten Daten


    # 2. Daten einlesen
    df = DatenEinlesen(file_path, sep=",")  # Daten einlesen, separat durch Semikolon
    if df is None:
        print("Fehler beim Einlesen der Daten. Beende das Skript.")
        return

    print("Daten erfolgreich eingelesen!")

    # 3. ADF-Test durchführen
    AdfTest(df)  

    # 4. CUSUM-Test durchführen
    cusum_test(df)  

if __name__ == "__main__":
    main()