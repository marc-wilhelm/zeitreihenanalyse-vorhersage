import pandas as pd
from scipy.stats import kruskal

def KruskalWallisTest(data):
    """
    Führt einen Kruskal-Wallis-Test durch, um saisonale Unterschiede zwischen Monaten zu prüfen.
    
    Parameters:
    data (pd.DataFrame): DataFrame mit den Spalten 'Datum' und 'MonatlicheDurchschnittsTemperatur'.
    
    Returns:
    None: Gibt das p-Value des Tests aus.
    """
    data['Datum'] = pd.to_datetime(data['Datum'])
    data['Monat'] = data['Datum'].dt.month  # Monat extrahieren
    
    # Temperaturdaten nach Monaten gruppieren
    monatliche_daten = [group['MonatlicheDurchschnittsTemperatur'].values 
                        for _, group in data.groupby('Monat')]
    
    # Kruskal-Wallis-Test
    stat, p = kruskal(*monatliche_daten)
    
    print(f"Kruskal-Wallis-Teststatistik: {stat:.4f}")
    print(f"p-Wert: {p:.4f}")
    if p < 0.05:
        print("⇒ Signifikante saisonale Unterschiede vorhanden.")
    else:
        print("⇒ Keine signifikanten saisonalen Unterschiede nachgewiesen.")
