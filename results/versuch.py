import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Übergeordnetes Verzeichnis hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Lade den Datensatz
df_angeles = pd.read_csv(config.PATH_TS_ANGELES_CLEAN)
df_angeles['Datum'] = pd.to_datetime(df_angeles['Datum'])

# Filtere nur die Jahre 1950 bis 1959
df_decade = df_angeles[(df_angeles['Datum'].dt.year >= 1950) & (df_angeles['Datum'].dt.year <= 1959)]

# Plot
plt.figure(figsize=(14, 6))
plt.plot(df_decade['Datum'], df_decade['MonatlicheDurchschnittsTemperatur'], marker='o')
plt.title("Monatliche Durchschnittstemperatur in Los Angeles – 1950 bis 1959")
plt.xlabel("Jahr")
plt.ylabel("Temperatur (°C)")
plt.xticks(df_decade['Datum'][::3], df_decade['Datum'].dt.strftime('%b %Y')[::3], rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
