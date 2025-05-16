import pandas as pd

def SpaltennamenKorrigieren(df):
    """
    Korrigiert die Spaltennamen des DataFrames.

    Diese Funktion benennt die Spaltennamen des DataFrames um, um sie konsistenter und lesbarer zu machen. 
    Es werden die Namen 'dt' und 'AverageTemperature' in 'Datum' und 'MonatlicheDurchschnittsTemperatur' geändert.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, dessen Spaltennamen korrigiert werden sollen.

    *Returns:*
    - pandas.DataFrame
        Der DataFrame mit den aktualisierten Spaltennamen.
    """
    # Überprüfe die Spaltennamen vor der Umbenennung
    print("Spaltennamen vor der Umbenennung:")
    print(df.columns)

    # Umbenennung der Spalten
    df = df.rename(columns={
        'dt': 'Datum',  # 'dt' in 'Datum' umbenennen
        'AverageTemperature': 'MonatlicheDurchschnittsTemperatur',  # 'AverageTemperature' in 'MonatlicheDurchschnittsTemperatur' umbenennen
    })
    
    # Überprüfe die Spaltennamen nach der Umbenennung
    print("Spaltennamen nach der Umbenennung:")
    print(df.columns)

    return df
