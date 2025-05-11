import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
# Beispiel: Zeitreihe aus CSV laden
# Ersetze 'deine_datei.csv' durch deinen Dateinamen
# und 'Datum' sowie 'Wert' durch die tatsächlichen Spaltennamen
df = pd.read_csv(config.PATH_TS_ABAKAN_CLEAN, parse_dates=["Datum"], index_col="Datum")

# Plotten
plt.figure(figsize=(12, 6))
plt.plot(df, label='Zeitreihe', color='blue')
plt.title("Zeitreihenplot")
plt.xlabel("Datum")
plt.ylabel("Wert")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
