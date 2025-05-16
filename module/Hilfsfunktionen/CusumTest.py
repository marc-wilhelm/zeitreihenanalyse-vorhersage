import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.regression.linear_model import OLS

def cusum_test(df, target_column='MonatlicheDurchschnittsTemperatur', date_column='Datum', city=None, save_path=None):
    """
    Führt den CUSUM-Test für eine gegebene Zeitreihe durch und speichert den Plot, wenn save_path angegeben ist.

    Parameters:
    - df: pandas.DataFrame
    - target_column: str – Spaltenname mit den Werten
    - date_column: str – Spaltenname mit Datumsangaben
    - city: str – Name der Stadt für Plot-Titel
    - save_path: str or None – Wenn gesetzt, wird der Plot als PNG gespeichert

    Returns:
    - None
    """
    # Datum vorbereiten
    if date_column not in df.columns and date_column == df.index.name:
        date_values = df.index
    else:
        df[date_column] = pd.to_datetime(df[date_column])
        date_values = df[date_column]

    y = df[target_column].values
    X = np.arange(len(y)).reshape(-1, 1)
    X = sm.add_constant(X)
    model = OLS(y, X).fit()
    residuals = model.resid

    # CUSUM berechnen
    mean_resid = np.mean(residuals)
    std_resid = np.std(residuals)
    cusum = np.cumsum((residuals - mean_resid) / std_resid)

    upper_bound = 3
    lower_bound = -3

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(date_values, cusum, label='CUSUM', color='blue')
    plt.axhline(y=upper_bound, color='red', linestyle='--', label='Upper bound (+3σ)')
    plt.axhline(y=lower_bound, color='red', linestyle='--', label='Lower bound (−3σ)')
    plt.title(f'CUSUM Test der Residuen – {city}' if city else 'CUSUM Test')
    plt.xlabel('Datum')
    plt.ylabel('CUSUM')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
