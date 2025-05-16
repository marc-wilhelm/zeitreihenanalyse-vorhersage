"""
AutoARIMA Evaluationsmetriken für Abakan
Generiert am: 2025-05-17 00:12:04
"""

evaluation_metrics = {
    'stadt': 'abakan',
    'order': (3, 0, 0),
    'seasonal_order': (1, 0, 1, 12),
    'aic': 7660.01825636895,
    'bic': 7697.680046887935,
    'generiert_am': '2025-05-17 00:12:04',
    'parameter_names': ['intercept', 'ar.L1', 'ar.L2', 'ar.L3', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
    'parameter_values': [-0.0015986574385440622, 0.1943900116446456, -0.0020763365655615583, 0.0027081604750139013, 0.9981299521184749, -0.8631954508158636, 6.730086839933276],
    't_values': [-0.8548972756790408, 9.541744867550326, -0.08742529539790624, 0.10483688544966735, 2154.4078141225973, -62.1773125209973, 33.43881658524616],
    'p_values': [0.39260801894358255, 1.4044903606962416e-21, 0.9303334635335286, 0.9165052409505277, 0.0, 0.0, 3.742371051760758e-245],
    'log_likelihood': -3823.009128184475,
    'n_observations': 1604,
    'significant_parameters': ['ar.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
}
# === Residuenanalyse nach Test des gefundenen SARIMA-Modells ===
# Folds ausgewertet: 5
# Durchschnittlicher Train-RMSE: 2.5850
# Durchschnittlicher Test-RMSE:  3.3924
# Durchschnittlicher Train-MSE:  6.6834
# Durchschnittlicher Test-MSE:   11.5514
# Durchschnittlicher Ljung-Box p-Wert (Lag 10): 0.9348
