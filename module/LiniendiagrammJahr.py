import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from Hilfsfunktionen.DatenEinlesen import DatenEinlesen

# Übergeordnetes Verzeichnis damit config Modul gefunden wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Das Working Directory zum Projektverzeichnis ändern
# Diese Zeile ist entscheidend für die relativen Pfade
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Aktuelle Working Directory ausgeben zur Überprüfung
print(f"Aktuelles Arbeitsverzeichnis: {os.getcwd()}")

# Ergebnisverzeichnis erstellen, falls es nicht existiert
ergebnisordner = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ergebnisse")
os.makedirs(ergebnisordner, exist_ok=True)

# Liste der zu verwendenden Dateipfade mit Namen für die Grafiken
dateipfade_mit_namen = [
    (config.PATH_TS_BERLIN_CLEAN, "Berlin"),
    (config.PATH_TS_ANGELES_CLEAN, "Angeles"),
    (config.PATH_TS_ABAKAN_CLEAN, "Abakan")
]

# Schleife durch alle Dateipfade mit ihren Namen
for file_path, zeitreihenname in dateipfade_mit_namen:
    print(f"\nAnalysiere Datei: {file_path} für Zeitreihe: {zeitreihenname}")
    
    # Daten einlesen
    df = DatenEinlesen(file_path, sep=",")
    
    if df is None:
        print(f"Fehler beim Einlesen der Daten aus {file_path}. Überspringe diese Datei.")
        continue
    
    print("Daten erfolgreich eingelesen!")
    
    # Stelle sicher, dass Datum in datetime konvertiert wird, falls notwendig
    if 'Datum' in df.columns:
        df['Datum'] = pd.to_datetime(df['Datum'])

    # Erstelle das Liniendiagramm
    plt.figure(figsize=(10, 6))
    
 
    if 'Datum' in df.columns:
        plt.plot(df['Datum'], df['MonatlicheDurchschnittsTemperatur'])
    else:
        plt.plot(df['MonatlicheDurchschnittsTemperatur'])
    

    plt.title(f"Monatliche Durchschnittstemperatur - {zeitreihenname}")
    plt.xlabel("Datum")
    plt.ylabel("Temperatur")
    
    
    plt.grid(True)
    plt.legend(['Temperatur'])
    plt.tight_layout()
    
    
    ausgabepfad = os.path.join(ergebnisordner, f"liniendiagramm_{zeitreihenname}.png")
    plt.savefig(ausgabepfad, dpi=300)
    print(f"Grafik gespeichert unter: {ausgabepfad}")
    

    plt.close()

print("\nAnalyse abgeschlossen. Alle Liniendiagramme wurden im Ordner 'ergebnisse' gespeichert.")