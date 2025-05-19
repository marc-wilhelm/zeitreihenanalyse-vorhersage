"""
Universelle AutoARIMA Evaluationsmetriken für Bern
Generiert am: 2025-05-19 21:40:55
"""

evaluation_metrics = {
    'Stadt': 'bern',
    'AIC': 6377.778622929415,
    'BIC': 6415.436047997682,
    'Universelles_Modell': True,
    'Gemeinsame_Parameter': {'order': (2, 0, 1), 'seasonal_order': (1, 0, 1, 12)},
    'parameter_names': ['intercept', 'ar.L1', 'ar.L2', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
    't_values': [-0.2822295951389944, 26.60685520310107, 1.541141132865528, -253.10363058142875, 1100.400602046627, -66.94231933512322, 30.00645476572778],
    'p_values': [0.7777674666894123, 5.654969593069916e-156, 0.12328244082343884, 0.0, 0.0, 0.0, 8.083889842439955e-198],
    'significant_parameters': ['ar.L1', 'ma.L1', 'ar.S.L12', 'ma.S.L12', 'sigma2'],
}
# === Durchschnittliche Evaluationsmetriken ===
# Durchschnittlicher Train-RMSE: 1.6935
# Durchschnittlicher Test-RMSE:  2.3492
# Durchschnittlicher Train-MSE:  2.8681
# Durchschnittlicher Test-MSE:   5.5295
# Durchschnittlicher Ljung-Box p-Wert (Lag 10): 0.7904


# === Konfidenzintervall ===
# ar.L1: [-0.932851, 2.040450]
# ar.L2: [-0.336384, 0.227088]
# ar.S.L12: [-0.097527, 0.021424]
# ma.L1: [-19.824819, 15.878033]
# ma.S.L12: [-1.042157, -0.980564]
# sigma2: [0.279941, 2.940222]
