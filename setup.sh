#!/bin/bash
echo "Starte Setup (macOS/Linux oder Windows mit Bash)..."

# Definieren der erforderlichen Python-Version
REQUIRED_VERSION="3.12.10"

# Funktion zum Finden der richtigen Python-Installation
find_python_version() {
    # Versuche 1: Prüfe auf Python 3.12 in PATH
    if command -v python3.12 &>/dev/null; then
        python_version=$(python3.12 --version 2>&1)
        if [[ $python_version == *"3.12"* ]]; then
            echo "python3.12"
            return 0
        fi
    fi

    # Versuche 2: Prüfe auf python3 mit Version 3.12
    if command -v python3 &>/dev/null; then
        python_version=$(python3 --version 2>&1)
        if [[ $python_version == *"3.12"* ]]; then
            echo "python3"
            return 0
        fi
    fi

    # Versuche 3: Prüfe pyenv, wenn verfügbar
    if command -v pyenv &>/dev/null; then
        if pyenv versions | grep -q "3.12"; then
            echo "pyenv exec python"
            # Stelle sicher, dass pyenv die richtige Version verwendet
            pyenv local 3.12 &>/dev/null
            return 0
        fi
    fi

    # Keine passende Version gefunden
    return 1
}

# Python-Version ermitteln
PYTHON_CMD=$(find_python_version)

if [ -z "$PYTHON_CMD" ]; then
    echo "Fehler: Python $REQUIRED_VERSION konnte nicht gefunden werden."
    echo "Bitte installieren Sie Python $REQUIRED_VERSION von:"
    echo "https://www.python.org/downloads/release/python-31210/"
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

# Python-Version im venv prüfen
VENV_VERSION=$(python --version 2>&1)
echo "Virtuelle Umgebung verwendet: $VENV_VERSION"

pip install --upgrade pip
pip install -r requirements.txt

echo "Setup abgeschlossen."
echo "Aktiviere das Environment mit:"
echo "source .venv/bin/activate"