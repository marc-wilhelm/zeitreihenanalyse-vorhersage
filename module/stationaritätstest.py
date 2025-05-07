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

# Das Working Directory zum Projektverzeichnis ändern
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def verarbeite_datei(file_path):
    """
    Führt die Analyse für eine bestimmte Datei durch.
    """
    print(f"\nVerarbeite Datei: {file_path}")

    # 2. Daten einlesen
    df = DatenEinlesen(file_path, sep=",")  # Daten einlesen, separiert durch Komma
    if df is None:
        print(f"Fehler beim Einlesen der Daten aus {file_path}. Überspringe diese Datei.")
        return

    print("Daten erfolgreich eingelesen!")
    print(f"Spalten in DataFrame: {df.columns.tolist()}")  # Zur Überprüfung der verfügbaren Spalten

    # 3. ADF-Test durchführen
    df_adf = df.copy()
    AdfTest(df_adf)

    # 4. CUSUM-Test durchführen
    cusum_test(df, target_column='MonatlicheDurchschnittsTemperatur', date_column='Datum')

def main():
    # Liste der bereinigten Datensätze aus der config.py
    dateipfade = [
        config.PATH_TS_BERLIN_CLEAN,
        config.PATH_TS_ANGELES_CLEAN,
        config.PATH_TS_ABAKAN_CLEAN
    ]

    # Aktuelles Arbeitsverzeichnis zur Überprüfung ausgeben
    print(f"Aktuelles Arbeitsverzeichnis: {os.getcwd()}")

    # Verarbeite alle angegebenen Dateien nacheinander
    for file_path in dateipfade:
        verarbeite_datei(file_path)

    print("\nAlle Dateien wurden verarbeitet!")

if __name__ == "__main__":
    main()