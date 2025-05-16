import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import pandas as pd
import os
import sys

# Projektverzeichnis setzen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config

# Ergebnisordner vorbereiten
output_dir = os.path.join(config.OUTPUT_FOLDER, "acf_pacf_plots")
os.makedirs(output_dir, exist_ok=True)

# Liste der Städte
cities = ["abakan", "berlin", "angeles"]

def plot_acf_series(series, lags, city):
    plt.figure(figsize=(10, 5))
    plot_acf(series.dropna(), lags=lags, ax=plt.gca(), title=f"ACF – {city.capitalize()}")
    plt.tight_layout()
    acf_path = os.path.join(output_dir, f"acf_plot_{city}.png")
    plt.savefig(acf_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ ACF gespeichert: {acf_path}")

def plot_pacf_series(series, lags, city):
    plt.figure(figsize=(10, 5))
    plot_pacf(series.dropna(), lags=lags, ax=plt.gca(), method='ywm', title=f"PACF – {city.capitalize()}")
    plt.tight_layout()
    pacf_path = os.path.join(output_dir, f"pacf_plot_{city}.png")
    plt.savefig(pacf_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ PACF gespeichert: {pacf_path}")

# Schleife über alle Städte
for city in cities:
    path = os.path.join("daten", "stationäre-daten", f"stationaere_zeitreihe_{city}.csv")
    if not os.path.exists(path):
        print(f"❌ Datei nicht gefunden für Stadt: {city} → {path}")
        continue

    df = pd.read_csv(path)
    if "MonatlicheDurchschnittsTemperatur" not in df.columns:
        print(f"❌ Spalte 'MonatlicheDurchschnittsTemperatur' fehlt in Datei: {path}")
        continue

    series = df["MonatlicheDurchschnittsTemperatur"]
    print(f"\n🔍 Verarbeite Stadt: {city} – {len(series)} Datenpunkte")

    plot_acf_series(series, lags=30, city=city)
    plot_pacf_series(series, lags=30, city=city)

print("\n✅ ACF- und PACF-Analyse für alle Städte abgeschlossen.")
