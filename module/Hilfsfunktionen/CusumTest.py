import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.regression.linear_model import OLS

def cusum_test(df, target_column='MonatlicheDurchschnittsTemperatur', date_column='Datum'):
    """
    Führt den CUSUM-Test für eine gegebene Zeitreihe durch und plottet die Ergebnisse.
    
    Parameters:
    - df: pandas.DataFrame
        Der DataFrame, der die Zeitreihe enthält.
    - target_column: str
        Der Name der Spalte mit der Zielvariable. Standard: 'MonatlicheDurchschnittsTemperatur'.
    - date_column: str
        Der Name der Datumsspalte. Standard: 'Datum'.

    Returns:
    - None: Der CUSUM-Test wird durchgeführt und ein Plot angezeigt.
    """

    # 1. Stelle sicher, dass das Datum datetime ist
    df[date_column] = pd.to_datetime(df[date_column])

    # 2. Zielvariable y
    y = df[target_column].values

    # 3. Zeitvariable X definieren (numerisch)
    X = np.arange(len(y)).reshape(-1, 1)
    X = sm.add_constant(X)

    # 4. OLS-Modell anpassen
    model = OLS(y, X).fit()
    residuals = model.resid

    # 5. CUSUM berechnen
    mean_resid = np.mean(residuals)
    std_resid = np.std(residuals)
    cusum = np.cumsum((residuals - mean_resid) / std_resid)

    # 6. Grenzen definieren (z. B. ±3σ)
    upper_bound = 3
    lower_bound = -3

    # 7. Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df[date_column], cusum, label='CUSUM', color='blue')
    plt.axhline(y=upper_bound, color='red', linestyle='--', label='Upper bound (+3σ)')
    plt.axhline(y=lower_bound, color='red', linestyle='--', label='Lower bound (−3σ)')
    plt.title(f'CUSUM Test der Residuen – {target_column}')
    plt.xlabel('Datum')
    plt.ylabel('CUSUM')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
