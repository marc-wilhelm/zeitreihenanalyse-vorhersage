def TemperaturUndDatumExtrahieren(df):
    """
    Erstellt einen DataFrame mit nur den Spalten 'Datum' und 'MonatlicheDurchschnittsTemperatur'.

    Diese Funktion extrahiert nur die relevanten Spalten 'Datum' und 'MonatlicheDurchschnittsTemperatur' aus dem DataFrame 
    und gibt einen neuen DataFrame zurück, der nur diese beiden Spalten enthält.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, aus dem die relevanten Spalten ausgewählt werden.

    *Returns:*
    - pandas.DataFrame
        Ein DataFrame, das nur die Spalten 'Datum' und 'MonatlicheDurchschnittsTemperatur' enthält.
    """
    df_selected = df[['Datum', 'MonatlicheDurchschnittsTemperatur']]  # Nur die relevanten Spalten auswählen
    return df_selected
