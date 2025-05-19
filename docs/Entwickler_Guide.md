# Entwickler Guide

Dieses Dokument enthält Richtlinien und Best Practices für Entwickler, die an diesem Projekt mitarbeiten.

## Git-Workflow

### Branches

Wir verwenden folgende Branch-Struktur:
- `main`: Stabile Version (nur über Pull Requests)
- `develop`: Entwicklungsumgebung (Basis für Feature-Branches)
- Feature-Branches: Nach dem Schema `feature/[stadtname]`
- Refactor-Branches: Nach dem Schema `refactor/[kontext]`

### Commit-Messages

Wir orientieren uns an der [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) Spezifikation:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Gebräuchliche Types:
- `fix`: Fehlerbehebung
- `feat`: Neue Funktionalität
- `docs`: Dokumentationsänderungen
- `chore`: Routineaufgaben, Wartung
- `refactor`: Code-Änderungen ohne Funktionsänderung
- `test`: Hinzufügen oder Korrigieren von Tests
- `style`: Formatierungsänderungen ohne Funktionsänderung

Beispiele:
```
feat(zeitreihe): Implementiere ARIMA-Modellierung für Berlin

fix: Korrigiere Behandlung fehlender Werte
```

### Umgang mit Merge-Konflikten

Bei signifikanten Unterschieden sollte eine Absprache mit dem entsprechenden Teammitglied erfolgen, bevor der Konflikt gelöst wird.

## Code-Standards

### Coding Style

Wir folgen [PEP 8](https://peps.python.org/pep-0008/) für Python-Code, mit einigen zusätzlichen Richtlinien:
- Max. Zeilenlänge: 88 Zeichen (Black-Standard)
- Einrückung: 4 Leerzeichen
- Docstrings: [Google-Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

### Benennungskonventionen

- Python-Dateinamen: `UpperCamelCase` (z.B. `AnalyzeTimeSeries.py`)
- Funktionen: `snake_case` (z.B. `data_preparation.py`)
- Variablen: `snake_case` (z.B. `temperature_data`)
- Konstanten: `UPPER_CASE_WITH_UNDERSCORES` (z.B. `MAX_ITERATIONS`)

### Code-Dokumentation

Alle Funktionen und Klassen müssen mit einem Docstring versehen werden:

```python
def ProcessTimeSeries(data, window_size=7):
    """
    Kurze einzeilige Beschreibung der Funktion.

    Ausführlichere Beschreibung der Funktion, die mehrere Zeilen umfassen kann.
    Hier solltest du den Zweck und die allgemeine Funktionsweise erklären.

    Args:
        data (pandas.DataFrame): Die Zeitreihendaten zum Verarbeiten
        window_size (int, optional): Größe des gleitenden Fensters. Default ist 7.

    Returns:
        pandas.DataFrame: Die verarbeiteten Zeitreihendaten

    Raises:
        ValueError: Wenn window_size kleiner als 1 ist
    """
    # Implementierung
    # Stichpunktartige Beschreibung neben entsprechender Codezeile
```

## Entwicklungsumgebung

### Setup

1. Python 3.12.x installieren
2. Repository klonen
3. Setup ausführen (siehe setup.sh oder setup.ps1)
4. Virtuelle Umgebung aktivieren und in der IDE als Standardinterpreter hinterlegen


