def NaNPruefen(df):
    """
    Gibt die Anzahl der NaN-Werte pro Spalte aus (prozentual) und die Zeilen mit NaN-Werten.

    Diese Funktion prüft, wie viele NaN-Werte (fehlende Werte) in jeder Spalte des DataFrames vorhanden sind. Zudem gibt sie 
    alle Zeilen aus, die mindestens einen NaN-Wert enthalten. Wenn NaN-Werte zu Beginn oder am Ende der Zeitreihe auftreten, 
    werden diese Zeilen entfernt.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, der auf NaN-Werte geprüft werden soll.

    *Returns:*
    - pandas.DataFrame
        Der bereinigte DataFrame ohne NaN-Werte zu Beginn oder Ende.
    """
    # Prozentualer Anteil an NaN-Werten pro Spalte
    nan_percentage = df.isna().mean() * 100  
    print(f"Prozentualer Anteil an NaN-Werten pro Spalte:\n{nan_percentage}\n")
    
    # Zeilen mit NaN-Werten
    nan_rows = df[df.isna().any(axis=1)]  
    print(f"Zeilen mit NaN-Werten:\n{nan_rows}\n")

    # Prüfen, ob NaN-Werte zu Beginn oder Ende der Zeitreihe vorliegen
    if df.isna().iloc[0].any() or df.isna().iloc[-1].any():
        # Lösche die Zeilen, die NaN am Anfang oder Ende enthalten
        df_cleaned = df.dropna(subset=['MonatlicheDurchschnittsTemperatur'])
        print("NaN-Werte am Anfang oder Ende der Zeitreihe gefunden und entfernt.")
    else:
        df_cleaned = df
        print("Keine NaN-Werte zu Beginn oder Ende der Zeitreihe gefunden.")

    # Rückgabe des bereinigten DataFrames
    return df_cleaned
