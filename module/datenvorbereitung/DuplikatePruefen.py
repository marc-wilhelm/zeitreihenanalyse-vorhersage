import pandas as pd

def DuplikatePruefen(df):
    """
    Überprüft und entfernt Duplikate im DataFrame.

    Diese Funktion prüft, ob es Duplikate im DataFrame gibt, und entfernt diese. 
    Duplikate werden basierend auf allen Spalten des DataFrames erkannt.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, der auf Duplikate geprüft werden soll.

    *Returns:*
    - pandas.DataFrame
        Der DataFrame ohne Duplikate.
    """
    
    # Duplikate basierend auf allen Spalten entfernen
    df_cleaned = df.drop_duplicates()

    # Gib die Anzahl der entfernten Duplikate aus
    duplikate_anzahl = len(df) - len(df_cleaned)
    if duplikate_anzahl > 0:
        print(f"Es wurden {duplikate_anzahl} Duplikate entfernt.")
    else:
        print("Es wurden keine Duplikate gefunden.")

    return df_cleaned
