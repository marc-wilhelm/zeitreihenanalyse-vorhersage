import numpy as np
import pandas as pd
from itertools import product
from statsmodels.tsa.statespace.sarimax import SARIMAX
from joblib import Parallel, delayed
import os
import sys
import time
import warnings
warnings.filterwarnings("ignore")

# Projektkonfiguration laden
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config

def evaluate_sarima_combination(train, order, seasonal_order, d=1, D=1, m=12):

    """
Diese Funktion nimmt eine Trainingszeitreihe und eine einzelne Kombination von SARIMA-Parametern (nicht-saisonale und saisonale Parameter) und erstellt ein SARIMA-Modell.
Sie berechnet das Modell und gibt den AIC-Wert zusammen mit den Parametern zurück.
Wenn ein Fehler auftritt (z. B. das Modell konvergiert nicht), gibt die Funktion np.inf zurück, um diese Kombination von Parametern als ungültig zu kennzeichnen.

    """
    try:
        model = SARIMAX(train,
                        order=(order[0], d, order[1]),
                        seasonal_order=(seasonal_order[0], D, seasonal_order[1], m),
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        result = model.fit(disp=False, low_memory=True)
        return (result.aic, (order[0], d, order[1]), (seasonal_order[0], D, seasonal_order[1], m))
    except:
        return (np.inf, None, None)

def find_best_sarima_parameters(ts_data, ts_name, pdq_range=None, seasonal_pdq_range=None, d=1, D=1, m=12, n_jobs=-1):
    """
    Finde die besten SARIMA-Parameter für eine Zeitreihe und speichere diese
    
    Parameter:
    ----------
    ts_data : pandas.Series
        Die zu analysierende Zeitreihe
    ts_name : str
        Name der Zeitreihe (für die Ausgabedatei)
    pdq_range : list, optional
        Liste von (p, q) Tupeln für den nicht-saisonalen Teil
    seasonal_pdq_range : list, optional
        Liste von (P, Q) Tupeln für den saisonalen Teil
    d : int, default=1
        Nicht-saisonale Differenzierungsordnung
    D : int, default=1
        Saisonale Differenzierungsordnung
    m : int, default=12
        Saisonalität (z.B. 12 für monatliche Daten)
    n_jobs : int, default=-1
        Anzahl der parallelen Jobs (-1 für alle verfügbaren Kerne)
    
    Returns:
    --------
    tuple
        (beste_order, beste_seasonal_order) - die optimalen SARIMA-Parameter
    """
    if pdq_range is None:
        pdq_range = [(p, q) for p in range(0, 3) for q in range(0, 3)]
    
    if seasonal_pdq_range is None:
        seasonal_pdq_range = [(P, Q) for P in range(0, 2) for Q in range(0, 2)]
    
    print(f"Starte SARIMA-Parametersuche für Zeitreihe '{ts_name}'...")
    print(f"Verwende {len(pdq_range) * len(seasonal_pdq_range)} Parameterkombinationen")
    
    combinations = list(product(pdq_range, seasonal_pdq_range)) #speichert alle mölichen Parameterkombinationen innerhalb der gewählten range
    
    start_time = time.time()
    results = Parallel(n_jobs=n_jobs)( #Parallele Berechnung für verschieden Paraberkominationen um Geschwindigkeit zu erhöhen
        delayed(evaluate_sarima_combination)(ts_data, order, seasonal_order, d, D, m)
        for order, seasonal_order in combinations # für jede Parameterkombination wird SARIMA-Modell ausgeführt und AIC wert berechnet 
    )
    duration = time.time() - start_time
    print(f"Parallele Parametersuche abgeschlossen in {duration:.2f} Sekunden")
    
    # Bestes Ergebnis filtern
    valid_results = [r for r in results if r[1] is not None] #enthält alle Ergebnisse für alle validen Paramterkombination
    if not valid_results:
        raise RuntimeError(f"Keine gültigen SARIMA-Modelle für {ts_name} gefunden.")
    
    best_result = min(valid_results, key=lambda x: x[0]) #filtert Paramterkombination mit niedrigstem AIC
    best_aic, best_order, best_seasonal_order = best_result
    
    print(f"Bestes Modell für {ts_name}: SARIMA{best_order}x{best_seasonal_order} mit AIC: {best_aic:.2f}")
    
    # Parameter in Datei speichern
    parameters = {
        'name': ts_name,
        'order': best_order,
        'seasonal_order': best_seasonal_order,
        'aic': best_aic
    }
    
    # Verzeichnis erstellen, falls nicht vorhanden
    os.makedirs('./parameter', exist_ok=True)
    
    # Parameter als Python-Modul speichern
    with open(f'./parameter/sarima_params_{ts_name}.py', 'w', encoding='utf-8') as f:
        f.write(f"# Automatisch generierte SARIMA-Parameter für {ts_name}\n")
        f.write(f"# Generiert am {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"name = '{ts_name}'\n")
        f.write(f"order = {best_order}\n")
        f.write(f"seasonal_order = {best_seasonal_order}\n")
        f.write(f"aic = {best_aic}\n")
    
    print(f"Parameter wurden in ./parameter/sarima_params_{ts_name}.py gespeichert")
    
    return best_order, best_seasonal_order

def main():
    print("Starte Bestimmung der optimalen SARIMA-Parameter...")
    
    # Zeitreihe aus Config laden
    stat_ts = config.seasonal_diff_abakan.squeeze()
    print(f"Zeitreihe geladen: {len(stat_ts)} Datenpunkte")
    
    # Parameter bestimmen
    try:
        best_order, best_seasonal_order = find_best_sarima_parameters(
            stat_ts, 
            'abakan',
            d=1, 
            D=1, 
            m=12
        )
        print("\nParameterbestimmung erfolgreich abgeschlossen.")
    except Exception as e:
        print(f"Fehler bei der Parameterbestimmung: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
