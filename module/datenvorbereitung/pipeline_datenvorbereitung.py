import os
import sys

# === Zentrale Konfiguration importieren ===
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

# Projektpfade initialisieren
config.init_project_paths()

# === Import der Datenvorbereitung-Funktionen ===
from .Bereinigung import (
    daten_einlesen,
    spaltennamen_korrigieren,
    datum_formatieren,
    temperatur_und_datum_extrahieren,
    zeitreihe_ab_1880,
    nan_pruefen,
    datentypen_pruefen,
    duplikate_pruefen,
    bereinigte_daten_speichern
)

def process_single_city(city, input_path, output_path, sep=";", decimal=","):
    """
    Verarbeitet die Daten einer einzelnen Stadt durch die komplette Pipeline.

    Parameters:
    city: str - Name der Stadt
    input_path: str - Pfad zur Eingabedatei
    output_path: str - Pfad zur Ausgabedatei
    sep: str - CSV-Separator
    decimal: str - Dezimaltrennzeichen

    Returns:
    bool - True wenn erfolgreich, False bei Fehler
    """
    print(f"\n Stadt: {city}")
    print(f"    Eingabe: {os.path.basename(input_path)}")
    print(f"    Ausgabe: {os.path.basename(output_path)}")

    try:
        # 1. Daten einlesen
        print("    Schritt 1: Daten einlesen...")
        df = daten_einlesen(input_path, sep=sep, decimal=decimal)

        if df is None:
            print(f"    Fehler beim Einlesen der Daten. Überspringe {city}.")
            return False

        original_rows = len(df)
        print(f"    {original_rows} Datensätze eingelesen")

        # 2. Spaltennamen korrigieren
        print("    Schritt 2: Spaltennamen korrigieren...")
        df = spaltennamen_korrigieren(df)
        print("    Spaltennamen korrigiert")

        # 3. Datum formatieren
        print("    Schritt 3: Datum formatieren...")
        df = datum_formatieren(df)
        print("    Datum formatiert")

        # 4. Temperatur und Datum extrahieren
        print("    Schritt 4: Temperatur und Datum extrahieren...")
        df = temperatur_und_datum_extrahieren(df)
        print("    Nur relevante Spalten extrahiert")

        # 5. Zeitreihe ab 1880 filtern
        print("    Schritt 5: Daten ab 1880 filtern...")
        df = zeitreihe_ab_1880(df)
        filtered_rows = len(df)
        print(f"    Daten gefiltert ({original_rows} → {filtered_rows} Datensätze)")

        # 6. NaN-Werte prüfen
        print("    Schritt 6: NaN-Werte prüfen...")
        df = nan_pruefen(df)
        print("    NaN-Prüfung abgeschlossen")

        # 7. Datentypen prüfen
        print("    Schritt 7: Datentypen prüfen...")
        datentypen_pruefen(df)
        print("    Datentypen geprüft")

        # 8. Duplikate prüfen
        print("    Schritt 8: Duplikate prüfen...")
        duplikate_pruefen(df)
        print("    Duplikate geprüft")

        # 9. Daten speichern
        print("    Schritt 9: Bereinigte Daten speichern...")
        bereinigte_daten_speichern(df, output_path)
        final_rows = len(df)
        print(f"    Daten gespeichert ({final_rows} Datensätze)")

        print(f"    {city} erfolgreich verarbeitet!")
        print("\n" + "="*80)
        return True

    except Exception as e:
        print(f"    Fehler bei {city}: {e}")
        return False

def run_complete_preprocessing():
    """
    Führt die komplette Datenvorbereitungspipeline für alle Städte durch.
    """
    print(" Starte komplette Datenvorbereitungspipeline...")
    print(f" Projektverzeichnis: {config.PROJECT_ROOT}")
    print(f" Städte: {', '.join(config.CITIES)}")
    print("\n" + "="*80)

    success_count = 0

    # Alle Städte verarbeiten
    for city in config.CITIES:
        input_path = config.CITY_PATHS_ORIGINAL[city]
        output_path = config.CITY_PATHS_CLEAN[city]

        # Stelle sicher, dass das Ausgabeverzeichnis existiert
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Stadt verarbeiten
        if process_single_city(city, input_path, output_path):
            success_count += 1

    # Zusammenfassung
    if success_count == len(config.CITIES):
        print(" DATENVORBEREITUNGSPIPELINE ERFOLGREICH ABGESCHLOSSEN! ")
    else:
        print(f" DATENVORBEREITUNGSPIPELINE BEENDET - {success_count}/{len(config.CITIES)} STÄDTE ERFOLGREICH")

    print(f" Bereinigte Daten befinden sich in: {os.path.join(config.PROJECT_ROOT, 'daten', 'bereinigte-daten')}")
    print("="*80)

    return success_count == len(config.CITIES)

def run_single_preprocessing(city):
    """
    Führt die Datenvorbereitungspipeline für eine spezifische Stadt durch.

    Parameters:
    city: str - Name der Stadt ('abakan', 'berlin', 'angeles')

    Returns:
    bool - True wenn erfolgreich, False bei Fehler
    """
    if city not in config.CITIES:
        print(f" Unbekannte Stadt: {city}")
        print(f"Verfügbare Städte: {config.CITIES}")
        return False

    print(f" Starte Datenvorbereitung für {city}...")
    print("="*60)

    input_path = config.CITY_PATHS_ORIGINAL[city]
    output_path = config.CITY_PATHS_CLEAN[city]

    # Stelle sicher, dass das Ausgabeverzeichnis existiert
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Stadt verarbeiten
    success = process_single_city(city, input_path, output_path)

    print("="*60)
    if success:
        print(f" Datenvorbereitung für {city} erfolgreich abgeschlossen")
    else:
        print(f" Datenvorbereitung für {city} fehlgeschlagen")

    return success

def main():
    """
    Hauptfunktion für die Datenvorbereitung - führt die komplette Pipeline durch
    """
    run_complete_preprocessing()

# === Hauptausführung ===
if __name__ == "__main__":
    main()