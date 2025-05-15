import os
import sys
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from scipy.stats import kruskal
from module.Hilfsfunktionen.CusumTest import cusum_test

# === Projektpfad setzen ===
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import config


def make_stationary_by_adf(series, city):
    """Führt ADF-Test durch, differenziert max. 2x und speichert Ergebnis als .py-Datei (überschreibt bestehende)"""
    differencing_count = 0
    records = []

    while differencing_count < 2:
        result = adfuller(series.dropna())
        p_value = result[1]
        stat = result[0]
        critical = result[4]

        print(f"\n📊 ADF-Test für {city} (Differenzierungsstufe: {differencing_count}):")
        print(f"   ADF Statistic: {stat:.4f} | p-Wert: {p_value:.4f}")

        records.append({
            "Stadt": city,
            "Differenzierung": differencing_count,
            "ADF_Statistik": stat,
            "p_Wert": p_value,
            **{f"Krit_Wert_{k}": v for k, v in critical.items()}
        })

        if p_value <= 0.05:
            print("✅ Stationär.")
            break
        else:
            print("⚠️ Nicht stationär. Differenzierung wird durchgeführt...")
            series = series.diff().dropna()
            differencing_count += 1

    # Ergebnisse speichern (immer überschreiben)
    result_dir = os.path.join(project_root, "results", "stationarität-ergebnisse")
    os.makedirs(result_dir, exist_ok=True)
    adf_result_path = os.path.join(result_dir, f"adf_result_{city}.py")
    with open(adf_result_path, "w", encoding="utf-8") as f:
        f.write("adf_results = [\n")
        for row in records:
            f.write("    " + repr(row) + ",\n")
        f.write("]\n")

    return series


def check_seasonality(df, city, phase):
    """Führt Kruskal-Wallis-Test durch und speichert Ergebnis als .py-Datei (überschreibt bestehende Phase)"""
    df = df.copy()
    df['Datum'] = pd.to_datetime(df['Datum'])
    df['Monat'] = df['Datum'].dt.month

    monatliche_daten = [group['MonatlicheDurchschnittsTemperatur'].values
                        for _, group in df.groupby('Monat')]

    stat, p = kruskal(*monatliche_daten)
    print(f"\n📈 Kruskal-Wallis-Test für {city} ({phase}):")
    print(f"   Teststatistik: {stat:.4f} | p-Wert: {p:.4f}")

    # Ergebnis schreiben
    result_dir = os.path.join(project_root, "results", "stationarität-ergebnisse")
    os.makedirs(result_dir, exist_ok=True)
    kruskal_result_path = os.path.join(result_dir, f"kruskal_result_{city}.py")

    result_entry = {
        "Stadt": city,
        "Phase": phase,
        "Teststatistik": stat,
        "p_Wert": p
    }

    # Liste neu schreiben (beide Phasen sammeln, nicht anhängen)
    if os.path.exists(kruskal_result_path):
        with open(kruskal_result_path, "r", encoding="utf-8") as f:
            content = f.read()
        local_vars = {}
        exec(content, {}, local_vars)
        kruskal_results = local_vars.get("kruskal_results", [])
        # Überschreibe nur den aktuellen Phasen-Eintrag
        kruskal_results = [r for r in kruskal_results if r["Phase"] != phase]
    else:
        kruskal_results = []

    kruskal_results.append(result_entry)

    with open(kruskal_result_path, "w", encoding="utf-8") as f:
        f.write("kruskal_results = [\n")
        for row in kruskal_results:
            f.write("    " + repr(row) + ",\n")
        f.write("]\n")

    return p < 0.05


def analyse_city(city, path):
    print(f"\n==============================")
    print(f"🌆 Stadt: {city}")
    print(f"==============================")

    # === Daten laden ===
    df = pd.read_csv(path)
    df['Datum'] = pd.to_datetime(df['Datum'])
    df = df[['Datum', 'MonatlicheDurchschnittsTemperatur']].dropna()

    # === Schritt 1: ADF-Test ===
    series = df['MonatlicheDurchschnittsTemperatur']
    stationary_series = make_stationary_by_adf(series, city)
    df_stationary = df.copy()
    df_stationary['MonatlicheDurchschnittsTemperatur'] = stationary_series
    df_stationary = df_stationary.dropna()

    # === Schritt 2: Kruskal-Wallis-Test vor saisonaler Differenzierung ===
    has_seasonality = check_seasonality(df_stationary, city, phase="vor saisonaler Differenzierung")

    if has_seasonality:
        print("🔁 Saisonaler Effekt erkannt. Führe saisonale Differenzierung (.diff(12)) durch.")
        df_stationary['MonatlicheDurchschnittsTemperatur'] = df_stationary['MonatlicheDurchschnittsTemperatur'].diff(12)
        df_stationary = df_stationary.dropna()

        # === Schritt 3: Kruskal-Wallis-Test nach saisonaler Differenzierung ===
        still_seasonal = check_seasonality(df_stationary, city, phase="nach saisonaler Differenzierung")

        if still_seasonal:
            print(f"⚠️ WARNUNG: Zeitreihe {city} zeigt auch nach saisonaler Differenzierung noch Saisonalität.")
            print(f"   → Die Datei wird **nicht gespeichert**. Bitte manuell prüfen.")
            return
        else:
            print(f"✅ Keine Saisonalität mehr nach Differenzierung für {city}. Speichere Zeitreihe.")
    else:
        print(f"✅ Kein saisonaler Effekt festgestellt für {city}. Speichere direkt.")

    # === Speicherung der finalen Zeitreihe ===
    output_dir = os.path.join(project_root, "daten", "stationäre-daten")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"stationaere_zeitreihe_{city}.csv")
    df_stationary.to_csv(output_path, index=False)
    print(f"💾 Stationäre Zeitreihe gespeichert unter: {output_path}")

    # === Schritt 4: CUSUM-Test und PNG speichern ===
    
    cusum_output_path = os.path.join(project_root, "results", "stationarität-ergebnisse", f"cusum_result_{city}.png")
    try:
        cusum_test(df_stationary, city=city, save_path=cusum_output_path)
        print(f"🖼️ CUSUM-Plot gespeichert unter: {cusum_output_path}")
    except Exception as e:
        print(f"❌ Fehler beim CUSUM-Test für {city}: {e}")



# === Hauptausführung ===
if __name__ == "__main__":
    stadt_dateien = {
        "abakan": config.PATH_TS_ABAKAN_CLEAN,
        "berlin": config.PATH_TS_BERLIN_CLEAN,
        "angeles": config.PATH_TS_ANGELES_CLEAN
    }

    for city, path in stadt_dateien.items():
        try:
            analyse_city(city, path)
        except Exception as e:
            print(f"❌ Fehler bei Stadt {city}: {e}")
