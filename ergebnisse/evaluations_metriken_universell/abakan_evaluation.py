"""
Universelle AutoARIMA Evaluationsmetriken für Abakan
Generiert am: 2025-05-18 00:07:06
"""

evaluation_metrics = {
    'Stadt': 'abakan',
    'AIC': 7649.750321512712,
    'BIC': 7687.407746580979,
    'Universelles_Modell': True,
    'Gemeinsame_Parameter': {'order': (2, 0, 1), 'seasonal_order': (1, 0, 1, 12)},
    'parameter_names': ['intercept', 'ar.L1', 'ar.L2', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
    't_values': [-0.12495951299408278, 11.491473279838013, 0.47727517122505614, -263.60942445991265, 2417.7079923755855, -59.16081273403529, 31.711556891134595],
    'p_values': [0.9005556029864198, 1.4560724042434152e-30, 0.6331661887786346, 0.0, 0.0, 0.0, 1.0766299464823317e-220],
    'significant_parameters': ['ar.L1', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
}
# === Durchschnittliche Evaluationsmetriken ===
# Durchschnittlicher Train-RMSE: 2.5836
# Durchschnittlicher Test-RMSE:  3.3926
# Durchschnittlicher Train-MSE:  6.6758
# Durchschnittlicher Test-MSE:   11.5530
# Durchschnittlicher Ljung-Box p-Wert (Lag 10): 0.9332


# === Konfidenzintervall ===
# ar.L1: [-0.641465, 0.464215]
# ar.L2: [-0.101247, 0.115158]
# ar.S.L12: [-0.045609, 0.055158]
# ma.L1: [-0.292879, 0.808784]
# ma.S.L12: [-25.300757, 23.275263]
# sigma2: [-144.014537, 156.059521]
