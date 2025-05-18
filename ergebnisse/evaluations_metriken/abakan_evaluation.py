"""
AutoARIMA Evaluationsmetriken für Abakan
Generiert am: 2025-05-18 13:23:15
"""

evaluation_metrics = {
    'stadt': 'abakan',
    'order': (2, 0, 1),
    'seasonal_order': (1, 0, 1, 12),
    'aic': 7650.585064321601,
    'bic': 7688.246854840586,
    'generiert_am': '2025-05-18 13:23:15',
    'parameter_names': ['intercept', 'ar.L1', 'ar.L2', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
    'parameter_values': [-4.959019491396941e-05, 1.05679596394322, -0.1693211119214285, -0.8935367596640843, 0.9989016625392952, -0.8554367829648419, 7.098026849208404],
    't_values': [-0.1990903491165601, 11.724156865349956, -7.495623579847706, -9.85289478663086, 2580.7712067342895, -53.4320328312059, 32.083198847039256],
    'p_values': [0.8421920704064746, 9.585062098394292e-32, 6.598390263014846e-14, 6.659767094501983e-23, 0.0, 0.0, 7.563347522039301e-226],
    'log_likelihood': -3818.2925321608004,
    'n_observations': 1604,
    'significant_parameters': ['ar.L1', 'ar.L2', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
}
# === Residuenanalyse nach Test des gefundenen SARIMA-Modells ===
# Folds ausgewertet: 5
# Durchschnittlicher Train-RMSE: 2.5836
# Durchschnittlicher Test-RMSE:  3.3926
# Durchschnittlicher Train-MSE:  6.6758
# Durchschnittlicher Test-MSE:   11.5530
# Durchschnittlicher Ljung-Box p-Wert (Lag 10): 0.9332
