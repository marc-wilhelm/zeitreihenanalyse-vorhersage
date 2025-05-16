import os
import sys

# === PROJEKTSTRUKTUR UND PFAD-INITIALISIERUNG ===
def get_project_root():
    """Ermittelt das Projektverzeichnis basierend auf der config.py Datei"""
    return os.path.dirname(os.path.abspath(__file__))

def init_project_paths():
    """
    Initialisiert die Projektpfade und fügt das Projektverzeichnis zum Python-Pfad hinzu.
    Diese Funktion sollte in jedem Modul aufgerufen werden.
    """
    project_root = get_project_root()

    # Projektverzeichnis zum Python-Pfad hinzufügen
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Working Directory auf Projektverzeichnis setzen
    os.chdir(project_root)

    return project_root

# === PROJEKTPFADE ===
PROJECT_ROOT = get_project_root()

# === EINGABEDATEN ===
# Original Daten
PATH_TS_BERLIN = os.path.join(PROJECT_ROOT, "daten", "original-daten", "zeitreihe_berlin.csv")
PATH_TS_ANGELES = os.path.join(PROJECT_ROOT, "daten", "original-daten", "zeitreihe_angeles.csv")
PATH_TS_ABAKAN = os.path.join(PROJECT_ROOT, "daten", "original-daten", "zeitreihe_abakan.csv")

# Bereinigte Daten
PATH_TS_BERLIN_CLEAN = os.path.join(PROJECT_ROOT, "daten", "bereinigte-daten", "bereinigt_zeitreihe_berlin.csv")
PATH_TS_ANGELES_CLEAN = os.path.join(PROJECT_ROOT, "daten", "bereinigte-daten", "bereinigt_zeitreihe_angeles.csv")
PATH_TS_ABAKAN_CLEAN = os.path.join(PROJECT_ROOT, "daten", "bereinigte-daten", "bereinigt_zeitreihe_abakan.csv")

# Stationäre Daten
STATIONAER_DATEN_DIR = os.path.join(PROJECT_ROOT, "daten", "stationäre-daten")

# === AUSGABEVERZEICHNISSE ===
# Hauptausgabeordner
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "ergebnisse")

# Spezifische Ausgabeordner
OUTPUT_ACF_PACF_PLOTS = os.path.join(OUTPUT_FOLDER, "acf_pacf_plots")
OUTPUT_LINIENDIAGRAMME = os.path.join(OUTPUT_FOLDER, "Liniendiagramme")
OUTPUT_STATIONARITAET = os.path.join(OUTPUT_FOLDER, "stationarität-ergebnisse")
OUTPUT_SARIMA_RESIDUEN = os.path.join(OUTPUT_FOLDER, "sarima_residuen_auswertung")
OUTPUT_EVALUATIONS_METRIKEN = os.path.join(OUTPUT_FOLDER, "evaluations_metriken")
OUTPUT_MODEL_PARAMETERS = os.path.join(OUTPUT_FOLDER, "model_parameters")

# === STÄDTELISTE UND DATENPFADE ===
CITIES = ["abakan", "berlin", "angeles"]

CITY_PATHS_ORIGINAL = {
    "abakan": PATH_TS_ABAKAN,
    "berlin": PATH_TS_BERLIN,
    "angeles": PATH_TS_ANGELES
}

CITY_PATHS_CLEAN = {
    "abakan": PATH_TS_ABAKAN_CLEAN,
    "berlin": PATH_TS_BERLIN_CLEAN,
    "angeles": PATH_TS_ANGELES_CLEAN
}

# === UTILITY FUNKTIONEN ===
def ensure_output_dirs():
    """Erstellt alle notwendigen Ausgabeordner falls sie nicht existieren"""
    output_dirs = [
        OUTPUT_FOLDER,
        OUTPUT_ACF_PACF_PLOTS,
        OUTPUT_LINIENDIAGRAMME,
        OUTPUT_STATIONARITAET,
        OUTPUT_SARIMA_RESIDUEN,
        OUTPUT_EVALUATIONS_METRIKEN,
        OUTPUT_MODEL_PARAMETERS,
        STATIONAER_DATEN_DIR
    ]

    for directory in output_dirs:
        os.makedirs(directory, exist_ok=True)

def get_stationary_data_path(city):
    """Gibt den Pfad für stationäre Daten einer Stadt zurück"""
    return os.path.join(STATIONAER_DATEN_DIR, f"stationaere_zeitreihe_{city}.csv")

def get_city_output_dir(base_output_dir, city):
    """Erstellt und gibt ein stadtspezifisches Ausgabeverzeichnis zurück"""
    city_dir = os.path.join(base_output_dir, city)
    os.makedirs(city_dir, exist_ok=True)
    return city_dir

# === INITIALISIERUNG ===
# Beim Import der config.py werden die Ausgabeordner erstellt
ensure_output_dirs()