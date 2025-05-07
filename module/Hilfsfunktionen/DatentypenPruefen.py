def DatentypenPruefen(df):
    """
    Prüft die Datentypen der Spalten.

    Diese Funktion gibt die Datentypen der Spalten im DataFrame aus und stellt sicher, dass die Spalte 'Datum' vom Typ `datetime`
    und die Spalte 'MonatlicheDurchschnittsTemperatur' vom Typ `float64` ist.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, dessen Datentypen überprüft werden sollen.

    *Returns:*
    - None
        Diese Funktion gibt keine Werte zurück, sondern gibt stattdessen Informationen auf der Konsole aus.
    """
    print(f"Datentypen der Spalten:\n{df.dtypes}")
    
    # Prüfen, ob Datum und Temperatur die richtigen Typen haben
    if df['Datum'].dtype != 'datetime64[ns]':  # Überprüfung, ob 'Datum' der richtige Typ ist
        print("Warnung: 'Datum' ist nicht vom Typ datetime.")
    if df['MonatlicheDurchschnittsTemperatur'].dtype != 'float64':  # Überprüfung, ob Temperatur der richtige Typ ist
        print("Warnung: 'MonatlicheDurchschnittsTemperatur' ist nicht vom Typ float.")
