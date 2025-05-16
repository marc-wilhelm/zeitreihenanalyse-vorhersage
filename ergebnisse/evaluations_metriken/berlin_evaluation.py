"""
AutoARIMA Evaluationsmetriken für Berlin
Generiert am: 2025-05-17 00:18:17
"""

evaluation_metrics = {
    'stadt': 'berlin',
    'order': (0, 1, 1),
    'seasonal_order': (1, 0, 1, 12),
    'aic': 6843.238962872178,
    'bic': 6870.137123635225,
    'generiert_am': '2025-05-17 00:18:17',
    'parameter_names': ['intercept', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
    'parameter_values': [-2.7412615402452704e-06, -0.9896346018042939, 0.9971526120424006, -0.8759337905964002, 4.001753658515494],
    't_values': [-0.09423688836259635, -207.93262824500945, 1246.718950330383, -58.51175030842492, 39.70036765378293],
    'p_values': [0.9249209824694649, 0.0, 0.0, 0.0, 0.0],
    'log_likelihood': -3416.619481436089,
    'n_observations': 1604,
    'significant_parameters': ['ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
}
# === Residuenanalyse nach Test des gefundenen SARIMA-Modells ===
# Folds ausgewertet: 5
# Durchschnittlicher Train-RMSE: 1.9190
# Durchschnittlicher Test-RMSE:  2.5908
# Durchschnittlicher Train-MSE:  3.6825
# Durchschnittlicher Test-MSE:   6.7201
# Durchschnittlicher Ljung-Box p-Wert (Lag 10): 0.0905
