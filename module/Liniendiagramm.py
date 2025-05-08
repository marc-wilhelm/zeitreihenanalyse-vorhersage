import pandas as pd
import matplotlib.pyplot as plt

# Beispiel: Zeitreihe aus CSV laden
# Ersetze 'deine_datei.csv' durch deinen Dateinamen
# und 'Datum' sowie 'Wert' durch die tatsächlichen Spaltennamen
df = pd.read_csv("./daten/bereinigte-daten/zeitreihe_berlin_bereinigt.csv", parse_dates=["Datum"], index_col="Datum")

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
