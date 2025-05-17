# Zeitreihenanalyse und Vorhersage

![Python Version](https://img.shields.io/badge/Python-3.12-blue)


## Thematischer Überblick

Im Rahmen dieses Projekts werden drei Zeitreihen mit historischen Temperaturdaten folgender Städte analysiert:

- **Abakan**, Russland
- **Berlin**, Deutschland
- **Angeles**, Philippinen

Das Hauptziel ist die korrekte Bereinigung und statistische Prüfung der Rohdaten, um eine fundierte Grundlage für die Zeitreihenanalyse zu schaffen. Darauf aufbauend werden präzise Vorhersagemodelle entwickelt, die monatliche Durchschnittstemperaturen für die kommenden 10 Perioden prognostizieren.

Der methodische Ansatz umfasst sowohl univariate Analysen für jede einzelne Stadt als auch einen übergreifenden Algorithmus, der robuste Vorhersagen für alle Temperaturreihen ermöglicht. Besonderer Wert wird auf die Stationaritätsprüfung, Saisonalitätsanalyse und statistische Validierung der Prognosemodelle gelegt.

> **Hinweis:** Weitere Informationen zum analytischen Vorgehen finden sich [hier](docs/Analyse_Vorgehen.md).


## Projekt-Anforderungen

- **Python 3.12.X** (neuere Versionen werden akutell nicht vom [pmdarima](https://pypi.org/project/pmdarima/)-Package unterstützt.
- **Virtuelle Umgebung** (werden durch Setup-Skripte erstellt - siehe [Installation](##installation))
- **Erforderliche Pakete** (in [requirements.txt](requirements.txt) spezifiziert)


## Installation

### 1. Python 3.12.X installieren

Stelle sicher, dass eine Python 3.12.X Version auf deinem System (Windows / macOS / Linux) 
installiert ist.

Beispielsweise: Python 3.12.10 ([download](https://www.python.org/downloads/release/python-31210/))

### 2. Repository klonen

```bash
git clone https://github.com/your-username/zeitreihenanalyse-vorhersage.git
cd zeitreihenanalyse-vorhersage
```

### 3. Setup ausführen

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

**macOS / Linux oder Windows mit Bash:**
```bash
chmod +x setup.sh  # Ausführungsrechte setzen, falls nötig
./setup.sh
```

### 4. Virtuelle Umgebung aktivieren

Es wird empfohlen das erstellte **venv** als Standard-Projekt Interpreter zu hinterlegen.
Das vorgehen ist je nach IDE abhängig. Die .exe ist unter **root > .venv > 
Scripts > 
python.exe** zu finden.

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux oder Windows mit Bash:**
```bash
source .venv/bin/activate
```

## Anwendung

### Ausführungsreihenfolge

Die Anwendung besteht aus mehreren Skripten, die in folgender Reihenfolge per terminal oder enstprechende IDE (z.B. [VSC](https://code.visualstudio.com/), 
[IntelliJ](https://www.jetbrains.com/de-de/ides/)) ausgeführt werden sollten:

1. **Datenvorbereitungsphase**

   Bereinigt und transformiert die Rohdaten für die weitere Verarbeitung.
   ```
   python skripte/main_datenvorbereitung.py
   ```

2. **Analyserphase**

   Führt Stationaritätstests durch und erstellt ACF/PACF-Plots zur Modellidentifikation.
   ```
   python skripte/main_analyse.py
   ```

3. **Modellierungsphase**

   Erstellt und trainiert die ARIMA/SARIMA-Modelle für jede Zeitreihe.
   ```
   python skripte/main_modellierung.py
   ```
   > **Hinweis:** Die Auto-ARIMA-Berechnung kann je nach Datenmenge und Hardware 15-20 Minuten dauern.

4. **Prognosebewertungsphase**

   Bewertet die erstellten Modelle und generiert Vorhersagen mit Konfidenzintervallen.
   ```
   python skripte/main_prognosebewertung.py
   ```

### Konfigurationsoptionen

Jedes Skript kann mit verschiedenen Parametern und Funktionen konfiguriert werden. Genaue Angaben können in den main-, pipeline- oder direkten Funktions-Dateien 
eingesehen werden.

## Projektstruktur

```
zeitreihenanalyse-vorhersage/
├── archiv/                # Archivierte Daten und Skripte
├── daten/                 
│   ├── bereinigte-daten/  # Bereinigte Daten
│   ├── original-daten/    # Rohdaten
│   └── stationäre-daten/  # Stationäre Daten
├── docs/                  # Dokumentation
├── ergebnisse/            # Ausgabeverzeichnisse für Diagramme und Analysen
├── module/                # Python-Module
│   ├── analyse
│   │   ├── __init__.py
│   │   └── pipeline_analyse.py
│   ├── datenvorbereitung
│   │   ├── __init__.py
│   │   └── pipeline_datenvorbereitung.py
│   ├── modollierung
│   │   ├── __init__.py
│   │   └── pipeline_modollierung.py
│   ├── prognosebewertung
│   │   ├── __init__.py
│   │   └── pipeline_prognosebewertung.py
│   └── __init__.py
├── skripte/               # Ausführbare Skripte (rufen entsprechende pipeline in module ab)
│   ├── main_analyse.py    
│   ├── main_datenvorbereitung.py
│   ├── main_modollierung.py
│   └── main_prognosebewertung.py
├── .gitignore             # Git-Ignorierte Dateien
├── .python-version        # Python-Versionsanforderung
├── config.py              # Projektkonfiguration
├── LICENSE                # Lizenzinformationen
├── README.md              
├── requirements.txt       # Abhängigkeiten / Packages
├── setup.ps1              # Setup-Skript für Windows
└── setup.sh               # Setup-Skript für macOS/Linux
```


## Funktionalitäten

Diese Anwendung bietet folgende Funktionen:

1. **Datenbereinigung und -aufbereitung**
   - Behandlung fehlender & falsch formatierter Werte
   - Datenfilterung & -anpassung
   - Typprüfung und -konvertierung
   - Duplikatserkennung
   - Extraktion relevanter Zeitreiheninformationen

2. **Zeitreihenanalyse**
   - Bestimmung der Stationarität durch Tests (ADF, KPSS)
   - ACF und PACF Analyse zur Modellidentifikation
   - Strukturbrucherkennung (CUSUM-Test)
   - Statistischer Überblick und Visualisierung

3. **Univariate Zeitreihenmodelle**
   - ARIMA/SARIMA-Modellierung
   - Residuenanalyse (Ljung-Box-Test)
   - Modellvalidierung (Expanding Window)
   - Statistische Signifikanzbewertung (t-Statistiken)

4. **Multivariate Analyse**
   - Modellvergleich und -bewertung (AIC, BIC, RMSE)
   - Automatisierte Modellselektion für optimale Parameterkombinationen
   - Robustheitsanalyse über verschiedene Zeitreihen

5. **Vorhersage**
   - Erstellung von Prognosen für zukünftige Perioden
   - Konfidenzintervallberechnung
   - Visualisierung der Ergebnisse
   - Rücktransformation differenzierter Zeitreihen

## Entwickler Guide

Für Entwickler, die zum Projekt beitragen möchten, haben wir einen [Entwickler-Guide](docs/DEVELOPER_GUIDE.md) erstellt. Hier findest du Best Practices, Code-Standards und Workflow-Guidelines.


## Mitwirkende

Dieses Projekt wurde im Rahmen der Veranstaltung "Vertiefung Business Analytics" bei Prof. Dr. Christian Menden entwickelt.

**Team MJM**
<table>
  <tr><td>Maike Knauer</td>     <td>6622007</td></tr>
  <tr><td>Johanna Kießling</td> <td>6622009</td></tr>
  <tr><td>Marc Wilhelm</td>     <td>6622005</td></tr>
</table>


## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.