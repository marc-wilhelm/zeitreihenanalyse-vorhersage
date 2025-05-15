import pandas as pd 

def DatentypenPruefen(df):
    """
    Prüft die Datentypen der Spalten.

    Diese Funktion gibt die Datentypen der Spalten im DataFrame aus und stellt sicher, dass die Spalte 'Datum' vom Typ `datetime`
    und die Spalte 'MonatlicheDurchschnittsTemperatur' vom Typ `float64` ist. Falls nötig, werden Konvertierungen durchgeführt.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, dessen Datentypen überprüft werden sollen.

    *Returns:*
    - pandas.DataFrame
        Der möglicherweise angepasste DataFrame mit korrekten Datentypen.
    """
    print(f"Datentypen der Spalten (vorher):\n{df.dtypes}\n")
    
    # Datum prüfen und ggf. konvertieren
    if df['Datum'].dtype != 'datetime64[ns]':
        print("⚠️ 'Datum' ist nicht vom Typ datetime. Versuche Umwandlung...")
        df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')
        if df['Datum'].isnull().any():
            print("❌ Fehler: Einige Werte in 'Datum' konnten nicht umgewandelt werden.")
        else:
            print("✅ 'Datum' erfolgreich in datetime umgewandelt.")
    
    # Temperatur prüfen und ggf. konvertieren
    if df['MonatlicheDurchschnittsTemperatur'].dtype != 'float64':
        print("⚠️ 'MonatlicheDurchschnittsTemperatur' ist nicht vom Typ float. Versuche Umwandlung...")
        df['MonatlicheDurchschnittsTemperatur'] = pd.to_numeric(df['MonatlicheDurchschnittsTemperatur'], errors='coerce')
        if df['MonatlicheDurchschnittsTemperatur'].isnull().any():
            print("❌ Fehler: Einige Werte in 'MonatlicheDurchschnittsTemperatur' konnten nicht umgewandelt werden.")
        else:
            print("✅ 'MonatlicheDurchschnittsTemperatur' erfolgreich in float64 umgewandelt.")

    print(f"\nDatentypen der Spalten (nachher):\n{df.dtypes}")
    return df
