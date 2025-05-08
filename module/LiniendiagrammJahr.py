import pandas as pd
import matplotlib.pyplot as plt

# CSV einlesen (passe parse_dates und index_col ggf. an!)
df = pd.read_csv(
    "./daten/bereinigte-daten/zeitreihe_berlin_bereinigt.csv",
    parse_dates=["Datum"],
    index_col="Datum"
)

# Nur jeden 13. Wert behalten
df_reduced = df.iloc[::13]

# Plotten
plt.figure(figsize=(12, 6))
plt.plot(df_reduced, label='Jeder 13. Wert', color='blue', marker='o')
plt.title("Zeitreihenplot – jeder 13. Datenpunkt")
plt.xlabel("Datum")
plt.ylabel("Wert")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
