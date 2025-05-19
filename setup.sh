#!/bin/bash
echo "Starte Setup (macOS/Linux oder Windows mit Bash)..."

# Definieren der erforderlichen Python-Version
REQUIRED_MAJOR_MINOR="3.12"  # Akzeptiere jede 3.12.x Version
# Optional: Für exakte Version verwenden: REQUIRED_VERSION="3.12.10"

# Funktion zum Finden der richtigen Python-Installation
find_python_version() {
    # Versuche 1: Prüfe auf Python 3.12 in PATH
    if command -v python3.12 &>/dev/null; then
        python_version=$(python3.12 --version 2>&1)
        if [[ $python_version =~ $REQUIRED_MAJOR_MINOR ]]; then
            echo "Gefunden mit python3.12: $python_version" >&2
            echo "python3.12"
            return 0
        fi
    fi

    # Versuche 2: Prüfe auf python3 mit Version 3.12
    if command -v python3 &>/dev/null; then
        python_version=$(python3 --version 2>&1)
        if [[ $python_version =~ $REQUIRED_MAJOR_MINOR ]]; then
            echo "Gefunden mit python3: $python_version" >&2
            echo "python3"
            return 0
        fi
    fi

    # Versuche 3: Prüfe auf python mit Version 3.12
    if command -v python &>/dev/null; then
        python_version=$(python --version 2>&1)
        if [[ $python_version =~ $REQUIRED_MAJOR_MINOR ]]; then
            echo "Gefunden mit python: $python_version" >&2
            echo "python"
            return 0
        fi
    fi

    # Versuche 4: Prüfe pyenv, wenn verfügbar
    if command -v pyenv &>/dev/null; then
        # Suche nach verfügbaren 3.12.x Versionen
        available_312=$(pyenv versions 2>/dev/null | grep -E "^\s*3\.12\." | head -1 | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
        if [ -n "$available_312" ]; then
            echo "Gefunden mit pyenv: $available_312" >&2
            # Stelle sicher, dass pyenv die richtige Version verwendet
            pyenv local "$available_312" &>/dev/null
            echo "pyenv exec python"
            return 0
        fi
    fi

    # Versuche 5: Prüfe Homebrew Python (macOS)
    if [[ "$OSTYPE" == "darwin"* ]] && command -v brew &>/dev/null; then
        if [ -x "/opt/homebrew/bin/python3.12" ]; then
            python_version=$(/opt/homebrew/bin/python3.12 --version 2>&1)
            if [[ $python_version =~ $REQUIRED_MAJOR_MINOR ]]; then
                echo "Gefunden mit Homebrew: $python_version" >&2
                echo "/opt/homebrew/bin/python3.12"
                return 0
            fi
        fi
    fi

    # Keine passende Version gefunden
    return 1
}

# Python-Version ermitteln
PYTHON_CMD=$(find_python_version)

if [ -z "$PYTHON_CMD" ]; then
    echo "Fehler: Python $REQUIRED_MAJOR_MINOR konnte nicht gefunden werden."
    echo "Bitte installieren Sie Python 3.12.x von:"
    echo "https://www.python.org/downloads/"
    echo ""
    echo "Verfügbare Python-Versionen:"

    # Zeige verfügbare Python-Versionen
    for cmd in python python3 python3.12; do
        if command -v "$cmd" &>/dev/null; then
            version=$($cmd --version 2>&1)
            echo "  $cmd: $version"
        fi
    done

    # Zeige pyenv Versionen falls verfügbar
    if command -v pyenv &>/dev/null; then
        echo "  pyenv verfügbare Versionen:"
        pyenv versions 2>/dev/null | grep -E "3\." | head -5
    fi

    exit 1
fi

echo "Verwende Python-Befehl: $PYTHON_CMD"

# Conda deaktivieren (temporär)
unset CONDA_PREFIX
hash -r

# Virtuelles Environment erstellen, falls nicht existiert
if [ ! -d ".venv" ]; then
    $PYTHON_CMD -m venv .venv
    echo "Virtuelles Environment '.venv' erstellt."
fi

# Aktivieren und Pakete installieren
source .venv/bin/activate

# Python-Version im venv prüfen und anzeigen
VENV_VERSION=$(python --version 2>&1)
echo "Virtuelle Umgebung verwendet: $VENV_VERSION"

# Überprüfen ob die Version kompatibel ist
if [[ ! $VENV_VERSION =~ $REQUIRED_MAJOR_MINOR ]]; then
    echo "Warnung: Die Python-Version im venv ($VENV_VERSION) entspricht nicht der gewünschten Version ($REQUIRED_MAJOR_MINOR)"
fi

pip install --upgrade pip
pip install -r requirements.txt

echo "Setup abgeschlossen."
echo "Aktiviere das Environment mit:"
echo "source .venv/bin/activate"