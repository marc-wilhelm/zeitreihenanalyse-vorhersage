# module/analyse/pipeline_analyse.py

import os
import sys
import logging
from datetime import datetime

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
os.chdir(project_root)

import config

class AnalysePipeline:
    """
    Pipeline für die Zeitreihenanalyse aller Städte
    Führt schrittweise alle Analyse-Module aus
    """

    def __init__(self):
        self.cities = ["abakan", "berlin", "angeles"]
        self.setup_logging()
        self.create_directories()

    def setup_logging(self):
        """Logging-Konfiguration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('analyze_pipeline.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def create_directories(self):
        """Erstellt alle benötigten Verzeichnisse basierend auf config.py"""
        directories = [
            config.OUTPUT_FOLDER,
            os.path.join(config.OUTPUT_FOLDER, "stationarität-ergebnisse"),
            os.path.join(config.OUTPUT_FOLDER, "acf_pacf_plots"),
            os.path.join(config.OUTPUT_FOLDER, "sarima_residuen_auswertung"),
            os.path.join(config.OUTPUT_FOLDER, "model_parameters"),
            os.path.join(config.OUTPUT_FOLDER, "evaluations_metriken"),
            os.path.join(config.OUTPUT_FOLDER, "Liniendiagramme"),
            "daten/stationäre-daten"
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

        self.logger.info("✅ Verzeichnisstruktur erstellt")

    def stationaritaetsanalyse(self):
        """Schritt 1: Stationaritätsanalyse für alle Städte"""
        self.logger.info("🔄 Schritt 1: Starte Stationaritätsanalyse...")

        try:
            from . import stationaritätstest

            stadt_dateien = {
                "abakan": config.PATH_TS_ABAKAN_CLEAN,
                "berlin": config.PATH_TS_BERLIN_CLEAN,
                "angeles": config.PATH_TS_ANGELES_CLEAN
            }

            for city, path in stadt_dateien.items():
                self.logger.info(f"📊 Analysiere Stadt: {city}")
                stationaritätstest.analyse_city(city, path)

            self.logger.info("✅ Stationaritätsanalyse abgeschlossen")
            return True
        except Exception as e:
            self.logger.error(f"❌ Fehler bei Stationaritätsanalyse: {e}")
            return False

    def liniendiagramme_erstellen(self):
        """Schritt 2: Liniendiagramme für alle Städte"""
        self.logger.info("🔄 Schritt 2: Erstelle Liniendiagramme...")

        try:
            # Liniendiagramme.py als Modul ausführen
            import subprocess
            result = subprocess.run([sys.executable, "module/analyse/Liniendiagramme.py"],
                                    capture_output=True, text=True)

            if result.returncode == 0:
                self.logger.info("✅ Liniendiagramme erstellt")
                return True
            else:
                self.logger.error(f"❌ Fehler bei Liniendiagrammen: {result.stderr}")
                return False
        except Exception as e:
            self.logger.error(f"❌ Fehler bei Liniendiagrammen: {e}")
            return False

    def acf_pacf_plots_erstellen(self):
        """Schritt 3: ACF und PACF Plots für alle Städte"""
        self.logger.info("🔄 Schritt 3: Erstelle ACF/PACF Plots...")

        try:
            # acf_und_pacf.py als Modul ausführen
            import subprocess
            result = subprocess.run([sys.executable, "module/analyse/acf_und_pacf.py"],
                                    capture_output=True, text=True)

            if result.returncode == 0:
                self.logger.info("✅ ACF/PACF Plots erstellt")
                return True
            else:
                self.logger.error(f"❌ Fehler bei ACF/PACF Plots: {result.stderr}")
                return False
        except Exception as e:
            self.logger.error(f"❌ Fehler bei ACF/PACF Plots: {e}")
            return False

    def sarima_parameter_erstellen(self):
        """Erstellt SARIMA-Parameter für alle Städte"""
        self.logger.info("🔄 Erstelle SARIMA-Parameter...")

        # Standard-Parameter (können manuell angepasst werden)
        cities_params = {
            'abakan': {
                'order': (1, 1, 1),
                'seasonal_order': (1, 1, 1, 12)
            },
            'berlin': {
                'order': (1, 1, 1),
                'seasonal_order': (1, 1, 1, 12)
            },
            'angeles': {
                'order': (1, 1, 1),
                'seasonal_order': (1, 1, 1, 12)
            }
        }

        # Parameter-Dateien erstellen
        param_dir = os.path.join(config.OUTPUT_FOLDER, "model_parameters")
        for city, params in cities_params.items():
            param_file = os.path.join(param_dir, f"{city}_params.py")
            with open(param_file, 'w') as f:
                f.write(f"# SARIMA-Parameter für {city.capitalize()}\n")
                f.write(f"# Automatisch generiert - können manuell angepasst werden\n\n")
                f.write(f"order = {params['order']}\n")
                f.write(f"seasonal_order = {params['seasonal_order']}\n")
            self.logger.info(f"📝 Parameter für {city} erstellt")

    def sarima_analyse(self):
        """Schritt 4: SARIMA-Analyse mit Cross-Validation"""
        self.logger.info("🔄 Schritt 4: Starte SARIMA-Analyse...")

        try:
            # Erst Parameter erstellen
            self.sarima_parameter_erstellen()

            # SARIMA Analyse ausführen
            import subprocess
            result = subprocess.run([sys.executable, "module/analyse/SARIMA_expanding_window_residuenanalyse.py"],
                                    capture_output=True, text=True)

            if result.returncode == 0:
                self.logger.info("✅ SARIMA-Analyse abgeschlossen")
                return True
            else:
                self.logger.error(f"❌ Fehler bei SARIMA-Analyse: {result.stderr}")
                return False
        except Exception as e:
            self.logger.error(f"❌ Fehler bei SARIMA-Analyse: {e}")
            return False

    def analyse_alle_staedte(self):
        """Führt die komplette Analyse für alle Städte durch"""
        self.logger.info("🚀 Starte Zeitreihenanalyse für alle Städte...")
        self.logger.info("="*50)

        # Schritte der Pipeline
        schritte = [
            ("Stationaritätsanalyse", self.stationaritaetsanalyse),
            ("Liniendiagramme", self.liniendiagramme_erstellen),
            ("ACF/PACF Plots", self.acf_pacf_plots_erstellen),
            ("SARIMA-Analyse", self.sarima_analyse),
        ]

        erfolgreiche_schritte = 0

        for schritt_name, schritt_funktion in schritte:
            self.logger.info(f"\n📋 Führe aus: {schritt_name}")
            if schritt_funktion():
                erfolgreiche_schritte += 1
            else:
                self.logger.warning(f"⚠️ Schritt '{schritt_name}' fehlgeschlagen, Pipeline wird fortgesetzt...")

        # Abschluss-Log
        self.logger.info("\n" + "="*50)
        self.logger.info("🏁 Analyse-Pipeline abgeschlossen!")
        self.logger.info(f"✅ Erfolgreiche Schritte: {erfolgreiche_schritte}/{len(schritte)}")
        self.logger.info(f"📁 Alle Ergebnisse im Verzeichnis: {config.OUTPUT_FOLDER}")