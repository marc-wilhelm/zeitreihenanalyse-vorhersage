# module/datenvorbereitung/__init__.py

# Alle Funktionen aus dem datenvorbereitung Modul importieren
from .Bereinigung import (
    daten_einlesen,
    spaltennamen_korrigieren,
    datum_formatieren,
    temperatur_und_datum_extrahieren,
    zeitreihe_ab_1880,
    nan_pruefen,
    datentypen_pruefen,
    duplikate_pruefen,
    bereinigte_daten_speichern
)

# Pipeline-Funktionen importieren
from .pipeline_datenvorbereitung import run_complete_preprocessing, run_single_preprocessing

# Liste aller verfügbaren Funktionen
__all__ = [
    'daten_einlesen',
    'spaltennamen_korrigieren',
    'datum_formatieren',
    'temperatur_und_datum_extrahieren',
    'zeitreihe_ab_1880',
    'nan_pruefen',
    'datentypen_pruefen',
    'duplikate_pruefen',
    'bereinigte_daten_speichern',
    'run_complete_preprocessing',
    'run_single_preprocessing'
]