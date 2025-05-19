import os
import sys
import time

# === Zentrale Konfiguration importieren ===
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

# Projektpfade initialisieren
config.init_project_paths()

# === Import der Analyse-Module ===
from . import (
    StatistischerUeberblick,
    Stationaritätstest,
    AcfUndPacf,
    Liniendiagramme
)

def run_complete_analysis():
    """
    Führt die komplette Analysepipeline für alle Städte durch:
    1. Statistischer Überblick
    2. Stationaritätstest
    3. ACF/PACF Analyse
    4. Liniendiagramme
    """
    start_time = time.time()

    print(" Starte komplette Analysepipeline...")
    print(f" Projektverzeichnis: {config.PROJECT_ROOT}")
    print(f" Städte: {', '.join(config.CITIES)}")
    print(f" Ausgabeordner: {config.OUTPUT_FOLDER}")
    print("\n" + "="*80)

    completed_steps = 0
    total_steps = 4

    # === Schritt 1: Statistischer Überblick ===
    print(f"\n SCHRITT 1/{total_steps}: Statistischer Überblick")
    print("-" * 50)
    print("   → Berechnet statistische Kennzahlen")
    print("   → Erstellt Histogramme und Boxplots")
    print("   → Prüft Normalverteilungsregeln")
    try:
        StatistischerUeberblick.main()
        completed_steps += 1
    except Exception as e:
        print(f"    Fehler beim Statistischen Überblick: {e}")
        return False

    # === Schritt 2: Stationaritätsanalyse ===
    print(f"\n SCHRITT 2/{total_steps}: Stationaritätsanalyse")
    print("-" * 50)
    print("   → Führt ADF-Tests durch")
    print("   → Führt KPSS-Tests durch")
    print("   → Erstellt stationäre Zeitreihen")
    try:
        Stationaritätstest.main()
        completed_steps += 1
    except Exception as e:
        print(f"    Fehler bei Stationaritätsanalyse: {e}")
        return False

    # === Schritt 3: ACF/PACF Analyse ===
    print(f"\n SCHRITT 3/{total_steps}: ACF/PACF Analyse")
    print("-" * 50)
    print("   → Berechnet Autokorrelationsfunktionen")
    print("   → Berechnet partielle Autokorrelationsfunktionen")
    print("   → Erstellt Korrelationsplots")
    try:
        AcfUndPacf.main()
        completed_steps += 1
    except Exception as e:
        print(f"    Fehler bei ACF/PACF Analyse: {e}")
        return False

    # === Schritt 4: Liniendiagramme ===
    print(f"\n SCHRITT 4/{total_steps}: Liniendiagramme erstellen")
    print("-" * 50)
    print("   → Erstellt Zeitreihen-Visualisierungen")
    print("   → Zeigt Trends und Saisonalität")
    try:
        Liniendiagramme.create_line_plots()
        completed_steps += 1
    except Exception as e:
        print(f"    Fehler bei Liniendiagrammen: {e}")
        return False

    # === Zusammenfassung ===
    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "="*80)
    print(" ANALYSEPIPELINE ERFOLGREICH ABGESCHLOSSEN! ")
    print(f" Gesamtdauer: {duration:.2f} Sekunden")
    print(f" Abgeschlossene Schritte: {completed_steps}/{total_steps}")
    print(f"\n Alle Ergebnisse befinden sich in: {config.OUTPUT_FOLDER}")
    print("\n Übersicht der Ausgabeordner:")
    print(f"    Statistische Kennzahlen: {config.OUTPUT_STATISTIK_KENNZAHLEN}")
    print(f"    Histogramme:             {config.OUTPUT_HISTOGRAMME}")
    print(f"    Boxplots:                {config.OUTPUT_BOXPLOTS}")
    print(f"    Stationarität:           {config.OUTPUT_STATIONARITAET}")
    print(f"    ACF/PACF Plots:          {config.OUTPUT_ACF_PACF_PLOTS}")
    print(f"    Liniendiagramme:         {config.OUTPUT_LINIENDIAGRAMME}")
    print("="*80)

    return True

def run_single_analysis(analysis_type):
    """
    Führt eine spezifische Analyse durch

    Parameters:
    - analysis_type: str - 'statistical_overview', 'stationarity', 'acf_pacf', 'plots'
    """
    analysis_map = {
        'statistical_overview': {
            'name': 'Statistischer Überblick',
            'func': StatistischerUeberblick.main,
            'description': 'Berechnet Kennzahlen, erstellt Histogramme und Boxplots'
        },
        'stationarity': {
            'name': 'Stationaritätsanalyse',
            'func': Stationaritätstest.main,
            'description': 'Führt ADF- und KPSS-Tests durch, erstellt stationäre Zeitreihen'
        },
        'acf_pacf': {
            'name': 'ACF/PACF Analyse',
            'func': AcfUndPacf.main,
            'description': 'Berechnet Auto- und partielle Autokorrelationsfunktionen'
        },
        'plots': {
            'name': 'Liniendiagramme',
            'func': Liniendiagramme.create_line_plots,
            'description': 'Erstellt Zeitreihen-Visualisierungen'
        }
    }

    if analysis_type not in analysis_map:
        print(f" Unbekannter Analyse-Typ: {analysis_type}")
        print(f"Verfügbare Optionen: {list(analysis_map.keys())}")
        return False

    analysis = analysis_map[analysis_type]

    start_time = time.time()
    print(f" Starte {analysis['name']}...")
    print(f" Beschreibung: {analysis['description']}")
    print(f" Städte: {', '.join(config.CITIES)}")
    print("="*60)

    try:
        analysis['func']()
        end_time = time.time()
        duration = end_time - start_time

        print("="*60)
        print(f" {analysis['name']} erfolgreich abgeschlossen")
        print(f" Dauer: {duration:.2f} Sekunden")
        print(f" Ergebnisse in: {config.OUTPUT_FOLDER}")
        return True
    except Exception as e:
        print("="*60)
        print(f" Fehler bei {analysis['name']}: {e}")
        return False

def main():
    """
    Hauptfunktion für die Analyse-Pipeline - führt die komplette Pipeline durch
    """
    run_complete_analysis()

# === Hauptausführung ===
if __name__ == "__main__":
    main()