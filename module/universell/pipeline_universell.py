import os
import sys
import time

# === Zentrale Konfiguration importieren ===
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

# Projektpfade initialisieren
config.init_project_paths()

# === Import der universellen Module ===
from . import (
    UniAutoArima,
    UniPrognoseMitRuecktransformation,
    UniSarimaCvRes
)

def run_complete_universell_analysis():
    """
    Führt die komplette universelle Analysepipeline für alle Städte durch:
    1. Universelles AutoARIMA (Parameteroptimierung)
    2. Universelle SARIMA Cross-Validation mit Residuenanalyse
    3. Universelle SARIMA-Prognose mit Rücktransformation
    """
    start_time = time.time()

    print(" Starte universelle Analysepipeline...")
    print("="*60)

    # === Schritt 1: Universelles AutoARIMA ===
    try:
        UniAutoArima.main()
    except Exception as e:
        print(f" Fehler beim AutoARIMA: {e}")
        return False

    # === Schritt 2: Universelle Cross-Validation ===
    try:
        UniSarimaCvRes.main()
    except Exception as e:
        print(f" Fehler bei Cross-Validation: {e}")
        return False

    # === Schritt 3: Universelle Prognose ===
    try:
        UniPrognoseMitRuecktransformation.main()
    except Exception as e:
        print(f" Fehler bei Prognose: {e}")
        return False

    # === Zusammenfassung ===
    end_time = time.time()
    duration = end_time - start_time

    print("="*60)
    print(f" Pipeline abgeschlossen in {duration:.2f} Sekunden")
    print("="*60)

    return True

def run_single_universell_analysis(analysis_type):
    """
    Führt eine spezifische universelle Analyse durch

    Parameters:
    - analysis_type: str - 'auto_arima', 'cross_validation', 'prognose'
    """
    analysis_map = {
        'auto_arima': {
            'name': 'AutoARIMA',
            'func': UniAutoArima.main
        },
        'cross_validation': {
            'name': 'Cross-Validation',
            'func': UniSarimaCvRes.main
        },
        'prognose': {
            'name': 'Prognose',
            'func': UniPrognoseMitRuecktransformation.main
        }
    }

    if analysis_type not in analysis_map:
        print(f" Unbekannter Typ: {analysis_type}")
        print(f"Verfügbar: {list(analysis_map.keys())}")
        return False

    analysis = analysis_map[analysis_type]

    start_time = time.time()
    print(f" Starte {analysis['name']}...")

    try:
        analysis['func']()
        end_time = time.time()
        duration = end_time - start_time
        print(f" {analysis['name']} abgeschlossen ({duration:.2f}s)")
        return True
    except Exception as e:
        print(f" Fehler bei {analysis['name']}: {e}")
        return False

def main():
    """
    Hauptfunktion für die universelle Pipeline - führt die komplette Pipeline durch
    """
    run_complete_universell_analysis()

# === Hauptausführung ===
if __name__ == "__main__":
    main()