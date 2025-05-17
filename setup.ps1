Write-Output "Starte Setup (Windows PowerShell)..."

# Definieren der erforderlichen Python-Version
$REQUIRED_VERSION = "3.12.10"

# Funktion zum Finden der richtigen Python-Installation
function Find-PythonVersion {
    # Versuche 1: Verwende py launcher (wenn verfügbar)
    try {
        $pyOutput = py -3.12 --version 2>&1
        if ($pyOutput -match $REQUIRED_VERSION) {
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
                if ($versionOutput -match "3.12") {
                    return $path
                }
            } catch {}
        }
    }

    # Versuche 3: Suche in PATH
    try {
        $python312Path = Get-Command python | Where-Object { $_.Version.ToString() -match "3.12" } | Select-Object -First 1 -ExpandProperty Source
        if ($python312Path) {
            return $python312Path
        }
    } catch {}

    # Keine passende Version gefunden
    return $null
}

# Python-Version ermitteln
$PYTHON_PATH = Find-PythonVersion

if ($null -eq $PYTHON_PATH) {
    Write-Error "Python $REQUIRED_VERSION konnte nicht gefunden werden. Bitte installieren Sie Python $REQUIRED_VERSION von:"
    Write-Error "https://www.python.org/downloads/release/python-31210/"
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

# Python-Version im venv prüfen
$VENV_VERSION = (python --version 2>&1).ToString()
Write-Output "Virtuelle Umgebung verwendet: $VENV_VERSION"

pip install --upgrade pip
pip install -r requirements.txt

Write-Output "Setup abgeschlossen."
Write-Output "Aktiviere das Environment mit:"
Write-Output ".\.venv\Scripts\Activate.ps1"