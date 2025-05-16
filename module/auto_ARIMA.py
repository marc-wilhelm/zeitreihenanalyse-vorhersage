import os
import sys
import pandas as pd
import pmdarima as pm

# === Projektstruktur einbinden ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# === Zeitreihenpfade ===
time_series_info = {
    "abakan": config.PATH_TS_ABAKAN_CLEAN,
    "berlin": config.PATH_TS_BERLIN_CLEAN,
    "angeles": config.PATH_TS_ANGELES_CLEAN
}

# === Speicherverzeichnisse ===
base_dir = os.path.dirname(__file__)
results_dir = os.path.join(base_dir, "..", "results")
param_dir = os.path.join(results_dir, "model_parameters")
eval_dir = os.path.join(results_dir, "evaluations_metriken")
os.makedirs(param_dir, exist_ok=True)
os.makedirs(eval_dir, exist_ok=True)

# === Hauptloop ===
for city, path in time_series_info.items():
    print(f"\n--- Bearbeite: {city} ---")

    # Daten laden
    df = pd.read_csv(path)
    df['Datum'] = pd.to_datetime(df['Datum'])
    df.set_index('Datum', inplace=True)
    df = df.sort_index()
    series = df['MonatlicheDurchschnittsTemperatur'].dropna()

    # Auto-ARIMA fitten
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

    # Parameter extrahieren, aber d und D manuell auf 0 setzen
    order = list(model.order)
    seasonal_order = list(model.seasonal_order)
    order[1] = 0
    seasonal_order[1] = 0

    # === 1. Modellparameter speichern ===
    param_path = os.path.join(param_dir, f"{city}_params.py")
    with open(param_path, "w") as f:
        f.write(f"name = '{city}'\n")
        f.write(f"order = {tuple(order)}  \n")
        f.write(f"seasonal_order = {tuple(seasonal_order)}  \n")
        f.write(f"aic = {model.aic()}\n")

    # === 2. Evaluationsmetriken extrahieren ===
    metrics = {
        "Stadt": city,
        "AIC": model.aic(),
        "BIC": model.bic()
    }

    try:
        res = model.arima_res_
        metrics["parameter_names"] = res.params.index.tolist()
        metrics["t_values"] = res.tvalues.tolist()
        metrics["p_values"] = res.pvalues.tolist()
    except Exception as e:
        print(f"⚠️ Keine t-/p-Werte extrahierbar für {city}: {e}")
        metrics["parameter_names"] = None
        metrics["t_values"] = None
        metrics["p_values"] = None

    # Speichern als Python-Datei
    eval_path = os.path.join(eval_dir, f"{city}_evaluation.py")
    with open(eval_path, "w", encoding="utf-8") as f:
        f.write("evaluation_metrics = {\n")
        for k, v in metrics.items():
            f.write(f"    '{k}': {repr(v)},\n")
        f.write("}\n")
