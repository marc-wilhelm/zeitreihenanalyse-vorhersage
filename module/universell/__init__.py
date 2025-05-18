# module/universell/__init__.py

# Einzelne universelle Module importieren
from . import UniAutoArima
from . import UniPrognoseMitRuecktransformation
from . import UniSarimaCvRes

# Hauptfunktion für komplette universelle Pipeline importieren
from .pipeline_universell import run_complete_universell_analysis, run_single_universell_analysis

# Liste aller verfügbaren Module und Funktionen
__all__ = [
    'UniAutoArima',
    'UniPrognoseMitRuecktransformation',
    'UniSarimaCvRes',
    'run_complete_universell_analysis',
    'run_single_universell_analysis'
]