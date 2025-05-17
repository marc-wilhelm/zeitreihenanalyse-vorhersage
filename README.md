# Zeitreihenanalyse und Vorhersage

![Python Version](https://img.shields.io/badge/Python-3.12-blue)


## Thematischer Überblick
Im Rahmen dieses Projekts sollen drei verschiedene Zeitreihen, die Temperaturdaten verschiedener Länder enthalten, analysiert werden. Darüber hinaus soll im Rahmen eines Forecasting Engineerings die zukünftige Entwicklung der jährlichen Durchschnittstemperaturen vorhergesagt werden. Dabei wird folgendes Vorgehen angewandt: Zunächst wird für jede einzelne Zeitreihe ein einzelnes passendes Prognosemodell gesucht. Anschließend wird darauf aufbauend ein übergreifender Algorithmus aufgesetzt, der eine passende Temperaturvorhersage für alle drei gewählten Länder liefert.


## Projekt-Anforderungen

- Python 3.12.X (neuere Versionen werden akutell nicht vom [pmdarima](https://pypi.org/project/pmdarima/)-Package unterstützt.
- Virtuelle Umgebung (wird durch Setup-Skripte erstellt)
- Erforderliche Pakete (in requirements.txt spezifiziert)


## Installation

### Python 3.12.X installieren

Stellen Sie sicher, dass eine Python 3.12.X Version auf Ihrem System (Windows / macOS / Linux) 
installiert ist.

Beispielsweise: Python 3.12.10 ([download](https://www.python.org/downloads/release/python-31210/))

### Repository klonen

```bash
git clone https://github.com/your-username/zeitreihenanalyse-vorhersage.git
cd zeitreihenanalyse-vorhersage
```

### Setup ausführen

#### Windows (PowerShell):
```powershell
.\setup.ps1
```

#### macOS / Linux oder Windows mit Bash:
```bash
chmod +x setup.sh  # Ausführungsrechte setzen, falls nötig
./setup.sh
```

### Virtuelle Umgebung aktivieren

#### Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

#### macOS/Linux oder Windows mit Bash:
```bash
source .venv/bin/activate
```


## Projektstruktur

```
zeitreihenanalyse-vorhersage/
├── archiv/                # Archivierte Daten und Skripte
├── daten/                 # Eingabedaten
│   ├── original-daten/    # Rohdaten
│   │   ├── zeitreihe_abakan.csv
│   │   ├── zeitreihe_angeles.csv
│   │   └── zeitreihe_berlin.csv
│   ├── bereinigte-daten/  # Bereinigte Daten
│   │   ├── bereinigt_zeitreihe_abakan.csv
│   │   ├── bereinigt_zeitreihe_angeles.csv
│   │   └── bereinigt_zeitreihe_berlin.csv
│   └── stationäre-daten/  # Stationäre Daten
├── docs/                  # Dokumentation
├── ergebnisse/            # Ausgabeverzeichnisse für Diagramme und Analysen
├── module/                # Python-Module
│   ├── datenbereinigung.py
│   └── hilfsfunktionen/
│       └── stationaritätstest.py
├── skripte/               # Ausführbare Skripte
├── .gitignore             # Git-Ignorierte Dateien
├── .python-version        # Python-Versionsanforderung
├── config.py              # Projektkonfiguration
├── main.py                # Hauptdatei zum Ausführen der Anwendung
├── README.md              # Diese Datei
├── requirements.txt       # Abhängigkeiten
├── setup.ps1              # Setup-Skript für Windows
└── setup.sh               # Setup-Skript für macOS/Linux
```


## Funktionalitäten

Diese Anwendung bietet folgende Funktionen:

1. **Datenbereinigung und -aufbereitung**
  - Behandlung fehlender Werte
  - Normalisierung und Transformation

2. **Zeitreihenanalyse**
  - Bestimmung der Stationarität
  - ACF und PACF Analyse
  - Modellidentifikation

3. **Univariate Zeitreihenmodelle**
  - ARIMA/SARIMA-Modellierung
  - Residuenanalyse
  - Modellvalidierung

4. **Multivariate Analyse**
  - Modellvergleich und -bewertung
  - Automatisierte Modellselektion

5. **Vorhersage**
  - Erstellung von Prognosen
  - Konfidenzintervallberechnung
  - Visualisierung der Ergebnisse


## Verwendung

```python
# Beispielcode zur Ausführung der Analyse
from module.pipeline_analyse import run_pipeline

# Pipeline für alle Städte ausführen
run_pipeline()

# Oder für eine spezifische Stadt
run_pipeline(city="berlin")
```


## Entwickler Guide

Für Entwickler, die zum Projekt beitragen möchten, haben wir einen [Entwickler-Guide](docs/DEVELOPER_GUIDE.md) erstellt. Hier findest du Best Practices, Code-Standards und Workflow-Guidelines.


## Mitwirkende

Dieses Projekt wurde im Rahmen der Veranstaltung "Vertiefung Business Analytics" bei Prof. Dr. Christian Menden entwickelt.

**Team:**
- Maike Knauer
- Johanna Kießling
- Marc Wilhelm


## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE)-Datei für Details.