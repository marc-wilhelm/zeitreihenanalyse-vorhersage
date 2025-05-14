import pandas as pd
import matplotlib.pyplot as plt
import pmdarima as pm
from statsmodels.graphics.tsaplots import plot_acf
import os
import sys

# Übergeordnetes Verzeichnis hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Liste der Zeitreihen
time_series_info = {
    "abakan": config.PATH_TS_ABAKAN_CLEAN,
    "berlin": config.PATH_TS_BERLIN_CLEAN,
    "angeles": config.PATH_TS_ANGELES_CLEAN
}

# Verzeichnisse vorbereiten
output_dir = os.path.join(os.path.dirname(__file__), "..", "results")
param_dir = os.path.join(output_dir, "model_parameters")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(param_dir, exist_ok=True)

# Hauptloop
for city, path in time_series_info.items():
    print(f"\n--- Bearbeite: {city} ---")

    # Daten laden
    df = pd.read_csv(path)
    df['Datum'] = pd.to_datetime(df['Datum'])
    df.set_index('Datum', inplace=True)
    df = df.sort_index()
    series = df['MonatlicheDurchschnittsTemperatur'].dropna()

    # Modell fitten
    model = pm.auto_arima(
        series,
        start_p=0, max_p=3,
        start_q=0, max_q=3,
        d=None,
        seasonal=True,
        m=12,
        start_P=0, max_P=3,
        start_Q=0, max_Q=3,
        D=None,
        trace=True,
        error_action='ignore',
        suppress_warnings=True,
        stepwise=False
    )

    print(model.summary())

    # Modellparameter extrahieren
    order = model.order
    seasonal_order = model.seasonal_order
    aic = model.aic()

    # In Python-Datei speichern
    param_file_path = os.path.join(param_dir, f"{city}_params.py")
    with open(param_file_path, "w") as f:
        f.write(f"name = '{city}'\n")
        f.write(f"order = {order}\n")
        f.write(f"seasonal_order = {seasonal_order}\n")
        f.write(f"aic = {aic}\n")

    # Differenzierte Zeitreihe berechnen
    d = order[1]
    D = seasonal_order[1]
    m = seasonal_order[3]
    differenced_series = series.copy()

    if d > 0:
        differenced_series = differenced_series.diff(d)
    if D > 0:
        differenced_series = differenced_series.diff(m * D)

    differenced_series = differenced_series.dropna()
    differenced_series.name = "Differenzierte Zeitreihe"

    # Speichern als CSV
    diff_out_path = os.path.join(output_dir, f"{city}_differenced.csv")
    differenced_series.to_csv(diff_out_path, header=True)

    # Residuen plotten
    resid = model.resid()
    plt.figure(figsize=(10, 4))
    plt.plot(resid)
    plt.title(f"Residuen - {city}")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{city}_residuals.png"))
    plt.close()

    # ACF der Residuen
    fig = plot_acf(resid)
    plt.title(f"ACF der Residuen - {city}")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{city}_acf_residuals.png"))
    plt.close()