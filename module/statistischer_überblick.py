import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from Hilfsfunktionen.DatenEinlesen import DatenEinlesen

# Projektverzeichnis setzen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Arbeitsverzeichnis auf Projektverzeichnis setzen
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(f"Aktuelles Arbeitsverzeichnis: {os.getcwd()}")

# Ergebnisverzeichnisse erstellen
results_dir = os.path.join("results")
os.makedirs(os.path.join(results_dir, "statistische_kennzahlen"), exist_ok=True)
os.makedirs(os.path.join(results_dir, "histogramme"), exist_ok=True)
os.makedirs(os.path.join(results_dir, "boxplots"), exist_ok=True)

# Liste der Eingabepfade und Städtenamen
dateipfade_mit_namen = [
    (config.PATH_TS_BERLIN_CLEAN, "berlin"),
    (config.PATH_TS_ANGELES_CLEAN, "angeles"),
    (config.PATH_TS_ABAKAN_CLEAN, "abakan")
]

def StatistischeAnalyse(df, spalte, city):
    """
    Führt statistische Analyse für eine gegebene Stadt durch:
    - Berechnet Kennzahlen
    - Prüft Normalverteilungsregeln (70%, 95%)
    - Erstellt Histogramm mit Linien
    - Erstellt Boxplot
    - Speichert alles in definierten Ordnern
    """
    print(f"\n--- Statistische Analyse für {city} ---")

    # Statistische Kennzahlen berechnen
    mu = df[spalte].mean()
    sigma = df[spalte].std()
    median = df[spalte].median()
    min_val = df[spalte].min()
    max_val = df[spalte].max()

    # Normalverteilungs-Intervalle
    intervall_70 = (mu - sigma, mu + sigma)
    intervall_95 = (mu - 2*sigma, mu + 2*sigma)

    in_70 = df[(df[spalte] >= intervall_70[0]) & (df[spalte] <= intervall_70[1])]
    in_95 = df[(df[spalte] >= intervall_95[0]) & (df[spalte] <= intervall_95[1])]

    prozent_70 = len(in_70) / len(df) * 100
    prozent_95 = len(in_95) / len(df) * 100

    regel_70_ok = abs(prozent_70 - 70) <= 10
    regel_95_ok = abs(prozent_95 - 95) <= 10

    # === Statistische Kennzahlen als Kommentierte Textzeilen vorbereiten ===
    summary_lines = [
        f"# Statistische Kennzahlen für {city.capitalize()}",
        f"# mean = {mu:.4f}",
        f"# std = {sigma:.4f}",
        f"# median = {median:.4f}",
        f"# min = {min_val:.4f}",
        f"# max = {max_val:.4f}",
        "",
        f"# Normalverteilungsprüfung:",
        f"# Anteil in [mu - sigma, mu + sigma] (~70%): {prozent_70:.2f}%",
        f"# Erfüllt 70%-Regel: {'Ja' if regel_70_ok else 'Nein'}",
        f"# Anteil in [mu - 2*sigma, mu + 2*sigma] (~95%): {prozent_95:.2f}%",
        f"# Erfüllt 95%-Regel: {'Ja' if regel_95_ok else 'Nein'}"
    ]
    summary_text = "\n".join(summary_lines)

    # Datei speichern
    stats_path = os.path.join(results_dir, "statistische_kennzahlen", f"statistische_kennzahlen_{city}.py")
    with open(stats_path, "w", encoding="utf-8") as f:
        f.write(summary_text + "\n")
    print(f"✅ Statistiken gespeichert unter: {stats_path}")

    # === Histogramm mit Linien ===
    plt.figure(figsize=(10, 6))
    plt.hist(df[spalte], bins=30, edgecolor='black', alpha=0.7)
    plt.axvline(mu, color='blue', linestyle='solid', linewidth=2, label='Mittelwert (mu)')
    plt.axvline(mu - sigma, color='red', linestyle='dashed', linewidth=2, label='mu - sigma')
    plt.axvline(mu + sigma, color='red', linestyle='dashed', linewidth=2, label='mu + sigma')
    plt.axvline(mu - 2*sigma, color='green', linestyle='dashed', linewidth=2, label='mu - 2*sigma')
    plt.axvline(mu + 2*sigma, color='green', linestyle='dashed', linewidth=2, label='mu + 2*sigma')
    plt.title(f"Verteilung der Zeitreihe {city.capitalize()} und Normalverteilungsintervalle")
    plt.xlabel("Monatliche Durchschnittstemperatur")
    plt.ylabel("Häufigkeit")
    plt.legend()
    plt.grid(True, alpha=0.3)

    hist_path = os.path.join(results_dir, "histogramme", f"histogramm_{city}.png")
    plt.savefig(hist_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📊 Histogramm gespeichert unter: {hist_path}")

    # === Boxplot ===
    plt.figure(figsize=(6, 6))
    plt.boxplot(df[spalte], vert=True, patch_artist=True)
    plt.title(f"Boxplot der Temperaturwerte – {city.capitalize()}")
    plt.ylabel("Monatliche Durchschnittstemperatur")
    plt.grid(True, alpha=0.3)

    boxplot_path = os.path.join(results_dir, "boxplots", f"boxplot_{city}.png")
    plt.savefig(boxplot_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📦 Boxplot gespeichert unter: {boxplot_path}")

# === Hauptschleife durch alle Städte ===
for file_path, city in dateipfade_mit_namen:
    print(f"\nAnalysiere Datei: {file_path} für Stadt: {city}")
    df = DatenEinlesen(file_path, sep=",")

    if df is None:
        print(f"❌ Fehler beim Einlesen von {file_path}. Überspringe.")
        continue

    if "MonatlicheDurchschnittsTemperatur" not in df.columns:
        print(f"❌ Spalte 'MonatlicheDurchschnittsTemperatur' fehlt in {file_path}.")
        continue

    StatistischeAnalyse(df, "MonatlicheDurchschnittsTemperatur", city)

print("\n✅ Analyse abgeschlossen. Ergebnisse wurden im 'results'-Ordner gespeichert.")
