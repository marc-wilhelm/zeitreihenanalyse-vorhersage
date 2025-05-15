# Importiere die entsprechenden Funktionen aus jedem Modul
from Hilfsfunktionen.DatenEinlesen import DatenEinlesen
from Hilfsfunktionen.SpaltennamenKorrigieren import SpaltennamenKorrigieren
from Hilfsfunktionen.DatumFormatieren import DatumFormatieren
from Hilfsfunktionen.TemperaturUndDatumExtrahieren import TemperaturUndDatumExtrahieren
from Hilfsfunktionen.ZeitreiheAb1880 import ZeitreiheAb1880
from Hilfsfunktionen.TemperaturRunden import TemperaturRunden
from Hilfsfunktionen.NaNPruefen import NaNPruefen
from Hilfsfunktionen.DatentypenPruefen import DatentypenPruefen
from Hilfsfunktionen.DuplikatePruefen import DuplikatePruefen
from Hilfsfunktionen.BereinigteDatenSpeichern import BereinigteDatenSpeichern
#from scipy.stats import zscore
import pandas as pd

import sys
import os
import glob

# Übergeordnetes Verzeichnis hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def verarbeite_datei(input_file, output_file):
    """
    Verarbeitet eine einzelne CSV-Datei und speichert die bereinigten Daten.

    Args:
        input_file (str): Pfad zur Eingabedatei
        output_file (str): Pfad zur Ausgabedatei
    """
    print(f"\nVerarbeite Datei: {input_file}")
    print(f"Ausgabepfad: {output_file}")

    # 1. Daten einlesen
    df = DatenEinlesen(input_file, sep=";")

    if df is None:
        print(f"Fehler beim Einlesen der Daten aus {input_file}. Überspringe diese Datei.")
        return

    print("Daten erfolgreich eingelesen!")

    # 2. Spaltennamen korrigieren
    df = SpaltennamenKorrigieren(df)
    print("Spaltennamen korrigiert!")

    # 3. Datum formatieren
    df = DatumFormatieren(df)
    print("Datum formatiert!")

    # 4. Temperatur und Datum extrahieren
    df = TemperaturUndDatumExtrahieren(df)
    print("Nur Temperatur und Datum extrahiert!")

    # 5. Zeitreihe ab 1880 filtern
    df = ZeitreiheAb1880(df)
    print("Daten ab 1880 gefiltert!")

    

    # 6. NaN-Werte prüfen
    df = NaNPruefen(df)


    # 7. Datentypen prüfen
    DatentypenPruefen(df)

    # Z-Transformation
    #df['MonatlicheDurchschnittsTemperatur'] = pd.to_numeric(df['MonatlicheDurchschnittsTemperatur'], errors='coerce')
    #df['MonatlicheDurchschnittsTemperatur'] = zscore(df['MonatlicheDurchschnittsTemperatur'])

    #df['MonatlicheDurchschnittsTemperatur'] = zscore(df['MonatlicheDurchschnittsTemperatur'])




    # 8. Duplikate prüfen
    DuplikatePruefen(df)

    # 9. Daten speichern
    BereinigteDatenSpeichern(df, output_file)
    print(f"Daten erfolgreich gespeichert unter {output_file}!")


def main():
    # Basispfad ist das Verzeichnis, in dem das Skript liegt
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Pfad zum Projektverzeichnis (eine Ebene höher)
    project_dir = os.path.join(script_dir, "..")

    # Pfad zum Verzeichnis mit den originalen Daten (relativ zum Projektverzeichnis)
    original_data_dir = os.path.join(project_dir, "daten", "original-daten")

    # Pfad zum Verzeichnis für bereinigte Daten (relativ zum Projektverzeichnis)
    bereinigt_data_dir = os.path.join(project_dir, "daten", "bereinigte-daten")

    # Stelle sicher, dass das Ausgabeverzeichnis existiert
    os.makedirs(bereinigt_data_dir, exist_ok=True)

    # Suche alle CSV-Dateien im Originalverzeichnis
    csv_files = glob.glob(os.path.join(original_data_dir, "*.csv"))

    if not csv_files:
        print(f"Keine CSV-Dateien im Verzeichnis {original_data_dir} gefunden.")
        return

    print(f"Gefundene CSV-Dateien: {len(csv_files)}")

    # Verarbeite jede CSV-Datei
    for input_file in csv_files:
        # Extrahiere den Dateinamen ohne Pfad
        filename = os.path.basename(input_file)
        # Erzeuge den Ausgabepfad
        output_file = os.path.join(bereinigt_data_dir, f"bereinigt_{filename}")

        # Verarbeite die Datei
        verarbeite_datei(input_file, output_file)

    print("\nAlle Dateien wurden verarbeitet!")


if __name__ == "__main__":
    main()