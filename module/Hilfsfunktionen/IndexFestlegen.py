import pandas as pd

def IndexFestlegen(df, datumsspalte):
    """
    Setzt die angegebene Datumsspalte als Index des DataFrames.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, bei dem die Datumsspalte als Index gesetzt werden soll.
    - datumsspalte: str
        Der Name der Spalte, die das Datum enthält und als Index gesetzt werden soll.

    *Returns:*
    - pandas.DataFrame
        Der DataFrame mit der Datumsspalte als Index.
    """
    
    # Stelle sicher, dass die Datumsspalte im Datetime-Format vorliegt
    df[datumsspalte] = pd.to_datetime(df[datumsspalte], errors='coerce')
    
    # Setze die Datumsspalte als Index
    df.set_index(datumsspalte, inplace=True)
    
    print(f"Die Datumsspalte '{datumsspalte}' wurde erfolgreich als Index gesetzt.")
    
    return df

# Beispielaufruf
# Angenommen, df ist dein DataFrame und die Datumsspalte heißt 'Datum':
# df = SetzeDatumAlsIndex(df, 'Datum')
