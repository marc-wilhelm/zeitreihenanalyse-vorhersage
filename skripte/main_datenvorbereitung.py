#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hauptprogramm für die Datenvorbereitungs-Pipeline
"""

import sys
import os

# Robuste Pfad-Lösung: Eine Ebene hoch zum Projekt-Root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

# Konfigurations- und Pipeline-Module importieren
import config
from module.datenvorbereitung import DatenvorbereitungsPipeline

def main():
    """
    Hauptfunktion - ruft die Pipeline für alle drei Städte auf
    """
    print("Starte Datenvorbereitungs-Pipeline...\n")

    # Pipeline-Instanz erstellen
    pipeline = DatenvorbereitungsPipeline()

    # Berlin verarbeiten
    pipeline.verarbeite_datei(
        config.PATH_TS_BERLIN,
        config.PATH_TS_BERLIN_CLEAN,
        sep=";",
        decimal=","
    )

    # Angeles verarbeiten
    pipeline.verarbeite_datei(
        config.PATH_TS_ANGELES,
        config.PATH_TS_ANGELES_CLEAN,
        sep=";",
        decimal=","
    )

    # Abakan verarbeiten
    pipeline.verarbeite_datei(
        config.PATH_TS_ABAKAN,
        config.PATH_TS_ABAKAN_CLEAN,
        sep=";",
        decimal=","
    )

    print("\nDatenvorbereitungs-Pipeline abgeschlossen.")

if __name__ == "__main__":
    main()