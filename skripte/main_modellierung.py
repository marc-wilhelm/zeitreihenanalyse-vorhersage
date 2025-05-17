#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hauptprogramm für die Zeitreihen-Modellierungspipeline
"""

import sys
import os

# Zentrale Konfiguration importieren und Pfade initialisieren
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

import config
config.init_project_paths()

from module.modellierung import run_complete_modeling, run_single_modeling

def main():
    """
    Hauptfunktion - führt die Zeitreihen-Modellierungspipeline durch

    KONFIGURATION: Hier können Sie einstellen, was ausgeführt werden soll
    """
    print("Starte Zeitreihen-Modellierungspipeline...\n")

    # ========== KONFIGURATION - WAS SOLL AUSGEFÜHRT WERDEN? ==========

    # Option 1: Komplette Pipeline ausführen (Standard)
    mode = "sarima_cv"  # Ändern Sie das hier für andere Modi

    # Option 2: Nur spezifische Schritte ausführen
    # mode = "autoarima"      # Nur AutoARIMA Modellauswahl
    # mode = "sarima_cv"      # Nur SARIMA Cross-Validation

    # ==================================================================

    if mode == "complete":
        print("🚀 Führe komplette Modellierungspipeline aus...")
        run_complete_modeling()

    elif mode in ["autoarima", "sarima_cv"]:
        analysis_names = {
            "autoarima": "AutoARIMA Modellauswahl",
            "sarima_cv": "SARIMA Cross-Validation"
        }
        print(f"🔧 Führe nur {analysis_names[mode]} aus...")
        run_single_modeling(mode)

    else:
        print(f"❌ Unbekannter Modus: {mode}")
        print("Verfügbare Modi: 'complete', 'autoarima', 'sarima_cv'")
        return

    print("✅ Zeitreihen-Modellierungspipeline abgeschlossen!")

if __name__ == "__main__":
    main()