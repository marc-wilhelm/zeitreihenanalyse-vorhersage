#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hauptprogramm für die Datenvorbereitungs-Pipeline
"""

import sys
import os

# Zentrale Konfiguration importieren und Pfade initialisieren
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

import config
config.init_project_paths()

from module.datenvorbereitung import run_complete_preprocessing, run_single_preprocessing

def main():
    """
    Hauptfunktion - führt die Datenvorbereitungs-Pipeline durch

    KONFIGURATION: Hier können Sie einstellen, was ausgeführt werden soll
    """
    print("Starte Datenvorbereitungs-Pipeline...\n")

    # ========== KONFIGURATION - WAS SOLL AUSGEFÜHRT WERDEN? ==========

    # Option 1: Komplette Pipeline für alle Städte ausführen (Standard)
    mode = "complete"  # Ändern Sie das hier für andere Modi

    # Option 2: Nur spezifische Städte verarbeiten
    # mode = "abakan"         # Nur Abakan
    # mode = "berlin"         # Nur Berlin
    # mode = "angeles"        # Nur Angeles

    # ==================================================================

    if mode == "complete":
        print(" Führe komplette Datenvorbereitungspipeline aus...")
        run_complete_preprocessing()

    elif mode in ["abakan", "berlin", "angeles"]:
        print(f" Führe Datenvorbereitung nur für {mode} aus...")
        run_single_preprocessing(mode)

    else:
        print(f" Unbekannter Modus: {mode}")
        print("Verfügbare Modi: 'complete', 'abakan', 'berlin', 'angeles'")
        return

    print(" Datenvorbereitungs-Pipeline abgeschlossen!")

if __name__ == "__main__":
    main()