# Importiere die entsprechenden Funktionen aus jedem Modul
from DatenEinlesen import DatenEinlesen
from SpaltennamenKorrigieren import SpaltennamenKorrigieren
from DatumFormatieren import DatumFormatieren
from TemperaturUndDatumExtrahieren import TemperaturUndDatumExtrahieren
from ZeitreiheAb1850 import ZeitreiheAb1850
from TemperaturRunden import TemperaturRunden
from NaNPruefen import NaNPruefen
from DatentypenPruefen import DatentypenPruefen
from DuplikatePruefen import DuplikatePruefen
from BereinigteDatenSpeichern import BereinigteDatenSpeichern

def main():
    # 1. Definiere die Eingabe- und Ausgabepfade
    file_path = "D:\\Johanna\\Studium\\6.Semester\\BBA Schwerpunkt\\Menden\\Git\\zeitreihenanalyse-vorhersage\\daten\\original-daten\\Zeitreihe_Berlin.csv"
    output_path = "D:\\Johanna\\Studium\\6.Semester\\BBA Schwerpunkt\\Menden\\Git\\zeitreihenanalyse-vorhersage\\daten\\bereinigte-daten\\zeitreihe_berlin_bereinigt.csv"

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

    # 6. Zeitreihe ab 1850 filtern
    df = ZeitreiheAb1850(df)
    print("Daten ab 1850 gefiltert!")

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

