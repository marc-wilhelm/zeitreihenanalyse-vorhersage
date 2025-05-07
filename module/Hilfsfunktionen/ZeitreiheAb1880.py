import pandas as pd

def ZeitreiheAb1880(df):
    """
    Filtert die Zeitreihe, sodass nur Daten ab 1880 enthalten sind.

    Diese Funktion entfernt alle Zeilen, bei denen das Jahr in der 'Datum'-Spalte vor 1880 liegt, sodass nur Daten ab 1850 im 
    DataFrame verbleiben.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, der auf das Jahr 1880 gefiltert werden soll.

    *Returns:*
    - pandas.DataFrame
        Der gefilterte DataFrame mit nur den Daten ab 1880.
    """
    # Stelle sicher, dass die 'Datum'-Spalte im Datetime-Format vorliegt
    df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')  # Konvertiere zu Datetime, falls nötig
    
    # Filtere die Daten nach dem Jahr (nur Daten ab 1880)
    df_filtered = df[df['Datum'].dt.year >= 1880]
    
    return df_filtered
