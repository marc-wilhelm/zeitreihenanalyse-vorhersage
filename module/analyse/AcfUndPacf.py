import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import pandas as pd
import os

# === Zentrale Konfiguration importieren ===
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

# Projektpfade initialisieren
config.init_project_paths()

def plot_acf_series(series, lags, city):
    """Erstellt und speichert ACF-Plot für eine Stadt"""
    plt.figure(figsize=(10, 5))
    plot_acf(series.dropna(), lags=lags, ax=plt.gca(), title=f"ACF – {city.capitalize()}")
    plt.tight_layout()
    acf_path = os.path.join(config.OUTPUT_ACF_PACF_PLOTS, f"acf_plot_{city}.png")
    plt.savefig(acf_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ ACF gespeichert: {acf_path}")

def plot_pacf_series(series, lags, city):
    """Erstellt und speichert PACF-Plot für eine Stadt"""
    plt.figure(figsize=(10, 5))
    plot_pacf(series.dropna(), lags=lags, ax=plt.gca(), method='ywm', title=f"PACF – {city.capitalize()}")
    plt.tight_layout()
    pacf_path = os.path.join(config.OUTPUT_ACF_PACF_PLOTS, f"pacf_plot_{city}.png")
    plt.savefig(pacf_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ PACF gespeichert: {pacf_path}")

# === Hauptausführung ===
def main():
    print("🔍 ACF- und PACF-Analyse wird gestartet...")

    # Schleife über alle Städte
    for city in config.CITIES:
        path = config.get_stationary_data_path(city)

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

    print(f"\n✅ ACF- und PACF-Analyse für alle Städte abgeschlossen.")
    print(f"📁 Alle Plots gespeichert in: {config.OUTPUT_ACF_PACF_PLOTS}")

if __name__ == "__main__":
    main()