"""
Universelle AutoARIMA Evaluationsmetriken für Angeles
Generiert am: 2025-05-18 13:54:42
"""

evaluation_metrics = {
    'Stadt': 'angeles',
    'AIC': 2027.7442025051052,
    'BIC': 2065.401627573372,
    'Universelles_Modell': True,
    'Gemeinsame_Parameter': {'order': (2, 0, 1), 'seasonal_order': (1, 0, 1, 12)},
    'parameter_names': ['intercept', 'ar.L1', 'ar.L2', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
    't_values': [0.03168171054458729, 14.846551742296437, 6.422032114867724, -69.86631325267832, 592.4651203809024, -41.95254443704889, 31.669611756012586],
    'p_values': [0.9747258804359973, 7.32402393908572e-50, 1.3446704364734664e-10, 0.0, 0.0, 0.0, 4.0731739872794765e-220],
    'significant_parameters': ['ar.L1', 'ar.L2', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
}
# === Durchschnittliche Evaluationsmetriken ===
# Durchschnittlicher Train-RMSE: 0.4541
# Durchschnittlicher Test-RMSE:  0.6999
# Durchschnittlicher Train-MSE:  0.2062
# Durchschnittlicher Test-MSE:   0.4941
# Durchschnittlicher Ljung-Box p-Wert (Lag 10): 0.0964


# === Konfidenzintervall ===
# ar.L1: [0.262140, 0.369746]
# ar.L2: [0.107656, 0.222405]
# ar.S.L12: [-0.085256, 0.036857]
# ma.L1: [-2.068877, 0.075630]
# ma.S.L12: [-0.993071, -0.932867]
# sigma2: [-0.025671, 0.379916]
