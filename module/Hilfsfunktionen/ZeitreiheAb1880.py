import pandas as pd

def ZeitreiheAb1880(df):
    """
    Entfernt nur Zeilen, deren Datum im Format YYYY-MM-DD erkannt wird und vor dem Jahr 1880 liegt.

    Alle anderen Zeilen (z. B. mit DD.MM.YYYY oder ungültigem Datum) bleiben erhalten.

    Parameters:
    - df: pandas.DataFrame

    Returns:
    - pandas.DataFrame
    """
    # Kopie der ursprünglichen Daten
    df = df.copy()

    # Versuche das Datum zu konvertieren (nur für Filterung verwenden)
    datum_konvertiert = pd.to_datetime(df['Datum'], errors='coerce')

    # Maske: Nur Zeilen, bei denen das konvertierte Datum entweder NaT ist oder Jahr >= 1880
    maske = datum_konvertiert.isna() | (datum_konvertiert.dt.year >= 1880)

    # Nur die Zeilen behalten, die die Maske erfüllen
    return df[maske].reset_index(drop=True)
