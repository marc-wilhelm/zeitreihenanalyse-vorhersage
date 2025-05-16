# module/datenbereinigung/pipeline_datenvorbereitung.py

import os
import glob
from . import (
    DatenEinlesen,
    SpaltennamenKorrigieren,
    DatumFormatieren,
    TemperaturUndDatumExtrahieren,
    ZeitreiheAb1880,
    NaNPruefen,
    DatentypenPruefen,
    DuplikatePruefen,
    BereinigteDatenSpeichern
)

class DatenvorbereitungsPipeline:
    def __init__(self):
        pass

    def verarbeite_datei(self, input_file, output_file, sep=";", decimal=","):
        """
        Verarbeitet eine einzelne CSV-Datei und speichert die bereinigten Daten.

        Args:
            input_file (str): Pfad zur Eingabedatei
            output_file (str): Pfad zur Ausgabedatei
            sep (str): Separator für CSV
            decimal (str): Dezimaltrennzeichen
        """
        print(f"\nVerarbeite Datei: {input_file}")
        print(f"Ausgabepfad: {output_file}")

        # 1. Daten einlesen
        df = DatenEinlesen(input_file, sep=sep, decimal=decimal)

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

        # 8. Duplikate prüfen
        DuplikatePruefen(df)

        # 9. Daten speichern
        BereinigteDatenSpeichern(df, output_file)
        print(f"Daten erfolgreich gespeichert unter {output_file}!")

        return df

    def verarbeite_alle_dateien(self, original_dir, output_dir):
        """
        Verarbeitet alle CSV-Dateien in einem Verzeichnis.

        Args:
            original_dir (str): Pfad zum Verzeichnis mit Originaldaten
            output_dir (str): Pfad zum Ausgabeverzeichnis
        """
        # Stelle sicher, dass das Ausgabeverzeichnis existiert
        os.makedirs(output_dir, exist_ok=True)

        # Suche alle CSV-Dateien
        csv_files = glob.glob(os.path.join(original_dir, "*.csv"))

        if not csv_files:
            print(f"Keine CSV-Dateien im Verzeichnis {original_dir} gefunden.")
            return

        print(f"Gefundene CSV-Dateien: {len(csv_files)}")

        # Verarbeite jede CSV-Datei
        for input_file in csv_files:
            filename = os.path.basename(input_file)
            output_file = os.path.join(output_dir, f"bereinigt_{filename}")
            self.verarbeite_datei(input_file, output_file)

        print("\nAlle Dateien wurden verarbeitet!")