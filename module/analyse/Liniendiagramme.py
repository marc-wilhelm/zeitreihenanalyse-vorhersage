import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# === Projektstruktur einbinden ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# === Städte & Dateipfade ===
cities = {
    "abakan": config.PATH_TS_ABAKAN_CLEAN,
    "berlin": config.PATH_TS_BERLIN_CLEAN,
    "angeles": config.PATH_TS_ANGELES_CLEAN
}

# === Verzeichnis für Diagramme vorbereiten ===
output_dir = os.path.join("results", "Liniendiagramme")
os.makedirs(output_dir, exist_ok=True)

# === Schleife über alle Städte ===
for city, original_path in cities.items():
    print(f"\n📈 Verarbeite Stadt: {city}")

    # === Originale Zeitreihe laden ===
    try:
        df_original = pd.read_csv(original_path)
        df_original['Datum'] = pd.to_datetime(df_original['Datum'])
    except Exception as e:
        print(f"❌ Fehler beim Laden der Originaldaten für {city}: {e}")
        continue

    # === Diagramm Originaldaten ===
    plt.figure(figsize=(10, 6))
    plt.plot(df_original['Datum'], df_original['MonatlicheDurchschnittsTemperatur'])
    plt.title(f"Originale Zeitreihe – {city.capitalize()}")
    plt.xlabel("Datum")
    plt.ylabel("Temperatur")
    plt.grid(True)
    plt.legend(["Temperatur"])
    plt.tight_layout()
    filename_original = f"originale_zeitreihe_liniendiagramm_{city}.png"
    plt.savefig(os.path.join(output_dir, filename_original), dpi=300)
    plt.close()
    print(f"✅ Originaldiagramm gespeichert: {filename_original}")

    # === Stationäre Zeitreihe laden ===
    path_stationary = os.path.join("daten", "stationäre-daten", f"stationaere_zeitreihe_{city}.csv")
    try:
        df_stationary = pd.read_csv(path_stationary)
        df_stationary['Datum'] = pd.to_datetime(df_stationary['Datum'])
    except Exception as e:
        print(f"⚠️ Fehler beim Laden der stationären Daten für {city}: {e}")
        continue

    # === Diagramm stationäre Zeitreihe ===
    plt.figure(figsize=(10, 6))
    plt.plot(df_stationary['Datum'], df_stationary['MonatlicheDurchschnittsTemperatur'])
    plt.title(f"Stationäre Zeitreihe – {city.capitalize()}")
    plt.xlabel("Datum")
    plt.ylabel("Temperatur (differenziert)")
    plt.grid(True)
    plt.legend(["Stationäre Temperatur"])
    plt.tight_layout()
    filename_stationary = f"stationaere_zeitreihe_liniendiagramm_{city}.png"
    plt.savefig(os.path.join(output_dir, filename_stationary), dpi=300)
    plt.close()
    print(f"✅ Stationäres Diagramm gespeichert: {filename_stationary}")

print("\n✅ Alle Liniendiagramme erfolgreich gespeichert in: results/Liniendiagramme")
