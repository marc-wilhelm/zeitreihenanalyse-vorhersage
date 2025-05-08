import pandas as pd



def DatumFormatieren(df, datums_spalte='Datum'):
    """
    Wandelt gemischte Datumsformate ('YYYY-MM-DD' und 'DD.MM.YYYY') in das einheitliche Format 'YYYY-MM-DD' um.
    Funktioniert robust durch zwei Stufen der Erkennung.

    Parameters:
    - df (pd.DataFrame): DataFrame mit einer Datumsspalte
    - datums_spalte (str): Name der Spalte mit den Datumswerten

    Returns:
    - pd.DataFrame: DataFrame mit korrekt konvertierten Datumswerten als datetime64
    """

    # Erster Versuch: ISO-Format
    df[datums_spalte] = pd.to_datetime(df[datums_spalte], errors='coerce', dayfirst=False)

    # Zweiter Versuch: deutsches Format nur für Zeilen, die noch NaT sind
    mask_nat = df[datums_spalte].isna()
    if mask_nat.any():
        df.loc[mask_nat, datums_spalte] = pd.to_datetime(
            df.loc[mask_nat, datums_spalte],
            errors='coerce',
            dayfirst=True
        )

    # Optional: Warnung ausgeben, falls immer noch NaT vorhanden sind
    if df[datums_spalte].isna().any():
        print("Warnung: Einige Datumswerte konnten nicht konvertiert werden.")

    # Jetzt sind alle gültigen Werte im datetime-Format
    return df
