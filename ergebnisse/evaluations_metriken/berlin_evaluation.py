"""
AutoARIMA Evaluationsmetriken für Berlin
Generiert am: 2025-05-18 13:29:07
"""

evaluation_metrics = {
    'stadt': 'berlin',
    'order': (1, 1, 2),
    'seasonal_order': (1, 0, 1, 12),
    'aic': 6782.348927726002,
    'bic': 6820.006352794269,
    'generiert_am': '2025-05-18 13:29:07',
    'parameter_names': ['intercept', 'ar.L1', 'ma.L1', 'ma.L2', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
    'parameter_values': [-2.6192514405578967e-06, 0.8814723951953949, -1.7591907128642905, 0.7635470998383126, 0.9990553307759479, -0.8746453020743412, 4.0256496554791115],
    't_values': [-0.35706199310319053, 32.01564506474657, -52.46440903376812, 24.148571610409547, 1929.9799419595504, -58.564729546155114, 44.35762888599747],
    'p_values': [0.7210453966043044, 6.60543095981888e-225, 0.0, 7.729139029233765e-129, 0.0, 0.0, 0.0],
    'log_likelihood': -3384.174463863001,
    'n_observations': 1604,
    'significant_parameters': ['ar.L1', 'ma.L1', 'ma.L2', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
}
# === Residuenanalyse nach Test des gefundenen SARIMA-Modells ===
# Folds ausgewertet: 5
# Durchschnittlicher Train-RMSE: 1.9160
# Durchschnittlicher Test-RMSE:  2.5921
# Durchschnittlicher Train-MSE:  3.6710
# Durchschnittlicher Test-MSE:   6.7272
# Durchschnittlicher Ljung-Box p-Wert (Lag 10): 0.9326
