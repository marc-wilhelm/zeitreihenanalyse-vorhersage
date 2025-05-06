import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from Hilfsfunktionen.DatenEinlesen import DatenEinlesen

# Übergeordnetes Verzeichnis damit config Modul gefunden wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config


# 1. Definiere die Eingabe- und Ausgabepfade
file_path = config.datapathzeitreiheangelesbereinigt
    # 2. Daten einlesen
df = DatenEinlesen(file_path, sep= ",")
    
if df is None:
    print("Fehler beim Einlesen der Daten. Beende das Skript.")



def StatistischeKennzahlenUndNormalverteilung(df, spalte):
    """
    Prüft, ob eine Zeitreihe normalverteilt ist, basierend auf den Intervallen:
    - [mu - sigma, mu + sigma] für ca. 70% der Beobachtungen
    - [mu - 2*sigma, mu + 2*sigma] für ca. 95% der Beobachtungen
    
    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, der die Zeitreihe enthält.
    - spalte: str
        Der Name der Spalte, die die Zeitreihe enthält.

    *Returns:*
    - None: Gibt eine Analyse der Normalverteilung zurück.
    """
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
    
    # Optional: Histogramm der Zeitreihe zur Visualisierung
    plt.hist(df[spalte], bins=30, edgecolor='black')
    plt.axvline(mu - sigma, color='r', linestyle='dashed', linewidth=2, label='mu - sigma')
    plt.axvline(mu + sigma, color='r', linestyle='dashed', linewidth=2, label='mu + sigma')
    plt.axvline(mu - 2*sigma, color='g', linestyle='dashed', linewidth=2, label='mu - 2*sigma')
    plt.axvline(mu + 2*sigma, color='g', linestyle='dashed', linewidth=2, label='mu + 2*sigma')
    plt.title(f"Verteilung der Zeitreihe und Normalverteilungsintervalle")
    plt.legend()
    plt.show()


StatistischeKennzahlenUndNormalverteilung(df, 'MonatlicheDurchschnittsTemperatur')