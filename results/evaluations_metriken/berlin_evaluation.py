evaluation_metrics = {
    'Stadt': 'berlin',
    'AIC': 6995.4783050206115,
    'BIC': 7033.1357300888785,
    'parameter_names': ['intercept', 'ar.L1', 'ma.L1', 'ma.L2', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
    't_values': [-0.9207254347101506, 27.894941027572752, -53.24534882704122, 34.93521270086526, 785.5060022037865, -50.0617251088704, 36.22660451937348],
    'p_values': [0.35719379343250146, 3.0730350940149564e-171, 0.0, 2.1718346767235738e-267, 0.0, 0.0, 2.321325871541269e-287],
}
# === Residuenanalyse nach Test des gefundenen SARIMA-Modells ===
# Folds ausgewertet: 5
# Durchschnittlicher Train-RMSE: 1.9160
# Durchschnittlicher Test-RMSE:  2.5922
# Durchschnittlicher Train-MSE:  3.6711
# Durchschnittlicher Test-MSE:   6.7274
# Durchschnittlicher Ljung-Box p-Wert (Lag 10): 0.9326
