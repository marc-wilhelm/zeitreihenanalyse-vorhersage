#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hauptprogramm für die Zeitreihenanalyse-Pipeline
"""

import sys
import os

# Zentrale Konfiguration importieren und Pfade initialisieren
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
os.chdir(project_root)

import config
config.init_project_paths()

from module.analyse import run_complete_analysis

def main():
    """
    Hauptfunktion - führt die komplette Zeitreihenanalyse-Pipeline durch
    """
    print("Starte Zeitreihenanalyse-Pipeline...\n")

    # Komplette Analyse für alle Städte durchführen
    run_complete_analysis()

    print("✅ Zeitreihenanalyse-Pipeline abgeschlossen!")

if __name__ == "__main__":
    main()