#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hauptprogramm für die universelle Zeitreihenanalyse-Pipeline
Führt SARIMA-Modellierung mit gemeinsamen Parametern für alle Städte durch
"""

import sys
import os

# Zentrale Konfiguration importieren und Pfade initialisieren
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

import config
config.init_project_paths()

from module.universell import run_complete_universell_analysis, run_single_universell_analysis

def main():
    """
    Hauptfunktion - führt die universelle Zeitreihenanalyse-Pipeline durch

    KONFIGURATION: Hier können Sie einstellen, was ausgeführt werden soll
    """
    print("Starte universelle Zeitreihenanalyse-Pipeline...\n")

    # ========== KONFIGURATION - WAS SOLL AUSGEFÜHRT WERDEN? ==========

    # Option 1: Komplette universelle Pipeline ausführen (Standard)
    #mode = ["cross_validation", "prognose"]   # Ändern Sie das hier für andere Modi
    mode = "complete"

    # Option 2: Nur spezifische Analysen ausführen
    # mode = "auto_arima"        # Nur universelles AutoARIMA
    # mode = "cross_validation"  # Nur universelle Cross-Validation
    # mode = "prognose"          # Nur universelle Prognose mit Rücktransformation

    # Option 3: Mehrere Analysen kombinieren (einfach Liste verwenden!)
    # mode = ["auto_arima", "prognose"]           # Nur AutoARIMA + Prognose
    # mode = ["auto_arima", "cross_validation"]   # Nur AutoARIMA + Cross-Validation
    # mode = ["cross_validation", "prognose"]     # Nur Cross-Validation + Prognose

    # ==================================================================

    if mode == "complete":
        print("🚀 Führe komplette universelle Analysepipeline aus...")
        print("   1️⃣ AutoARIMA (Parameteroptimierung)")
        print("   2️⃣ Cross-Validation (Modellvalidierung)")
        print("   3️⃣ Prognose (mit Rücktransformation)")
        run_complete_universell_analysis()

    elif mode in ["auto_arima", "cross_validation", "prognose"]:
        analysis_names = {
            "auto_arima": "AutoARIMA",
            "cross_validation": "Cross-Validation",
            "prognose": "Prognose mit Rücktransformation"
        }
        print(f"📊 Führe nur {analysis_names[mode]} aus...")
        run_single_universell_analysis(mode)

    else:
        # Fallback für mehrere Modi oder unbekannte Modi
        if isinstance(mode, list):
            print(f"🔄 Führe mehrere Analysen aus: {mode}")
            for single_mode in mode:
                if single_mode in ["auto_arima", "cross_validation", "prognose"]:
                    print(f"\n▶️ Starte {single_mode}...")
                    run_single_universell_analysis(single_mode)
                else:
                    print(f"❌ Unbekannter Modus: {single_mode}")
        else:
            print(f"❌ Unbekannter Modus: {mode}")
            print("Verfügbare Modi:")
            print("  'complete'         - Komplette Pipeline")
            print("  'auto_arima'       - Nur AutoARIMA Parameteroptimierung")
            print("  'cross_validation' - Nur Cross-Validation und Residuenanalyse")
            print("  'prognose'         - Nur Prognose mit Rücktransformation")
            print("\nBeispiel für mehrere Modi: modes = ['auto_arima', 'prognose']")
            return

    print("\n✅ Universelle Zeitreihenanalyse-Pipeline abgeschlossen!")
    print("\n📋 Die universelle Pipeline hat folgende Vorteile:")
    print("   🔧 Ein Parametersatz für alle Städte")
    print("   ⚡ Effiziente Modellierung")
    print("   📊 Vergleichbare Ergebnisse")
    print("   🎯 Robuste Prognosen")

if __name__ == "__main__":
    main()