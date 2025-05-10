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

def StatistischeKennzahlenUndNormalverteilung(df, spalte, zeitreihenname):
    """
    Prüft, ob eine Zeitreihe normalverteilt ist, basierend auf den Intervallen:
    - [mu - sigma, mu + sigma] für ca. 70% der Beobachtungen
    - [mu - 2*sigma, mu + 2*sigma] für ca. 95% der Beobachtungen
    
    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, der die Zeitreihe enthält.
    - spalte: str
        Der Name der Spalte, die die Zeitreihe enthält.
    - zeitreihenname: str
        Name der Zeitreihe für den Grafiktitel und den Dateinamen
        
    *Returns:*
    - None: Gibt eine Analyse der Normalverteilung zurück und speichert Grafik.
    """
    print(f"\n--- Statistische Kennzahlen für {zeitreihenname} ---")
    
    # Berechne Mittelwert (mu) und Standardabweichung (sigma)
    mu = df[spalte].mean()
    sigma = df[spalte].std()
    
    # Intervall [mu - sigma, mu + sigma] für ca. 70% der Beobachtungen
    intervall_70 = ((mu - sigma), (mu + sigma))
    
    # Intervall [mu - 2*sigma, mu + 2*sigma] für ca. 95% der Beobachtungen
    intervall_95 = ((mu - 2*sigma), (mu + 2*sigma))
    
    # Berechne, wie viele Beobachtungen in diesen Intervallen liegen
    in_70_intervall = df[(df[spalte] >= intervall_70[0]) & (df[spalte] <= intervall_70[1])]
    in_95_intervall = df[(df[spalte] >= intervall_95[0]) & (df[spalte] <= intervall_95[1])]
    
    # Berechne den Prozentsatz der Werte, die in den Intervallen liegen
    prozent_70 = len(in_70_intervall) / len(df) * 100
    prozent_95 = len(in_95_intervall) / len(df) * 100
    
    print(f"Prozentuale Beobachtungen im Intervall [mu - sigma, mu + sigma] (ca. 70%): {prozent_70:.2f}%")
    print(f"Prozentuale Beobachtungen im Intervall [mu - 2*sigma, mu + 2*sigma] (ca. 95%): {prozent_95:.2f}%")
    
    # Überprüfen, ob die Prozentsätze nahe den Erwartungen liegen
    if abs(prozent_70 - 70) > 10:
        print("Warnung: Die Zeitreihe entspricht nicht der 70%-Regel.")
    else:
        print("Die Zeitreihe entspricht der 70%-Regel.")
    
    if abs(prozent_95 - 95) > 10:
        print("Warnung: Die Zeitreihe entspricht nicht der 95%-Regel.")
    else:
        print("Die Zeitreihe entspricht der 95%-Regel.")
    
    # Histogramm der Zeitreihe zur Visualisierung
    plt.figure(figsize=(10, 6))
    plt.hist(df[spalte], bins=30, edgecolor='black', alpha=0.7)
    plt.axvline(mu - sigma, color='r', linestyle='dashed', linewidth=2, label='mu - sigma')
    plt.axvline(mu + sigma, color='r', linestyle='dashed', linewidth=2, label='mu + sigma')
    plt.axvline(mu - 2*sigma, color='g', linestyle='dashed', linewidth=2, label='mu - 2*sigma')
    plt.axvline(mu + 2*sigma, color='g', linestyle='dashed', linewidth=2, label='mu + 2*sigma')
    plt.axvline(mu, color='blue', linestyle='solid', linewidth=2, label='Mittelwert (mu)')
    
    plt.title(f"Verteilung der Zeitreihe {zeitreihenname} und Normalverteilungsintervalle")
    plt.xlabel('Monatliche Durchschnittstemperatur')
    plt.ylabel('Häufigkeit')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Grafikdatei speichern
    ausgabepfad = os.path.join(ergebnisordner, f"normalverteilung_{zeitreihenname}.png")
    plt.savefig(ausgabepfad, dpi=300, bbox_inches='tight')
    print(f"Grafik gespeichert unter: {ausgabepfad}")
    
    # Schließe die Grafik-Instanz, um Speicher freizugeben
    plt.close()

# Schleife durch alle Dateipfade mit ihren Namen
for file_path, zeitreihenname in dateipfade_mit_namen:
    print(f"\nAnalysiere Datei: {file_path} für Zeitreihe: {zeitreihenname}")
    
    # Daten einlesen
    df = DatenEinlesen(file_path, sep=",")
    
    if df is None:
        print(f"Fehler beim Einlesen der Daten aus {file_path}. Überspringe diese Datei.")
        continue
    
    print("Daten erfolgreich eingelesen!")
    print(f"Anzahl der Datenpunkte: {len(df)}")
    
    # Statistische Kennzahlen berechnen und Normalverteilung prüfen
    StatistischeKennzahlenUndNormalverteilung(df, 'MonatlicheDurchschnittsTemperatur', zeitreihenname)

print("\nAnalyse abgeschlossen. Alle Grafiken wurden im Ordner 'ergebnisse' gespeichert.")