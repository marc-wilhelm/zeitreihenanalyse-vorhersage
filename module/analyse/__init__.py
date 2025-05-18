# module/analyse/__init__.py

# Einzelne Analyse-Module importieren
from . import (
    StatistischerUeberblick,
    Stationaritätstest,
    AcfUndPacf,
    Liniendiagramme,
    CusumTest
)

# Hauptfunktion für komplette Analyse importieren
from .pipeline_analyse import run_complete_analysis, run_single_analysis

# Liste aller verfügbaren Module und Funktionen
__all__ = [
    'StatistischerUeberblick',
    'Stationaritätstest',
    'AcfUndPacf',
    'Liniendiagramme',
    'CusumTest',
    'run_complete_analysis',
    'run_single_analysis'
]