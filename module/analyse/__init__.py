# module/analyse/__init__.py

# Einzelne Analyse-Module importieren
from . import statistischer_überblick
from . import stationaritätstest
from . import acf_und_pacf
from . import liniendiagramme
from . import CusumTest

# Hauptfunktion für komplette Analyse importieren
from .pipeline_analyse import run_complete_analysis, run_single_analysis

# Liste aller verfügbaren Module und Funktionen
__all__ = [
    'statistischer_überblick',
    'stationaritätstest',
    'acf_und_pacf',
    'liniendiagramme',
    'CusumTest',
    'run_complete_analysis',
    'run_single_analysis'
]