#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hauptprogramm für die Zeitreihenanalyse-Pipeline
"""

import sys
import os

# Zentrale Konfiguration importieren und Pfade initialisieren
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

import config
config.init_project_paths()

from module.analyse import run_complete_analysis, run_single_analysis

def main():
    """
    Hauptfunktion - führt die Zeitreihenanalyse-Pipeline durch

    KONFIGURATION: Hier können Sie einstellen, was ausgeführt werden soll
    """
    print("Starte Zeitreihenanalyse-Pipeline...\n")

    # ========== KONFIGURATION - WAS SOLL AUSGEFÜHRT WERDEN? ==========

    # Option 1: Komplette Pipeline ausführen (Standard)
    mode = "complete"  # Ändern Sie das hier für andere Modi

    # Option 2: Nur spezifische Analysen ausführen
    # mode = "statistical_overview"   # Nur Statistischer Überblick
    # mode = "stationarity"          # Nur Stationaritätstest
    # mode = "acf_pacf"              # Nur ACF/PACF Analyse
    # mode = "plots"                 # Nur Liniendiagramme

    # ==================================================================

    if mode == "complete":
        print("🚀 Führe komplette Analysepipeline aus...")
        run_complete_analysis()

    elif mode in ["statistical_overview", "stationarity", "acf_pacf", "plots"]:
        analysis_names = {
            "statistical_overview": "Statistischen Überblick",
            "stationarity": "Stationaritätsanalyse",
            "acf_pacf": "ACF/PACF Analyse",
            "plots": "Liniendiagramme"
        }
        print(f"📊 Führe nur {analysis_names[mode]} aus...")
        run_single_analysis(mode)

    else:
        print(f"❌ Unbekannter Modus: {mode}")
        print("Verfügbare Modi: 'complete', 'statistical_overview', 'stationarity', 'acf_pacf', 'plots'")
        return

    print("✅ Zeitreihenanalyse-Pipeline abgeschlossen!")

if __name__ == "__main__":
    main()