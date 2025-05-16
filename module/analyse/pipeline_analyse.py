import os
import sys

# === Zentrale Konfiguration importieren ===
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

# Projektpfade initialisieren
config.init_project_paths()

# === Import der Analyse-Module ===
from module.analyse import stationaritätstest
from module.analyse import acf_und_pacf
from module.analyse import Liniendiagramme
from module.analyse import SARIMA_expanding_window_residuenanalyse

def run_complete_analysis():
    """
    Führt die komplette Analysepipeline für alle Städte durch:
    1. Stationaritätstest
    2. ACF/PACF Analyse
    3. Liniendiagramme
    4. SARIMA Residuenanalyse
    """
    print("🚀 Starte komplette Analysepipeline...")
    print(f"📁 Projektverzeichnis: {config.PROJECT_ROOT}")
    print(f"🏙️ Städte: {', '.join(config.CITIES)}")
    print("\n" + "="*80)

    # === Schritt 1: Stationaritätsanalyse ===
    print("\n🔬 SCHRITT 1: Stationaritätsanalyse")
    print("-" * 40)
    try:
        stationaritätstest.main()
        print("✅ Stationaritätsanalyse abgeschlossen")
    except Exception as e:
        print(f"❌ Fehler bei Stationaritätsanalyse: {e}")
        return False

    # === Schritt 2: ACF/PACF Analyse ===
    print("\n📊 SCHRITT 2: ACF/PACF Analyse")
    print("-" * 40)
    try:
        acf_und_pacf.main()
        print("✅ ACF/PACF Analyse abgeschlossen")
    except Exception as e:
        print(f"❌ Fehler bei ACF/PACF Analyse: {e}")
        return False

    # === Schritt 3: Liniendiagramme ===
    print("\n📈 SCHRITT 3: Liniendiagramme erstellen")
    print("-" * 40)
    try:
        Liniendiagramme.create_line_plots()
        print("✅ Liniendiagramme erstellt")
    except Exception as e:
        print(f"❌ Fehler bei Liniendiagrammen: {e}")
        return False

    # === Schritt 4: SARIMA Residuenanalyse ===
    print("\n🔍 SCHRITT 4: SARIMA Residuenanalyse")
    print("-" * 40)
    try:
        SARIMA_expanding_window_residuenanalyse.main()
        print("✅ SARIMA Residuenanalyse abgeschlossen")
    except Exception as e:
        print(f"❌ Fehler bei SARIMA Residuenanalyse: {e}")
        return False

    # === Zusammenfassung ===
    print("\n" + "="*80)
    print("🎉 ANALYSEPIPELINE ERFOLGREICH ABGESCHLOSSEN! 🎉")
    print(f"📁 Alle Ergebnisse befinden sich in: {config.OUTPUT_FOLDER}")
    print(f"   → Stationarität: {config.OUTPUT_STATIONARITAET}")
    print(f"   → ACF/PACF: {config.OUTPUT_ACF_PACF_PLOTS}")
    print(f"   → Liniendiagramme: {config.OUTPUT_LINIENDIAGRAMME}")
    print(f"   → SARIMA Residuen: {config.OUTPUT_SARIMA_RESIDUEN}")
    print(f"   → Evaluationsmetriken: {config.OUTPUT_EVALUATIONS_METRIKEN}")
    print("="*80)

    return True

def run_single_analysis(analysis_type):
    """
    Führt eine spezifische Analyse durch

    Parameters:
    - analysis_type: str - 'stationarity', 'acf_pacf', 'plots', 'sarima'
    """
    analysis_map = {
        'stationarity': ('Stationaritätsanalyse', stationaritätstest.main),
        'acf_pacf': ('ACF/PACF Analyse', acf_und_pacf.main),
        'plots': ('Liniendiagramme', Liniendiagramme.create_line_plots),
        'sarima': ('SARIMA Residuenanalyse', SARIMA_expanding_window_residuenanalyse.main)
    }

    if analysis_type not in analysis_map:
        print(f"❌ Unbekannter Analyse-Typ: {analysis_type}")
        print(f"Verfügbare Optionen: {list(analysis_map.keys())}")
        return False

    name, func = analysis_map[analysis_type]
    print(f"🚀 Starte {name}...")

    try:
        func()
        print(f"✅ {name} erfolgreich abgeschlossen")
        return True
    except Exception as e:
        print(f"❌ Fehler bei {name}: {e}")
        return False

# === Hauptausführung ===
if __name__ == "__main__":
    # Hier können verschiedene Modi ausgewählt werden

    # Vollständige Pipeline ausführen
    run_complete_analysis()

    # Oder spezifische Analyse (auskommentiert):
    # run_single_analysis('stationarity')
    # run_single_analysis('acf_pacf')
    # run_single_analysis('plots')
    # run_single_analysis('sarima')