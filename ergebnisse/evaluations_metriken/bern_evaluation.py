"""
AutoARIMA Evaluationsmetriken für Bern
Generiert am: 2025-05-19 15:34:48
"""

evaluation_metrics = {
    'stadt': 'bern',
    'order': (3, 0, 2),
    'seasonal_order': (0, 0, 0, 12),
    'aic': 6812.119656386244,
    'bic': 6849.777081454511,
    'generiert_am': '2025-05-19 15:34:48',
    'parameter_names': ['intercept', 'ar.L1', 'ar.L2', 'ar.L3', 'ma.L1', 'ma.L2', 'sigma2'],
    'parameter_values': [0.00040677613303944065, 1.3309557778753893, -0.32167308659244864, -0.373340077514682, -1.758958751421281, 0.7675198808708058, 4.087186144071231],
    't_values': [0.8908710610554834, 50.63932009843156, -7.167423334877774, -14.114086303731343, -94.85909196994045, 41.57359814598298, 30.345205836505794],
    'p_values': [0.37299834696745426, 0.0, 7.642243789272567e-13, 3.110209256263877e-45, 0.0, 0.0, 2.906405857819532e-202],
    'log_likelihood': -3399.059828193122,
    'n_observations': 1604,
    'significant_parameters': ['ar.L1', 'ar.L2', 'ar.L3', 'ma.L1', 'ma.L2', 'sigma2'],
}
# === Residuenanalyse nach Test des gefundenen SARIMA-Modells ===
# Folds ausgewertet: 5
# Durchschnittlicher Train-RMSE: 2.2643
# Durchschnittlicher Test-RMSE:  2.3736
# Durchschnittlicher Train-MSE:  5.1282
# Durchschnittlicher Test-MSE:   5.6478
# Durchschnittlicher Ljung-Box p-Wert (Lag 10): 0.2195
