import os
import sys
import pandas as pd
import pmdarima as pm
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# === Projektstruktur einbinden ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# === Speicherverzeichnisse ===
def setup_output_dirs():
    """Sicherstellen, dass die notwendigen Ausgabeverzeichnisse für universelles Modell existieren"""
    config.ensure_output_dirs()
    return config.OUTPUT_MODEL_PARAMETERS_UNIVERSELL, config.OUTPUT_EVALUATIONS_METRIKEN_UNIVERSELL

def main():
    """
    Hauptfunktion - Führt universelles AutoARIMA für alle Städte durch
    """
    print("🔄 Starte universelles AutoARIMA für alle Städte...")

    # Ausgabeverzeichnisse erstellen
    param_dir, eval_dir = setup_output_dirs()

    # Alle Zeitreihen vorbereiten
    all_series = {}
    for city in config.CITIES:
        print(f"\n🏙️ Lade Zeitreihe für {city.upper()}...")
        path = config.CITY_PATHS_CLEAN[city]
        df = pd.read_csv(path)
        df['Datum'] = pd.to_datetime(df['Datum'])
        df.set_index('Datum', inplace=True)
        df = df.sort_index()
        series = df['MonatlicheDurchschnittsTemperatur'].dropna()
        all_series[city] = series
        print(f"   📊 {len(series)} Beobachtungen geladen")
        print(f"   📅 Zeitraum: {series.index.min()} bis {series.index.max()}")

    # === Kandidatenparameter pro Stadt sammeln ===
    candidate_params = set()
    for city, series in all_series.items():
        print(f"\n--- Auto-ARIMA für {city} ---")
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
        candidate_params.add((tuple(model.order), tuple(model.seasonal_order)))
        print(f"   ✅ Beste Kandidatenparameter für {city}: SARIMA{model.order}x{model.seasonal_order}")

    # === Beste gemeinsame Kombination finden (kombinierter AIC/BIC) ===
    print("\n🔍 Finde beste gemeinsame Parameter...")
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
            print(f"   SARIMA{order}x{seasonal_order} | Kombinierter Score: {combined_score:.2f}")

            if combined_score < best_score:
                best_score = combined_score
                best_order = list(order); best_order[1] = 0  # d auf 0 setzen
                best_seasonal_order = list(seasonal_order); best_seasonal_order[1] = 0  # D auf 0 setzen
                best_models = current_models.copy()

        except Exception as e:
            print(f"   ⚠️ Fehler bei Modell {order} x {seasonal_order}: {e}")
            continue

    # === Gemeinsame Parameter speichern ===
    param_path = os.path.join(param_dir, "gemeinsame_parameter.py")
    with open(param_path, "w", encoding="utf-8") as f:
        f.write('"""\n')
        f.write(f'Universelle SARIMA-Parameter für alle Städte\n')
        f.write(f'Generiert am: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write('"""\n\n')
        f.write(f"order = {tuple(best_order)}\n")
        f.write(f"seasonal_order = {tuple(best_seasonal_order)}\n")
        f.write(f"kombinierter_score = {best_score}\n")
    print(f"\n💾 Gemeinsame Parameter gespeichert: {param_path}")
    print(f"   ✅ Beste universelle Parameter: SARIMA{tuple(best_order)}x{tuple(best_seasonal_order)}")

    # === Evaluation je Stadt speichern ===
    print("\n📊 Speichere Evaluationsmetriken für jede Stadt...")
    for city, model in best_models.items():
        metrics = {
            "Stadt": city,
            "AIC": model.aic(),
            "BIC": model.bic(),
            "Universelles_Modell": True,
            "Gemeinsame_Parameter": {
                "order": tuple(best_order),
                "seasonal_order": tuple(best_seasonal_order)
            }
        }

        try:
            res = model.arima_res_
            metrics["parameter_names"] = res.params.index.tolist()
            metrics["t_values"] = res.tvalues.tolist()
            metrics["p_values"] = res.pvalues.tolist()

            # Signifikante Parameter (p < 0.05)
            significant_params = [
                name for name, p_val in zip(res.params.index, res.pvalues)
                if p_val < 0.05
            ]
            metrics["significant_parameters"] = significant_params

        except Exception as e:
            print(f"   ⚠️ Keine t-/p-Werte für {city}: {e}")
            metrics["parameter_names"] = None
            metrics["t_values"] = None
            metrics["p_values"] = None

        eval_path = os.path.join(eval_dir, f"{city}_evaluation.py")
        with open(eval_path, "w", encoding="utf-8") as f:
            f.write('"""\n')
            f.write(f'Universelle AutoARIMA Evaluationsmetriken für {city.title()}\n')
            f.write(f'Generiert am: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write('"""\n\n')
            f.write("evaluation_metrics = {\n")
            for k, v in metrics.items():
                f.write(f"    '{k}': {repr(v)},\n")
            f.write("}\n")
        print(f"   ✅ Metriken für {city} gespeichert")

    # === Zusammenfassung ===
    print("\n" + "="*60)
    print("📋 ZUSAMMENFASSUNG - UNIVERSELLES AUTOARIMA")
    print("="*60)
    print(f"Beste universelle Parameter für alle Städte:")
    print(f"SARIMA{tuple(best_order)}x{tuple(best_seasonal_order)}")
    print(f"Kombinierter Score (AIC+BIC): {best_score:.2f}")
    print("\nStadt-spezifische Metriken mit universellen Parametern:")
    for city, model in best_models.items():
        print(f"✅ {city.title():<10} | AIC: {model.aic():>8.2f} | BIC: {model.bic():>8.2f}")

    print(f"\n📁 Ergebnisse gespeichert in:")
    print(f"   • Universelle Parameter: {param_dir}")
    print(f"   • Evaluationsmetriken: {eval_dir}")
    print("="*60)

    return True

# === Direkter Aufruf ===
if __name__ == "__main__":
    main()