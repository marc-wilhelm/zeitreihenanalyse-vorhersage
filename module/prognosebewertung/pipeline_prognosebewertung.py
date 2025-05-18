import os
import sys
import time

# === Zentrale Konfiguration importieren ===
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

# Projektpfade initialisieren
config.init_project_paths()

# === Import der Prognose-Module ===
from . import PrognoseMitRuecktransformation

def run_single_forecast(city, forecast_steps=10):
    """
    Führt eine Prognose für eine einzelne Stadt durch

    Parameters:
    - city: str - Name der Stadt
    - forecast_steps: int - Anzahl der Prognosemonate

    Returns:
    - bool - True bei Erfolg, False bei Fehler
    """
    print(f"\n🔍 Erstelle Prognose für: {city.capitalize()}")
    return PrognoseMitRuecktransformation.run_forecast_for_city(city, forecast_steps)

def run_complete_forecasting(forecast_steps=10):
    """
    Führt die komplette Prognosepipeline für alle Städte durch

    Parameters:
    - forecast_steps: int - Anzahl der Prognosemonate

    Returns:
    - bool - True wenn alle Prognosen erfolgreich, False sonst
    """
    start_time = time.time()

    print("🚀 Starte komplette Prognosepipeline...")
    print(f"📁 Projektverzeichnis: {config.PROJECT_ROOT}")
    print(f"🏙️ Städte: {', '.join(config.CITIES)}")
    print(f"📊 Prognoseschritte: {forecast_steps} Monate")
    print("\n" + "="*80)

    successful_forecasts = 0
    failed_forecasts = []

    # Ausgabeordner erstellen
    output_dir = os.path.join(config.OUTPUT_FOLDER, "prognose_ergebnisse")
    os.makedirs(output_dir, exist_ok=True)

    # Prognosen für alle Städte erstellen
    for i, city in enumerate(config.CITIES, 1):
        print(f"\n📈 PROGNOSE {i}/{len(config.CITIES)}: {city.capitalize()}")
        print("-" * 50)

        success = PrognoseMitRuecktransformation.run_forecast_for_city(city, forecast_steps)
        if success:
            successful_forecasts += 1
        else:
            failed_forecasts.append(city)

    # Einfache Zusammenfassung für Pipeline
    end_time = time.time()
    duration = end_time - start_time

    print(f"\n✅ Pipeline abgeschlossen: {successful_forecasts}/{len(config.CITIES)} Prognosen erfolgreich in {duration:.2f}s")

    if failed_forecasts:
        print(f"❌ Fehlgeschlagene Prognosen: {failed_forecasts}")

    return successful_forecasts == len(config.CITIES)

def main():
    """
    Hauptfunktion für die Prognose-Pipeline - führt die komplette Pipeline durch
    """
    run_complete_forecasting()

# === Hauptausführung ===
if __name__ == "__main__":
    main()