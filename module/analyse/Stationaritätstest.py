import os
import sys
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from scipy.stats import kruskal
from .CusumTest import cusum_test

# === Zentrale Konfiguration importieren ===
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

# Projektpfade initialisieren
config.init_project_paths()

def make_stationary_by_adf(series, city):
    """Führt ADF-Test durch, differenziert max. 2x und speichert Ergebnis als .py-Datei"""
    differencing_count = 0
    results = []

    while differencing_count < 2:
        result = adfuller(series.dropna())
        p_value = result[1]
        stat = result[0]
        critical = result[4]

        print(f"\n ADF-Test für {city} (Differenzierungsstufe: {differencing_count}):")
        print(f"   ADF Statistic: {stat:.5f} | p-Wert: {p_value:.5f}")

        results.append({
            "differenzierung": differencing_count,
            "adf_stat": stat,
            "p": p_value,
            "krit_1": critical["1%"],
            "krit_5": critical["5%"],
            "krit_10": critical["10%"]
        })

        if p_value <= 0.05:
            print(" Stationär.")
            break
        else:
            print(" Nicht stationär. Differenzierung wird durchgeführt...")
            series = series.diff().dropna()
            differencing_count += 1

    # === Ergebnisse in .py-Datei speichern ===
    file_path = os.path.join(config.OUTPUT_STATIONARITAET, f"adf_result_{city}.py")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Trendanalyse für {city.capitalize()}\n")

        r0 = results[0]
        f.write(f"adf_statistik_vor = {r0['adf_stat']:.5f}\n")
        f.write(f"p_wert_vor = {r0['p']:.5f}\n")
        f.write(f"kritischer_wert_0_01_vor = {r0['krit_1']:.5f}\n")
        f.write(f"kritischer_wert_0_05_vor = {r0['krit_5']:.5f}\n")
        f.write(f"kritischer_wert_0_10_vor = {r0['krit_10']:.5f}\n")

        if len(results) > 1:
            r1 = results[1]
            f.write("\n")
            f.write(f"adf_statistik_nach = {r1['adf_stat']:.5f}\n")
            f.write(f"p_wert_nach = {r1['p']:.5f}\n")
            f.write(f"kritischer_wert_0_01_nach = {r1['krit_1']:.5f}\n")
            f.write(f"kritischer_wert_0_05_nach = {r1['krit_5']:.5f}\n")
            f.write(f"kritischer_wert_0_10_nach = {r1['krit_10']:.5f}\n")
            f.write(f"d = 1\n")
        else:
            f.write(f"d = 0\n")

    print(f" ADF-Ergebnisse gespeichert unter: {file_path}")
    return series

def analyse_city(city, path):
    """Führt vollständige Stationaritätsanalyse für eine Stadt durch"""
    print(f"\n==============================")
    print(f" Stadt: {city}")
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
    df_stationary['Monat'] = df_stationary['Datum'].dt.month
    monatliche_daten = [group['MonatlicheDurchschnittsTemperatur'].values for _, group in df_stationary.groupby('Monat')]
    stat_vor, p_vor = kruskal(*monatliche_daten)
    has_seasonality = p_vor < 0.05
    print(f"\n Kruskal-Wallis-Test für {city} (vor saisonaler Differenzierung):")
    print(f"   Teststatistik: {stat_vor:.4f} | p-Wert: {p_vor:.5f}")

    D = 0
    p_nach = None
    if has_seasonality:
        print(" Saisonaler Effekt erkannt. Führe saisonale Differenzierung (.diff(12)) durch.")
        df_stationary['MonatlicheDurchschnittsTemperatur'] = df_stationary['MonatlicheDurchschnittsTemperatur'].diff(12)
        df_stationary = df_stationary.dropna()
        D = 1

        # === Schritt 3: Kruskal-Wallis-Test nach saisonaler Differenzierung ===
        df_stationary['Monat'] = df_stationary['Datum'].dt.month
        monatliche_daten = [group['MonatlicheDurchschnittsTemperatur'].values for _, group in df_stationary.groupby('Monat')]
        stat_nach, p_nach = kruskal(*monatliche_daten)
        still_seasonal = p_nach < 0.05
        print(f"\n Kruskal-Wallis-Test für {city} (nach saisonaler Differenzierung):")
        print(f"   Teststatistik: {stat_nach:.4f} | p-Wert: {p_nach:.5f}")

        if still_seasonal:
            print(f" WARNUNG: Zeitreihe {city} zeigt auch nach saisonaler Differenzierung noch Saisonalität.")
            print(f"   → Die Datei wird **nicht gespeichert**. Bitte manuell prüfen.")
            return
        else:
            print(f" Keine Saisonalität mehr nach Differenzierung für {city}. Speichere Zeitreihe.")
    else:
        print(f" Kein saisonaler Effekt festgestellt für {city}. Speichere direkt.")

    # === Speicherung der finalen Zeitreihe ===
    output_path = config.get_stationary_data_path(city)
    df_stationary = df_stationary[['Datum', 'MonatlicheDurchschnittsTemperatur']]
    df_stationary.to_csv(output_path, index=False)
    print(f" Stationäre Zeitreihe gespeichert unter: {output_path}")

    # === CUSUM-Test ===
    cusum_output_path = os.path.join(config.OUTPUT_STATIONARITAET, f"cusum_result_{city}.png")
    try:
        cusum_test(df_stationary, city=city, save_path=cusum_output_path)
        print(f" CUSUM-Plot gespeichert unter: {cusum_output_path}")
    except Exception as e:
        print(f" Fehler beim CUSUM-Test für {city}: {e}")

    # === Speichern von Kruskal-Wallis-Auswertung als Variablen ===
    result_path = os.path.join(config.OUTPUT_STATIONARITAET, f"kruskal_result_{city}.py")
    with open(result_path, "w", encoding="utf-8") as f:
        f.write(f"# Saisonalitätsanalyse für {city.capitalize()}\n")
        f.write(f"p_wert_vor = {p_vor:.5f}\n")
        f.write(f"p_wert_nach = {p_nach:.5f}\n" if p_nach is not None else "p_wert_nach = None\n")
        f.write(f"D = {D}\n")
    print(f" Kruskal-Ergebnis gespeichert unter: {result_path}")

def main():
    """Führt Stationaritätsanalyse für alle Städte durch"""
    print(" Stationaritätsanalyse wird gestartet...")

    for city in config.CITIES:
        path = config.CITY_PATHS_CLEAN[city]
        try:
            analyse_city(city, path)
        except Exception as e:
            print(f" Fehler bei Stadt {city}: {e}")

    print(f"\n Stationaritätsanalyse abgeschlossen.")
    print(f" Ergebnisse gespeichert in: {config.OUTPUT_STATIONARITAET}")

# === Hauptausführung ===
if __name__ == "__main__":
    main()