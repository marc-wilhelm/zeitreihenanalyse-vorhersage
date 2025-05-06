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
import sys
import os

# Übergeordnetes Verzeichnis damit config Modul gefunden wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config

def main():
    # 1. Definiere die Eingabe- und Ausgabepfade
    file_path = config.datapathzeitreiheberlin
    output_path = config.datapathzeitreiheberlinbereinigt
    # 2. Daten einlesen
    df = DatenEinlesen(file_path, sep= ";")
    
    if df is None:
        print("Fehler beim Einlesen der Daten. Beende das Skript.")
        return

    print("Daten erfolgreich eingelesen!")

    # 3. Spaltennamen korrigieren
    df = SpaltennamenKorrigieren(df)
    print("Spaltennamen korrigiert!")
    print(df.head())

    # 4. Datum formatieren
    df = DatumFormatieren(df)
    print("Datum formatiert!")

    # 5. Temperatur und Datum extrahieren
    df = TemperaturUndDatumExtrahieren(df)
    print("Nur Temperatur und Datum extrahiert!")

    # 6. Zeitreihe ab 1880 filtern
    df = ZeitreiheAb1880(df)
    print("Daten ab 1880 gefiltert!")

    # 7. Temperaturwerte runden
    df = TemperaturRunden(df)
    print("Temperaturwerte gerundet!")


    # 8. NaN-Werte prüfen
    df = NaNPruefen(df)  


    # 9. Datentypen prüfen
    DatentypenPruefen(df)
    

    # 10. Duplikate prüfen
    DuplikatePruefen(df)
    

    # 11. Daten speichern
    BereinigteDatenSpeichern(df, output_path)
    print(f"Daten erfolgreich gespeichert unter {output_path}!")

if __name__ == "__main__":
    main()

