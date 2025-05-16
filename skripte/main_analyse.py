#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hauptprogramm für die Zeitreihenanalyse-Pipeline
Führt die komplette Analyse für alle drei Städte durch:
- Stationaritätsanalyse (ADF, Kruskal-Wallis, CUSUM)
- Visualisierungen (Liniendiagramme, ACF/PACF)
- SARIMA-Modellierung mit Cross-Validation
- Residuenanalyse
"""

import sys
import os

# Robuste Pfad-Lösung: Projektverzeichnis finden
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
os.chdir(project_root)

# Konfigurations- und Pipeline-Module importieren
import config
from module.analyse.pipeline_analyse import AnalysePipeline

def main():
    """
    Hauptfunktion - ruft die Analyse-Pipeline für alle drei Städte auf
    """

    print("Starte Zeitreihenanalyse-Pipeline...\n")

    # Pipeline-Instanz erstellen
    pipeline = AnalysePipeline()

    # Komplette Analyse für alle Städte durchführen
    pipeline.analyse_alle_staedte()

    print("✅ Zeitreihenanalyse-Pipeline abgeschlossen!")


if __name__ == "__main__":
    main()