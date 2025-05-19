#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hauptprogramm für die Zeitreihen-Prognosepipeline
"""

import sys
import os

# Zentrale Konfiguration importieren und Pfade initialisieren
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

import config
config.init_project_paths()

from module.prognosebewertung import run_complete_forecasting, run_single_forecast

def main():
    """
    Hauptfunktion - führt die Zeitreihen-Prognosepipeline durch

    KONFIGURATION: Hier können Sie einstellen, was ausgeführt werden soll
    """
    print(" Starte Zeitreihen-Prognosepipeline...\n")

    # ========== KONFIGURATION - WAS SOLL AUSGEFÜHRT WERDEN? ==========

    # Modus auswählen
    mode = "complete"  # Ändern Sie dies für andere Modi

    # Mögliche Modi:
    # "complete"     - Prognosen für alle Städte
    # "single"       - Prognose für eine spezifische Stadt

    # Falls Sie "single" verwenden, geben Sie hier die Stadt an:
    single_city = "berlin"  # Optionen: "abakan", "berlin", "angeles"

    # Anzahl der Prognosemonate
    forecast_months = 10  # Ändern Sie dies nach Bedarf

    # ==================================================================

    print(f" Konfiguration:")
    print(f"   Modus: {mode}")
    if mode == "single":
        print(f"   Stadt: {single_city}")
    print(f"   Prognosemonate: {forecast_months}")
    print("\n" + "="*60)

    if mode == "complete":
        print(" Führe Prognosen für alle Städte durch...")
        success = run_complete_forecasting(forecast_steps=forecast_months)

        if success:
            print(" Alle Prognosen erfolgreich erstellt!")
        else:
            print(" Einige Prognosen sind fehlgeschlagen. Prüfen Sie die Ausgabe oben.")

    elif mode == "single":
        if single_city not in config.CITIES:
            print(f" Fehler: Stadt '{single_city}' ist nicht verfügbar.")
            print(f"Verfügbare Städte: {config.CITIES}")
            return

        print(f" Führe Prognose für {single_city.capitalize()} durch...")
        success = run_single_forecast(single_city, forecast_steps=forecast_months)

        if success:
            print(f" Prognose für {single_city.capitalize()} erfolgreich erstellt!")
        else:
            print(f" Prognose für {single_city.capitalize()} fehlgeschlagen.")

    else:
        print(f" Unbekannter Modus: {mode}")
        print("Verfügbare Modi: 'complete', 'single'")
        return

    print("\n Zeitreihen-Prognosepipeline abgeschlossen!")
    print("\n Ergebnisse finden Sie in:")
    print(f"   {os.path.join(config.OUTPUT_FOLDER, 'prognose_ergebnisse')}")

    # Zeige Übersicht der erstellten Dateien
    output_dir = os.path.join(config.OUTPUT_FOLDER, "prognose_ergebnisse")
    if os.path.exists(output_dir):
        print("\n Erstellte Dateien:")
        for file in sorted(os.listdir(output_dir)):
            print(f"    {file}")

if __name__ == "__main__":
    main()