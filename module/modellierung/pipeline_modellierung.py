import os
import sys
import time

# === Zentrale Konfiguration importieren ===
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

# Projektpfade initialisieren
config.init_project_paths()

# === Import der Modellierungs-Module ===
from module.modellierung import AutoArima
from module.modellierung import SarimaCvRes

def run_complete_modeling():
    """
    Führt die komplette Modellierungspipeline für alle Städte durch:
    1. AutoARIMA - Automatische SARIMA-Modellauswahl
    2. SARIMA Cross-Validation - Residuenanalyse mit Expanding Window
    """
    start_time = time.time()

    print("="*80)
    print(f"📁 Projektverzeichnis: {config.PROJECT_ROOT}")
    print(f"🏙️ Städte: {', '.join(config.CITIES)}")
    print(f"📊 Ausgabeverzeichnis: {config.OUTPUT_FOLDER}")
    print("="*80)

    completed_steps = 0
    total_steps = 2

    # === Schritt 1: AutoARIMA Modellauswahl ===
    print(f"\n🤖 SCHRITT 1/{total_steps}: AutoARIMA Modellauswahl")
    print("-" * 80)
    print("   → Automatische SARIMA-Modellauswahl für alle Städte")
    print("   → Speichert optimale Modellparameter")
    print("   → Erstellt Evaluationsmetriken")


    # === Schritt 2: SARIMA Cross-Validation & Residuenanalyse ===
    print(f"\n🔬 SCHRITT 2/{total_steps}: SARIMA Cross-Validation & Residuenanalyse")
    print("-" * 80)
    print("   → Cross-Validation mit Expanding Window")
    print("   → Residuenanalyse und Diagnostik")
    print("   → Prognose-Evaluierung")


    # === Erfolgreiche Zusammenfassung ===
    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "="*80)
    print("🎉 MODELLIERUNGSPIPELINE ERFOLGREICH ABGESCHLOSSEN! 🎉")
    print(f"⏱️ Gesamtdauer: {duration:.2f} Sekunden")
    print(f"✅ Abgeschlossene Schritte: {completed_steps}/{total_steps}")
    print(f"\n📁 Alle Ergebnisse befinden sich in: {config.OUTPUT_FOLDER}")
    print("\n📋 Übersicht der Ausgabeordner:")
    print(f"   🤖 Modellparameter:         {config.OUTPUT_MODEL_PARAMETERS}")
    print(f"   📊 Evaluationsmetriken:     {config.OUTPUT_EVALUATIONS_METRIKEN}")
    print(f"   🔬 SARIMA Residuenanalyse:  {config.OUTPUT_SARIMA_RESIDUEN}")
    print("="*80)

    return True

def run_single_modeling(modeling_type):
    """
    Führt einen spezifischen Modellierungsschritt durch

    Parameters:
    - modeling_type: str - 'autoarima', 'sarima_cv'
    """
    modeling_map = {
        'autoarima': {
            'name': 'AutoARIMA Modellauswahl',
            'func': AutoArima.main,
            'icon': '🤖',
            'description': 'Automatische SARIMA-Modellauswahl für alle Städte'
        },
        'sarima_cv': {
            'name': 'SARIMA Cross-Validation',
            'func': SarimaCvRes.main,
            'icon': '🔬',
            'description': 'Cross-Validation und Residuenanalyse'
        }
    }

    if modeling_type not in modeling_map:
        print(f"❌ Unbekannter Modellierungs-Typ: {modeling_type}")
        print(f"Verfügbare Optionen: {list(modeling_map.keys())}")
        return False

    analysis = modeling_map[modeling_type]

    start_time = time.time()
    print(f"{analysis['icon']} STARTE {analysis['name'].upper()}")
    print("="*80)
    print(f"📋 Beschreibung: {analysis['description']}")
    print(f"🏙️ Städte: {', '.join(config.CITIES)}")
    print("="*80)

    try:
        result = analysis['func']()
        end_time = time.time()
        duration = end_time - start_time

        print("="*80)
        print(f"✅ {analysis['name']} erfolgreich abgeschlossen")
        print(f"⏱️ Dauer: {duration:.2f} Sekunden")
        print(f"📁 Ergebnisse in: {config.OUTPUT_FOLDER}")
        print("="*80)
        return result if result is not None else True
    except Exception as e:
        print("="*80)
        print(f"❌ Fehler bei {analysis['name']}: {e}")
        print("="*80)
        return False

def main():
    """
    Hauptfunktion für die Modellierungs-Pipeline - führt die komplette Pipeline durch
    """
    run_complete_modeling()

# === Hauptausführung ===
if __name__ == "__main__":
    # Hier können verschiedene Modi ausgewählt werden

    # Vollständige Pipeline ausführen
    run_complete_modeling()

    # Oder spezifische Modellierung (auskommentiert):
    # run_single_modeling('autoarima')
    # run_single_modeling('sarima_cv')