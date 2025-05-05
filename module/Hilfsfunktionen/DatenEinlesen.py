import pandas as pd

def DatenEinlesen(Dateipfad, sep=';'):
    """
    Liest eine CSV-Datei ein und gibt das DataFrame zurück.

    Diese Funktion liest eine CSV-Datei von dem angegebenen Pfad ein und gibt den Inhalt als Pandas DataFrame zurück. 
    Sie fängt eventuelle Fehler beim Einlesen der Datei ab und gibt im Falle eines Fehlers `None` zurück.

    *Parameters:*
    - Dateipfad: str
        Der Pfad zur CSV-Datei, die eingelesen werden soll.
    - sep: str
        Das Trennzeichen, das in der CSV-Datei verwendet wird. Standardmäßig ist es ';'.

    *Returns:*
    - pandas.DataFrame or None
        Ein DataFrame, das die eingelesenen Daten enthält, oder `None`, falls ein Fehler auftritt.
    """
    try:
        df = pd.read_csv(Dateipfad, sep=sep)  # Hier sep übergeben
        return df
    except Exception as e:
        print(f"Fehler beim Einlesen der Daten: {e}")
        return None

