import os
import sys
import pandas as pd
import pmdarima as pm
import numpy as np

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
param_dir = os.path.join(results_dir, "model_parameters_universell")
eval_dir = os.path.join(results_dir, "evaluations_metriken_universell")
os.makedirs(param_dir, exist_ok=True)
os.makedirs(eval_dir, exist_ok=True)

# === Alle Zeitreihen vorbereiten ===
all_series = {}
for city, path in time_series_info.items():
    df = pd.read_csv(path)
    df['Datum'] = pd.to_datetime(df['Datum'])
    df.set_index('Datum', inplace=True)
    df = df.sort_index()
    series = df['MonatlicheDurchschnittsTemperatur'].dropna()
    all_series[city] = series

# === Kandidatenparameter pro Stadt sammeln ===
candidate_params = set()
for city, series in all_series.items():
    print(f"\n--- auto_arima für {city} ---")
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
        trace=False,
        error_action='ignore',
        suppress_warnings=True,
        stepwise=False
    )
    candidate_params.add((tuple(model.order), tuple(model.seasonal_order)))

# === Beste gemeinsame Kombination finden (kombinierter AIC/BIC) ===
alpha = 0.5  # Gewicht AIC
beta = 0.5   # Gewicht BIC

best_score = np.inf
best_order = None
best_seasonal_order = None
best_models = {}

for order, seasonal_order in candidate_params:
    try:
        current_models = {}
        aic_sum = 0
        bic_sum = 0

        for city, series in all_series.items():
            model = pm.ARIMA(order=order, seasonal_order=seasonal_order).fit(series)
            current_models[city] = model
            aic_sum += model.aic()
            bic_sum += model.bic()

        combined_score = alpha * aic_sum + beta * bic_sum

        if combined_score < best_score:
            best_score = combined_score
            best_order = list(order); best_order[1] = 0  # d auf 0 setzen
            best_seasonal_order = list(seasonal_order); best_seasonal_order[1] = 0  # D auf 0 setzen
            best_models = current_models.copy()

    except Exception as e:
        print(f"⚠️ Fehler bei Modell {order} x {seasonal_order}: {e}")
        continue

# === Gemeinsame Parameter speichern ===
param_path = os.path.join(param_dir, "gemeinsame_parameter.py")
with open(param_path, "w") as f:
    f.write(f"order = {tuple(best_order)}\n")
    f.write(f"seasonal_order = {tuple(best_seasonal_order)}\n")
    f.write(f"kombinierter_score = {best_score}\n")

# === Evaluation je Stadt speichern ===
for city, model in best_models.items():
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
        print(f"⚠️ Keine t-/p-Werte für {city}: {e}")
        metrics["parameter_names"] = None
        metrics["t_values"] = None
        metrics["p_values"] = None

    eval_path = os.path.join(eval_dir, f"{city}_evaluation.py")
    with open(eval_path, "w", encoding="utf-8") as f:
        f.write("evaluation_metrics = {\n")
        for k, v in metrics.items():
            f.write(f"    '{k}': {repr(v)},\n")
        f.write("}\n")
