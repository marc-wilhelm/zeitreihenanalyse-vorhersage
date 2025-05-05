import pandas as pd

def DatumFormatieren(df):
    """
    Wandelt die Werte in der Spalte 'Datum' in das Format YYYY-MM-DD um.

    Diese Funktion stellt sicher, dass alle Werte in der Spalte 'Datum' in das Format YYYY-MM-DD konvertiert werden,
    unabhängig davon, ob sie im Format DD.MM.YYYY oder YYYY-MM-DD vorliegen.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, dessen Datumswerte formatiert werden sollen.

    *Returns:*
    - pandas.DataFrame
        Der DataFrame mit den konvertierten Datumswerten im Format YYYY-MM-DD.
    """
    
    # Umwandlung der 'Datum' Spalte in das einheitliche Format YYYY-MM-DD
    df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce', dayfirst=True)  # dayfirst=True für DD.MM.YYYY
    df['Datum'] = df['Datum'].dt.strftime('%Y-%m-%d')  # Format auf YYYY-MM-DD setzen
    
    return df
