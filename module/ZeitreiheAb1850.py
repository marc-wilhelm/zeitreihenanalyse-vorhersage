import pandas as pd

def ZeitreiheAb1850(df):
    """
    Filtert die Zeitreihe, sodass nur Daten ab 1850 enthalten sind.

    Diese Funktion entfernt alle Zeilen, bei denen das Jahr in der 'Datum'-Spalte vor 1850 liegt, sodass nur Daten ab 1850 im 
    DataFrame verbleiben.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, der auf das Jahr 1850 gefiltert werden soll.

    *Returns:*
    - pandas.DataFrame
        Der gefilterte DataFrame mit nur den Daten ab 1850.
    """
    # Stelle sicher, dass die 'Datum'-Spalte im Datetime-Format vorliegt
    df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')  # Konvertiere zu Datetime, falls nötig
    
    # Filtere die Daten nach dem Jahr (nur Daten ab 1850)
    df_filtered = df[df['Datum'].dt.year >= 1850]
    
    return df_filtered
