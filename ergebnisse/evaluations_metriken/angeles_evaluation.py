"""
AutoARIMA Evaluationsmetriken für Angeles
Generiert am: 2025-05-19 15:29:44
"""

evaluation_metrics = {
    'stadt': 'angeles',
    'order': (2, 0, 1),
    'seasonal_order': (1, 0, 1, 12),
    'aic': 2027.7442025051052,
    'bic': 2065.401627573372,
    'generiert_am': '2025-05-19 15:29:44',
    'parameter_names': ['intercept', 'ar.L1', 'ar.L2', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
    'parameter_values': [1.1654156384802648e-06, 0.4061800900165722, 0.16895290999971502, -0.962899657449246, 0.99493258372272, -0.8202611330213396, 0.20272150046873133],
    't_values': [0.03168171054458729, 14.846551742296437, 6.422032114867724, -69.86631325267832, 592.4651203809024, -41.95254443704889, 31.669611756012586],
    'p_values': [0.9747258804359973, 7.32402393908572e-50, 1.3446704364734664e-10, 0.0, 0.0, 0.0, 4.0731739872794765e-220],
    'log_likelihood': -1006.8721012525526,
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
