# Zeitreihenanalyse und Vorhersage

![Python Version](https://img.shields.io/badge/Python-3.12-blue)


## Thematischer Überblick


Im Rahmen dieses Projekts werden drei Zeitreihen mit historischen Temperaturdaten ([Quelle](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)) folgender Städte analysiert:

- **Abakan**, Russland
- **Berlin**, Deutschland
- **Angeles**, Philippinen

Das Hauptziel ist die korrekte Bereinigung und statistische Prüfung der Rohdaten, um eine fundierte Grundlage für die Zeitreihenanalyse zu schaffen. Darauf aufbauend werden präzise Vorhersagemodelle entwickelt, die monatliche Durchschnittstemperaturen für die kommenden 10 Perioden prognostizieren.

Der methodische Ansatz umfasst sowohl univariate Analysen für jede einzelne Stadt als auch einen übergreifenden Algorithmus, der robuste Vorhersagen für alle Temperaturreihen ermöglicht. Besonderer Wert wird auf die Stationaritätsprüfung, Saisonalitätsanalyse und statistische Validierung der Prognosemodelle gelegt.

> **Hinweis:** Weitere Informationen zum analytischen Vorgehen finden sich [hier](docs/Analyse_Vorgehen.md).


## Projekt-Anforderungen

- **Python 3.12.X** (neuere Versionen werden akutell nicht vom [pmdarima](https://pypi.org/project/pmdarima/)-Package unterstützt.
- **Virtuelle Umgebung** (werden durch Setup-Skripte erstellt - siehe [Installation](#installation))
- **Erforderliche Pakete** (in [requirements.txt](requirements.txt) spezifiziert)

> **Hinweis:** Weitere Informationen zu technischen Implementierungsdetails finden sich [hier](docs/Technische_Implementierungsdetails.md).

## Installation

### 1. Python 3.12.X installieren

Stelle sicher, dass eine Python 3.12.X Version auf deinem System (Windows / macOS / Linux) 
installiert ist.

Beispielsweise: Python 3.12.10 ([download](https://www.python.org/downloads/release/python-31210/))

### 2. Repository klonen

Öffne das Terminal deines Betriebssystems und navigiere zu dem Ordner, in dem du das Projekt ablegen möchtest. Du kannst mit dem `cd`-Befehl zwischen Verzeichnissen wechseln. Sobald du im gewünschten Ordner bist, führe die folgenden Befehle aus:

```bash
git clone git@github.com:marc-wilhelm/zeitreihenanalyse-vorhersage.git
cd zeitreihenanalyse-vorhersage
```

### 3. Setup ausführen

Nach dem erfolgreichen Klonen des Repositories hast du zwei Möglichkeiten: Du kannst entweder direkt im Terminal weiterarbeiten oder das geklonte Projekt in deiner 
bevorzugten IDE öffnen. Das Setup-Skript erstellt automatisch eine virtuelle Python-Umgebung und installiert alle benötigten Abhängigkeiten.

**Führe das entsprechende Setup-Skript für dein Betriebssystem aus:**

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

> **Hinweis:** Aus Sicherheitsgründen kann es sein, dass Windows standardmäßig das Skript nicht ausführen lässt. Um das zu beheben verwende `Set-ExecutionPolicy 
> -ExecutionPolicy RemoteSigned -Scope CurrentUser` im Terminal.

**macOS / Linux oder Windows mit Bash:**
```bash
chmod +x setup.sh  # Ausführungsrechte setzen, falls nötig
./setup.sh
```

### 4. Virtuelle Umgebung aktivieren

#### Warum eine virtuelle Umgebung?

Die virtuelle Umgebung isoliert die Python-Pakete dieses Projekts von deinem System, um Konflikte mit anderen Projekten zu vermeiden. Es ist wie ein separater Arbeitsplatz für dieses spezifische Projekt mit seinen eigenen Werkzeugen.

#### IDE-Setup (empfohlen)

Es ist empfehlenswert, die erstellte virtuelle Umgebung als Standard-Interpreter in deiner IDE zu hinterlegen. Dadurch erkennt die IDE automatisch alle installierten Pakete und bietet bessere Code-Vervollständigung.

**Visual Studio Code:**

1. Öffne den Repository Ordner
2. Gib in die Suchleiste `> Python: Select Interpreter` ein
3. Wähle `Interpreterpfad eingeben`
4. Suche nach dem Pfad im .venv Ordner nach folgender Adresse oder gib diese direkt ein:
   - `.venv/Scripts/python.exe` (Windows) oder
   - `.venv/bin/python` (macOS/Linux)

**PyCharm/IntelliJ:**
   
1. Öffne den Repository Ordner als Projekt
2. Gehe zu Settings > Project Structure > Project > SDK > Add Python SDK from Disk > Existing Environment > Interpreter
3. Wähle den erstellten .venv Pfad aus mit Klick auf die drei Punkte `...`:
   - `.venv/Scripts/python.exe` (Windows) oder
   - `.venv/bin/python` (macOS/Linux).

**Manuelle Aktivierung im Terminal**

Falls du direkt im Terminal arbeiten möchtest, kannst du die virtuelle Umgebung mit folgenden Befehlen aktivieren:

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux oder Windows mit Bash:**
```bash
source .venv/bin/activate
```


#### Troubleshooting - Globale Python Umgebungen

Es kann sein, dass trotz Setzen der virtuellen Python-Umgebung eine andere Python-Umgebung priorisiert wird (z.B. conda base). Bitte deaktiviere dementsprechend
diese globale Einstellung permanent oder temporär mit folgenden Codes:

**Conda Base temporär deaktivieren:**
```bash
# Conda Base-Umgebung verlassen
conda deactivate
```

**Conda Base permanent deaktivieren:**
```bash
# Automatische Aktivierung der Base-Umgebung beim Terminal-Start deaktivieren
conda config --set auto_activate_base false

# Überprüfung der Einstellung
conda config --show auto_activate_base
```

## Anwendung

### Ausführungsreihenfolge

Die Anwendung besteht aus mehreren Skripten, die in folgender Reihenfolge per terminal oder enstprechende IDE (z.B. [VSC](https://code.visualstudio.com/), 
[IntelliJ](https://www.jetbrains.com/de-de/ides/)) ausgeführt werden sollten:

#### Individuelle Modelle

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

   Bewertet die erstellten Modelle und generiert Vorhersagen mit Prognoseintervallen.
   ```
   python skripte/main_prognosebewertung.py
   ```

#### Universelle Modelle

Führe wie oben Schritt 1 und 2 aus. Anschließend noch:

3. **Universellephase - Modellierung & Prognose**

   Erstellt und trainiert die ARIMA/SARIMA-Modelle für jede Zeitreihe und bewertet die erstellten Modelle und generiert Vorhersagen mit Prognoseintervallen.
   ```
   python skripte/main_universell.py
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
│   ├── universell
│   │   ├── __init__.py
│   │   └── pipeline_universell.py
│   └── __init__.py
├── skripte/               # Ausführbare Skripte (Entry Point zu den Pipelines)
│   ├── main_analyse.py    
│   ├── main_datenvorbereitung.py
│   ├── main_modollierung.py
│   ├── main_prognosebewertung.py
│   └── main_universell.py
├── .gitignore             # Git-Ignorierte Dateien
├── .python-version        # Python-Versionsanforderung
├── .tool-versions         # Tool-Versionsanforderung
├── config.py              # Projektkonfiguration
├── LICENSE                # Lizenzinformationen
├── README.md              
├── requirements.txt       # Abhängigkeiten / Packages
├── setup.ps1              # Setup-Skript für Windows
└── setup.sh               # Setup-Skript für macOS/Linux
```

## Organisatorischer Workflow

Die Projektstruktur folgt einem modularen Pipeline-Ansatz, bei dem jede Analysephase als eigenständiges Modul organisiert ist. Die `__init__.py`-Dateien in jedem Unterordner von `module/` machen die entsprechenden Pipeline-Funktionen als Python-Packages importierbar, während die Main-Skripte in `skripte/` als Einstiegspunkte fungieren und die jeweiligen Pipelines ausführen.

Dieser Workflow ermöglicht es, jede Phase der Zeitreihenanalyse - von der Datenvorbereitung über die Analyse und Modellierung bis hin zur Prognosebewertung - 
unabhängig voneinander zu entwickeln und auszuführen. Ein Entwickler kann beispielsweise nur `main_analyse.py` ausführen, um die Analysephase zu testen, ohne die gesamte Pipeline (Datenvorbereitung bis Prognose) durchlaufen zu müssen.

Die modulare Struktur bietet entscheidende Vorteile:
1. Teammitglieder können parallel an verschiedenen Modulen arbeiten, ohne sich gegenseitig zu blockieren.
2. Das Debugging wird erheblich vereinfacht, da Fehler in isolierten Komponenten lokalisiert werden können.
3. Die klare Trennung der Verantwortlichkeiten ermöglicht eine einfache Erweiterung des Systems - neue Analysemethoden oder Modelle können als separate Module 
   hinzugefügt werden, ohne bestehende Funktionalitäten zu beeinträchtigen.

## Projekt-Funktionalitäten

Diese Projekt beinhaltet folgende Funktionen:

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
   - Prognoseintervallberechnung
   - Visualisierung der Ergebnisse
   - Rücktransformation differenzierter Zeitreihen

## Entwickler Guide

Für Entwickler, die zum Projekt beitragen möchten, haben wir einen [Entwickler-Guide](docs/Entwickler_Guide.md) erstellt. Hier finden sich unsere Best Practices, Code-Standards und Workflow-Guidelines.


## Mitwirkende

Dieses Projekt wurde im Rahmen der Veranstaltung "Vertiefung Business Analytics" bei Prof. Dr. Christian Menden entwickelt.

**Team MJM**
<table>
  <tr><td>Maike Knauer</td>     <td>6622007</td></tr>
  <tr><td>Johanna Kießling</td> <td>6622009</td></tr>
  <tr><td>Marc Wilhelm</td>     <td>6622005</td></tr>
</table>

> **Hinweis:** Ein abschließendes Fazit zum Projekt findet sich [hier](docs/Fazit.md).

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.