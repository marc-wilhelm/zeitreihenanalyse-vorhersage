def install_required_packages():
    """
    Überprüft alle Pakete in requirements.txt und installiert fehlende Pakete.
    Verwendet importlib.metadata statt pkg_resources (deprecated).
    """
    import subprocess
    import sys
    import importlib.metadata

    print("Überprüfe und installiere benötigte Pakete...")

    # Versuche, die requirements.txt zu lesen
    try:
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("FEHLER: requirements.txt nicht gefunden!")
        return False

    # Überprüfe, welche Pakete installiert werden müssen
    packages_to_install = []
    for package in requirements:
        # Extrahiere Paketname (ohne Version)
        package_name = package.split('==')[0].split('>=')[0].split('<=')[0].strip()

        try:
            # Versuche das Paket zu importieren
            importlib.import_module(package_name.replace('-', '_'))
            print(f"✓ {package_name} ist bereits installiert.")
        except (ImportError, ModuleNotFoundError):
            # Alternativ: Überprüfe direkt mit importlib.metadata
            try:
                importlib.metadata.version(package_name)
                print(f"✓ {package_name} ist bereits installiert.")
            except importlib.metadata.PackageNotFoundError:
                # Wenn das Paket nicht gefunden wird, füge es zur Liste hinzu
                packages_to_install.append(package)
                print(f"✗ {package_name} muss installiert werden.")

    # Installiere fehlende Pakete
    if packages_to_install:
        print(f"\nInstalliere {len(packages_to_install)} fehlende Pakete...")
        for package in packages_to_install:
            print(f"Installiere {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ {package} erfolgreich installiert.")
            except subprocess.CalledProcessError:
                print(f"✗ FEHLER bei der Installation von {package}!")
                return False
        print("\nAlle benötigten Pakete wurden installiert.")
    else:
        print("\nAlle benötigten Pakete sind bereits installiert.")

    return True

# Beispiel für die Verwendung in main.py
if __name__ == "__main__":
    # Führe die Paketinstallation durch
    if install_required_packages():
        print("Setup abgeschlossen, führe Hauptprogramm aus...")
        # Hier kannst du dein Hauptprogramm aufrufen
        # main()
    else:
        print("Setup fehlgeschlagen. Bitte Fehler überprüfen.")