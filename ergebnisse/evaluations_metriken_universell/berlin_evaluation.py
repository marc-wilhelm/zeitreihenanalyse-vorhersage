"""
Universelle AutoARIMA Evaluationsmetriken für Berlin
Generiert am: 2025-05-18 13:54:42
"""

evaluation_metrics = {
    'Stadt': 'berlin',
    'AIC': 6740.146937662722,
    'BIC': 6777.804362730989,
    'Universelles_Modell': True,
    'Gemeinsame_Parameter': {'order': (2, 0, 1), 'seasonal_order': (1, 0, 1, 12)},
    'parameter_names': ['intercept', 'ar.L1', 'ar.L2', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
    't_values': [-0.17726702396908617, 13.163197993473542, 0.29219864313896127, -220.50680446783855, 1036.134886454102, -67.33159082938262, 36.04488407603125],
    'p_values': [0.8592986516206789, 1.4290663198451074e-39, 0.7701347490055125, 0.0, 0.0, 0.0, 1.65865640423505e-284],
    'significant_parameters': ['ar.L1', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
}
# === Durchschnittliche Evaluationsmetriken ===
# Durchschnittlicher Train-RMSE: 1.9093
# Durchschnittlicher Test-RMSE:  2.5917
# Durchschnittlicher Train-MSE:  3.6455
# Durchschnittlicher Test-MSE:   6.7248
# Durchschnittlicher Ljung-Box p-Wert (Lag 10): 0.9252


# === Konfidenzintervall ===
# ar.L1: [-1.056583, 0.822441]
# ar.L2: [-0.089551, 0.365466]
# ar.S.L12: [-0.066775, 0.037808]
# ma.L1: [-0.583560, 1.301270]
# ma.S.L12: [-5.734608, 3.717024]
# sigma2: [-12.802467, 19.560712]
