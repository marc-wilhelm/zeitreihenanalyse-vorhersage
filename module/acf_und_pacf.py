import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import sys
import os
from Hilfsfunktionen.DatenEinlesen import DatenEinlesen

# Übergeordnetes Verzeichnis damit config Modul gefunden wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config


# 1. Definiere die Eingabe- und Ausgabepfade
#file_path = config.PATH_TS_ANGELES_CLEAN
    # 2. Daten einlesen
#df = DatenEinlesen(file_path, sep= ",")
    
#if df is None:
    #print("Fehler beim Einlesen der Daten. Beende das Skript.")


def plot_acf_series(series, lags=40, title='ACF'):
    """
    Plottet die Autokorrelationsfunktion (ACF) einer Zeitreihe.
    
    Parameters:
    - series: pd.Series
        Zeitreihe (z. B. differenzierte Temperaturdaten)
    - lags: int
        Anzahl der zu betrachtenden Verzögerungen (Lags)
    - title: str
        Titel des Plots
    """
    plt.figure(figsize=(10, 5))
    plot_acf(series.dropna(), lags=lags, ax=plt.gca(), title=title)
    plt.tight_layout()
    plt.show()


def plot_pacf_series(series, lags=40, title='PACF'):
    """
    Plottet die partielle Autokorrelationsfunktion (PACF) einer Zeitreihe.
    
    Parameters:
    - series: pd.Series
        Zeitreihe (z. B. differenzierte Temperaturdaten)
    - lags: int
        Anzahl der zu betrachtenden Verzögerungen (Lags)
    - title: str
        Titel des Plots
    """
    plt.figure(figsize=(10, 5))
    plot_pacf(series.dropna(), lags=lags, ax=plt.gca(), method='ywm', title=title)
    plt.tight_layout()
    plt.show()
    
plot_acf_series(config.temp_diff_abakan, lags=30, title="ACF der differenzierten Temperatur")
plot_pacf_series(config.temp_diff_abakan, lags=30, title="PACF der differenzierten Temperatur")