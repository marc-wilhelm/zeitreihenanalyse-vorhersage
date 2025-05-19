import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# === Zentrale Konfiguration importieren ===
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

# Projektpfade initialisieren
config.init_project_paths()

def create_line_plots():
    """Erstellt Liniendiagramme für originale und stationäre Zeitreihen aller Städte"""
    print(" Liniendiagramme werden erstellt...")

    # Schleife über alle Städte
    for city in config.CITIES:
        print(f"\n Verarbeite Stadt: {city}")

        # === Originale Zeitreihe laden ===
        original_path = config.CITY_PATHS_CLEAN[city]
        try:
            df_original = pd.read_csv(original_path)
            df_original['Datum'] = pd.to_datetime(df_original['Datum'])
        except Exception as e:
            print(f" Fehler beim Laden der Originaldaten für {city}: {e}")
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
        output_path_original = os.path.join(config.OUTPUT_LINIENDIAGRAMME, filename_original)
        plt.savefig(output_path_original, dpi=300)
        plt.close()
        print(f" Originaldiagramm gespeichert: {filename_original}")

        # === Stationäre Zeitreihe laden ===
        stationary_path = config.get_stationary_data_path(city)
        try:
            df_stationary = pd.read_csv(stationary_path)
            df_stationary['Datum'] = pd.to_datetime(df_stationary['Datum'])
        except Exception as e:
            print(f" Fehler beim Laden der stationären Daten für {city}: {e}")
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
        output_path_stationary = os.path.join(config.OUTPUT_LINIENDIAGRAMME, filename_stationary)
        plt.savefig(output_path_stationary, dpi=300)
        plt.close()
        print(f" Stationäres Diagramm gespeichert: {filename_stationary}")

    print(f"\n Alle Liniendiagramme erfolgreich gespeichert in: {config.OUTPUT_LINIENDIAGRAMME}")

# === Hauptausführung ===
if __name__ == "__main__":
    create_line_plots()