Write-Output "Starte Setup (Windows PowerShell)..."

# Definieren der erforderlichen Python-Version
$REQUIRED_MAJOR_MINOR = "3.12"  # Akzeptiere jede 3.12.x Version
# Optional: Für exakte Version verwenden: $REQUIRED_VERSION = "3.12.10"

# Funktion zum Finden der richtigen Python-Installation
function Find-PythonVersion {
    # Versuche 1: Verwende py launcher (wenn verfügbar)
    try {
        $pyOutput = py -3.12 --version 2>&1
        if ($pyOutput -match $REQUIRED_MAJOR_MINOR) {
            Write-Output "Gefunden mit py launcher: $pyOutput"
            return "py -3.12"
        }
    } catch {}

    # Versuche 2: Suche nach Python 3.12 in typischen Installationsverzeichnissen
    $potentialPaths = @(
        "${env:LOCALAPPDATA}\Programs\Python\Python312\python.exe",
        "${env:PROGRAMFILES}\Python\Python312\python.exe",
        "${env:PROGRAMFILES(X86)}\Python\Python312\python.exe",
        "C:\Python312\python.exe"
    )

    foreach ($path in $potentialPaths) {
        if (Test-Path $path) {
            try {
                $versionOutput = & $path --version 2>&1
                if ($versionOutput -match $REQUIRED_MAJOR_MINOR) {
                    Write-Output "Gefunden in Pfad: $versionOutput ($path)"
                    return $path
                }
            } catch {}
        }
    }

    # Versuche 3: Suche in PATH
    try {
        $pythonCommands = Get-Command python* -ErrorAction SilentlyContinue
        foreach ($cmd in $pythonCommands) {
            try {
                $versionOutput = & $cmd.Source --version 2>&1
                if ($versionOutput -match $REQUIRED_MAJOR_MINOR) {
                    Write-Output "Gefunden in PATH: $versionOutput ($($cmd.Source))"
                    return $cmd.Source
                }
            } catch {}
        }
    } catch {}

    # Keine passende Version gefunden
    return $null
}

# Python-Version ermitteln
$PYTHON_PATH = Find-PythonVersion

if ($null -eq $PYTHON_PATH) {
    Write-Error "Python $REQUIRED_MAJOR_MINOR konnte nicht gefunden werden."
    Write-Error "Bitte installieren Sie Python 3.12.x von:"
    Write-Error "https://www.python.org/downloads/"
    Write-Output ""
    Write-Output "Verfügbare Python-Versionen:"
    try {
        py --list
    } catch {
        Write-Output "Py launcher nicht verfügbar"
    }
    exit 1
}

Write-Output "Verwende Python von: $PYTHON_PATH"

# Conda deaktivieren (temporär)
Remove-Item Env:CONDA_PREFIX -ErrorAction SilentlyContinue

# Virtuelles Environment erstellen, falls nicht existiert
if (!(Test-Path -Path ".venv")) {
    if ($PYTHON_PATH -eq "py -3.12") {
        & py -3.12 -m venv .venv
    } else {
        & $PYTHON_PATH -m venv .venv
    }
    Write-Output "Virtuelles Environment '.venv' erstellt."
}

# Aktivieren und Pakete installieren
.venv\Scripts\Activate.ps1

# Python-Version im venv prüfen und anzeigen
$VENV_VERSION = (python --version 2>&1).ToString()
Write-Output "Virtuelle Umgebung verwendet: $VENV_VERSION"

# Überprüfen ob die Version kompatibel ist
if ($VENV_VERSION -notmatch $REQUIRED_MAJOR_MINOR) {
    Write-Warning "Achtung: Die Python-Version im venv ($VENV_VERSION) entspricht nicht der gewünschten Version ($REQUIRED_MAJOR_MINOR)"
}

pip install --upgrade pip
pip install -r requirements.txt

Write-Output "Setup abgeschlossen."
Write-Output "Aktiviere das Environment mit:"
Write-Output ".\.venv\Scripts\Activate.ps1"