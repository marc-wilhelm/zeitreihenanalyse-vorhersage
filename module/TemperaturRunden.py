import pandas as pd

import pandas as pd

def TemperaturRunden(df, Dezimalstellen=2):
    """
    Rundet die Werte in der Spalte 'MonatlicheDurchschnittsTemperatur' auf eine angegebene Anzahl von Dezimalstellen.

    Diese Funktion stellt sicher, dass die Werte in der Spalte 'MonatlicheDurchschnittsTemperatur' numerisch sind 
    und rundet sie dann auf die angegebene Anzahl von Dezimalstellen. Falls Werte in der Spalte nicht numerisch sind,
    werden sie in NaN umgewandelt.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, dessen Temperaturwerte gerundet werden sollen.
    - Dezimalstellen: int
        Die Anzahl der Dezimalstellen, auf die gerundet werden soll. Standardmäßig 2.

    *Returns:*
    - pandas.DataFrame
        Der DataFrame mit den gerundeten Temperaturwerten in der Spalte 'MonatlicheDurchschnittsTemperatur'.
    """
    
    # Ersetze Kommas durch Punkte für die Dezimalstellen und konvertiere die Spalte zu float
    df['MonatlicheDurchschnittsTemperatur'] = df['MonatlicheDurchschnittsTemperatur'].astype(str).str.replace(',', '.', regex=False)
    
    # Konvertiere die Spalte 'MonatlicheDurchschnittsTemperatur' in numerische Werte (ungültige Werte werden zu NaN)
    df['MonatlicheDurchschnittsTemperatur'] = pd.to_numeric(df['MonatlicheDurchschnittsTemperatur'], errors='coerce')
    
    # Jetzt die Werte runden, NaN-Werte bleiben unverändert
    df['MonatlicheDurchschnittsTemperatur'] = df['MonatlicheDurchschnittsTemperatur'].round(Dezimalstellen)
    
    return df
