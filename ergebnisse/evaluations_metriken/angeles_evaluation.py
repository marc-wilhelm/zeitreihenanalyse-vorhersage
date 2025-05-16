"""
AutoARIMA Evaluationsmetriken für Angeles
Generiert am: 2025-05-17 00:24:08
"""

evaluation_metrics = {
    'stadt': 'angeles',
    'order': (2, 1, 1),
    'seasonal_order': (1, 0, 1, 12),
    'aic': 1972.7504028473475,
    'bic': 2010.4078279156142,
    'generiert_am': '2025-05-17 00:24:08',
    'parameter_names': ['intercept', 'ar.L1', 'ar.L2', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
    'parameter_values': [-1.2587080466925437e-05, 0.3215558402368969, 0.15990997019004105, -0.9863164610018507, 0.9977949194190829, -0.8456474659340081, 0.2044163934297668],
    't_values': [-0.7927695227841297, 15.623963747504519, 6.942882865206775, -145.17820076409183, 931.8193385676457, -44.661241518819025, 31.437298275897284],
    'p_values': [0.4279121162585705, 4.999839860352619e-55, 3.841779627617821e-12, 0.0, 0.0, 0.0, 6.260800574075759e-217],
    'log_likelihood': -979.3752014236737,
    'n_observations': 1604,
    'significant_parameters': ['ar.L1', 'ar.L2', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
}
# === Residuenanalyse nach Test des gefundenen SARIMA-Modells ===
# Folds ausgewertet: 5
# Durchschnittlicher Train-RMSE: 0.4541
# Durchschnittlicher Test-RMSE:  0.6999
# Durchschnittlicher Train-MSE:  0.2062
# Durchschnittlicher Test-MSE:   0.4941
# Durchschnittlicher Ljung-Box p-Wert (Lag 10): 0.0964
