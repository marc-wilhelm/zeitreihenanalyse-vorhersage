# module/datenbereinigung/__init__.py

# Alle Funktionen aus den einzelnen Modulen importieren
from .DatenEinlesen import DatenEinlesen
from .SpaltennamenKorrigieren import SpaltennamenKorrigieren
from .DatumFormatieren import DatumFormatieren
from .TemperaturUndDatumExtrahieren import TemperaturUndDatumExtrahieren
from .ZeitreiheAb1880 import ZeitreiheAb1880
from .NaNPruefen import NaNPruefen
from .DatentypenPruefen import DatentypenPruefen
from .DuplikatePruefen import DuplikatePruefen
from .BereinigteDatenSpeichern import BereinigteDatenSpeichern

# Pipeline importieren
from .pipeline_datenvorbereitung import DatenvorbereitungsPipeline

# Liste aller verfügbaren Funktionen
__all__ = [
    'DatenEinlesen',
    'SpaltennamenKorrigieren',
    'DatumFormatieren',
    'TemperaturUndDatumExtrahieren',
    'ZeitreiheAb1880',
    'NaNPruefen',
    'DatentypenPruefen',
    'DuplikatePruefen',
    'BereinigteDatenSpeichern',
    'DatenvorbereitungsPipeline'
]