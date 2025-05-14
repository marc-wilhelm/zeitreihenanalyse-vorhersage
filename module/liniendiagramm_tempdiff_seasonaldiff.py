import pandas as pd

import matplotlib.pyplot as plt
import sys
import os
import glob

# Übergeordnetes Verzeichnis hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config 



# Daten laden
df_angeles = pd.read_csv(config.PATH_TS_ANGELES_CLEAN)
df_angeles['Datum'] = pd.to_datetime(df_angeles['Datum'])

# Einmalige Differenzierung
temp_diff_angeles = df_angeles['MonatlicheDurchschnittsTemperatur'].diff(1)
df_temp_diff = df_angeles.copy()
df_temp_diff['Differenz'] = temp_diff_angeles

# Saisonale Differenzierung (nach einmaliger Differenzierung)
seasonal_diff_angeles = temp_diff_angeles.diff(12)
df_seasonal_diff = df_angeles.copy()
df_seasonal_diff['Differenz'] = seasonal_diff_angeles

# Zeitraum 1920 bis 1970
mask = (df_angeles['Datum'].dt.year >= 1920) & (df_angeles['Datum'].dt.year <= 1922)

# Plot erstellen
plt.figure(figsize=(14, 6))

# Einmalig differenzierte Zeitreihe
plt.subplot(2, 1, 1)
plt.plot(df_temp_diff.loc[mask, 'Datum'], df_temp_diff.loc[mask, 'Differenz'], label='Einmalige Differenzierung')
plt.title('Einmalig differenzierte Zeitreihe (1920–1970)')
plt.ylabel('Differenzierte Temperatur')
plt.grid(True)

# Saisonal differenzierte Zeitreihe
plt.subplot(2, 1, 2)
plt.plot(df_seasonal_diff.loc[mask, 'Datum'], df_seasonal_diff.loc[mask, 'Differenz'], label='Saisonale Differenzierung', color='orange')
plt.title('Saisonal differenzierte Zeitreihe (1920–1970)')
plt.xlabel('Jahr')
plt.ylabel('Differenzierte Temperatur')
plt.grid(True)

plt.tight_layout()
plt.show()
