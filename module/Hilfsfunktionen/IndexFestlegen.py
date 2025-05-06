import pandas as pd

def IndexFestlegen(df):
    """
    Setzt die erste Spalte des DataFrames als Index.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, bei dem die erste Spalte als Index gesetzt werden soll.

    *Returns:*
    - pandas.DataFrame
        Der DataFrame mit der ersten Spalte als Index.
    """
    
    # Hole den Namen der ersten Spalte
    erste_spalte = df.columns[0]
    
    # Setze die erste Spalte als Index
    df.set_index(erste_spalte, inplace=True)
    
    print(f"Die erste Spalte '{erste_spalte}' wurde erfolgreich als Index gesetzt.")
    
    return df
