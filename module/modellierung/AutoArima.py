import os
import sys
import pandas as pd
import pmdarima as pm
from datetime import datetime

# === Projektstruktur einbinden ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

def main():
    """
    Hauptfunktion - Führt AutoARIMA für alle Städte durch
    """
    # Sicherstellen, dass Ausgabeordner existieren
    config.ensure_output_dirs()

    # Ergebnisse sammeln
    results_summary = []

    # === Zeitreihenpfade ===
    time_series_info = config.CITY_PATHS_CLEAN

    # === Hauptloop ===
    for i, (city, path) in enumerate(time_series_info.items(), 1):
        print(f"\n[{i}/{len(time_series_info)}]  BEARBEITE: {city.upper()}")
        print("-" * 40)

        try:
            # Daten laden
            print(f"    Lade Zeitreihe...")
            df = pd.read_csv(path)
            df['Datum'] = pd.to_datetime(df['Datum'])
            df.set_index('Datum', inplace=True)
            df = df.sort_index()
            series = df['MonatlicheDurchschnittsTemperatur'].dropna()

            print(f"    {len(series)} Beobachtungen geladen")
            print(f"    Zeitraum: {series.index.min()} bis {series.index.max()}")

            # Auto-ARIMA fitten
            print(f"    Starte AutoARIMA...")
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

            print(f"    Bestes Modell: SARIMA{model.order}x{model.seasonal_order}")
            print(f"    AIC: {model.aic():.2f}, BIC: {model.bic():.2f}")

            # Parameter extrahieren, aber d und D manuell auf 0 setzen
            order = list(model.order)
            seasonal_order = list(model.seasonal_order)
            order[1] = 0
            seasonal_order[1] = 0

            # In Tupel konvertieren für konsistente Verwendung
            order_tuple = tuple(order)
            seasonal_order_tuple = tuple(seasonal_order)

            # === 1. Modellparameter speichern ===
            param_path = os.path.join(config.OUTPUT_MODEL_PARAMETERS, f"{city}_params.py")
            with open(param_path, "w", encoding="utf-8") as f:
                f.write(f'"""\n')
                f.write(f'AutoARIMA Modellparameter für {city.title()}\n')
                f.write(f'Generiert am: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
                f.write(f'"""\n\n')
                f.write(f"name = '{city}'\n")
                f.write(f"order = {order_tuple}\n")
                f.write(f"seasonal_order = {seasonal_order_tuple}\n")
                f.write(f"aic = {model.aic()}\n")
                f.write(f"bic = {model.bic()}\n")

            print(f"    Parameter gespeichert")

            # === 2. Evaluationsmetriken extrahieren ===
            metrics = {
                "stadt": city,
                "order": order_tuple,           # <-- KORRIGIERT: Verwendet modifizierte order
                "seasonal_order": seasonal_order_tuple,  # <-- KORRIGIERT: Verwendet modifizierte seasonal_order
                "aic": model.aic(),
                "bic": model.bic(),
                "generiert_am": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            try:
                res = model.arima_res_
                metrics.update({
                    "parameter_names": res.params.index.tolist(),
                    "parameter_values": res.params.tolist(),
                    "t_values": res.tvalues.tolist(),
                    "p_values": res.pvalues.tolist(),
                    "log_likelihood": res.llf,
                    "n_observations": res.nobs
                })

                # Signifikante Parameter (p < 0.05)
                significant_params = [
                    name for name, p_val in zip(res.params.index, res.pvalues)
                    if p_val < 0.05
                ]
                metrics["significant_parameters"] = significant_params

            except Exception as e:
                print(f"    Erweiterte Statistiken nicht verfügbar: {e}")
                metrics.update({
                    "parameter_names": None,
                    "t_values": None,
                    "p_values": None,
                    "significant_parameters": None
                })

            # Speichern als Python-Datei
            eval_path = os.path.join(config.OUTPUT_EVALUATIONS_METRIKEN, f"{city}_evaluation.py")
            with open(eval_path, "w", encoding="utf-8") as f:
                f.write('"""\n')
                f.write(f'AutoARIMA Evaluationsmetriken für {city.title()}\n')
                f.write(f'Generiert am: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
                f.write('"""\n\n')
                f.write("evaluation_metrics = {\n")
                for k, v in metrics.items():
                    f.write(f"    '{k}': {repr(v)},\n")
                f.write("}\n")

            print(f"    Evaluationsmetriken gespeichert")

            # Zusammenfassung für diese Stadt (auch hier modifizierte Parameter verwenden)
            results_summary.append({
                'stadt': city,
                'order': order_tuple,           # <-- KORRIGIERT
                'seasonal_order': seasonal_order_tuple,  # <-- KORRIGIERT
                'aic': round(model.aic(), 2),
                'bic': round(model.bic(), 2),
                'status': 'Erfolgreich'
            })

            print(f"    {city.title()} erfolgreich abgeschlossen!")

        except Exception as e:
            print(f"    Fehler bei {city}: {e}")
            results_summary.append({
                'stadt': city,
                'status': f'Fehler: {str(e)[:50]}...'
            })
            continue

    # === Zusammenfassung aller Ergebnisse ===
    print("\n" + "="*60)
    print(" ZUSAMMENFASSUNG - AUTOARIMA ERGEBNISSE")
    print("="*60)

    successful_cities = [r for r in results_summary if r['status'] == 'Erfolgreich']
    failed_cities = [r for r in results_summary if r['status'] != 'Erfolgreich']

    print(f" Erfolgreich: {len(successful_cities)}/{len(config.CITIES)} Städte")
    if failed_cities:
        print(f" Fehlgeschlagen: {len(failed_cities)}/{len(config.CITIES)} Städte")

    print("\nDetaillierte Ergebnisse:")
    for result in results_summary:
        status_icon = "✅" if result['status'] == 'Erfolgreich' else "❌"
        print(f"{status_icon} {result['stadt'].title():<10} | ", end="")

        if result.get('order'):
            print(f"SARIMA{result['order']}x{result['seasonal_order']} | ", end="")
            print(f"AIC: {result['aic']:>8.2f} | BIC: {result['bic']:>8.2f}")
        else:
            print(f"Status: {result['status']}")

    print(f"\n Ergebnisse gespeichert in:")
    print(f"   • Modellparameter: {config.OUTPUT_MODEL_PARAMETERS}")
    print(f"   • Evaluationsmetriken: {config.OUTPUT_EVALUATIONS_METRIKEN}")
    print("="*60)

    # Rückgabe für Pipeline-Integration
    return len(successful_cities) == len(config.CITIES)

# === Direkter Aufruf für Testing ===
if __name__ == "__main__":
    main()