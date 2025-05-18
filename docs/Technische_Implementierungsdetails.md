# Technische Implementierung: Zeitreihenanalyse-Projekt

## Überblick

Die technische Umsetzung unseres Zeitreihenanalyse-Projekts folgt modernen Softwareentwicklungsprinzipien und nutzt eine durchdachte Architektur, die Skalierbarkeit, Wartbarkeit und Reproduzierbarkeit gewährleistet. Das Projekt demonstriert, wie wissenschaftliche Datenanalyse und professionelle Softwareentwicklung erfolgreich kombiniert werden können.

## Git-Repository und Versionskontrolle

Wir implementierten eine professionelle Branch-Strategie mit `main` (stabile Versionen), `develop` (Integration) und Feature-Branches nach dem Schema `feature/[stadtname]`. Die Commit-Messages folgen der Conventional Commits Spezifikation für automatische Versionierung und klare Nachverfolgung.

## Python-Umgebung und Dependencies

Das Projekt unterstützt alle Python 3.12.x Versionen, wobei pmdarima-Kompatibilität der limitierende Faktor für neuere Python-Versionen ist. Unsere automatisierten Setup-Skripte (`setup.ps1`, `setup.sh`) erkennen intelligent die korrekte Python-Version und erstellen virtuelle Umgebungen automatisch. Die `requirements.txt` balanciert feste Versionen für kritische Packages mit flexiblen Anforderungen für Support-Libraries.

## Projektarchitektur

Das `config.py`-Modul implementiert zentrales Konfigurationsmanagement mit dynamischer Pfad-Initialisierung und automatischer Verzeichniserstellung. Jeder Verarbeitungsschritt ist als eigenständige Pipeline organisiert, wodurch modulare Entwicklung und unabhängige Ausführung ermöglicht wird.

## Automatisierte Verarbeitung

Die vier Hauptskripte bilden eine sequenzielle Pipeline, bei der jeder Schritt auf den Ergebnissen des vorherigen aufbaut. Loop-basierte Stadtverarbeitung gewährleistet konsistente Anwendung aller Operationen auf die drei Zeitreihen.

Das Projekt implementiert einen **Dual-Modellierungs-Ansatz**: Zunächst werden für jede Stadt individuelle, optimal angepasste SARIMA-Modelle entwickelt, die die spezifischen klimatischen Eigenschaften berücksichtigen. Parallel dazu entwickelten wir ein **universelles "One-fits-all" Modell**, das mit einem einzigen Parametersatz für alle drei Zeitreihen funktioniert. Unser innovativer Algorithmus durchsucht systematisch den Parameterraum und identifiziert über gewichtete AIC/BIC-Kriterien die optimalen universellen SARIMA-Parameter, die robust über alle klimatischen Bedingungen hinweg performen.

## Spezialisierte Python-Packages

Das Projekt nutzt ein durchdachtes Ecosystem spezialisierter Libraries. `pmdarima` ermöglicht Auto-ARIMA-Funktionalität, `statsmodels` liefert statistische Tests und SARIMA-Implementierungen, während `pandas` und `numpy` die Datenverarbeitungsgrundlage bilden. `matplotlib` und `seaborn` sorgen für umfassende Visualisierungen.

## Performance-Optimierungen

Unser Expanding Window Cross-Validation nutzt effiziente pandas-Operations mit DataFrame-Views statt Kopien. Die rechenintensive Auto-ARIMA-Optimierung (15-20 Minuten) implementiert persistentes Caching der Parameter, wodurch wiederholte Berechnungen vermieden werden.

## Reproduzierbarkeit

Die Kombination aus versionierter Umgebung, Google-Style Docstrings und modularer Architektur gewährleistet vollständige Reproduzierbarkeit. Jedes Hauptskript kann unabhängig für Debugging ausgeführt werden, während die Pfad-Abstraktion das System robust gegen verschiedene Deployment-Szenarien macht.