import pandas as pd


def daten_einlesen(Dateipfad, sep=';', decimal=','):
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
        df = pd.read_csv(Dateipfad, sep=sep, decimal=decimal)
        return df
    except Exception as e:
        print(f"Fehler beim Einlesen der Daten: {e}")
        return None


def spaltennamen_korrigieren(df):
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


def datum_formatieren(df):
    """
    Konvertiert gemischte Datumsformate in einheitliches YYYY-MM-DD-Format.
    """
    def parse_datum(datum):
        try:
            if isinstance(datum, str):
                if "." in datum:
                    return pd.to_datetime(datum, dayfirst=True, errors='coerce')
                else:
                    return pd.to_datetime(datum, dayfirst=False, errors='coerce')
            return pd.NaT
        except Exception:
            return pd.NaT

    df['Datum'] = df['Datum'].apply(parse_datum)
    #df['Datum'] = df['Datum'].dt.strftime('%Y-%m-%d')
    return df


def temperatur_und_datum_extrahieren(df):
    """
    Erstellt einen DataFrame mit nur den Spalten 'Datum' und 'MonatlicheDurchschnittsTemperatur'.

    Diese Funktion extrahiert nur die relevanten Spalten 'Datum' und 'MonatlicheDurchschnittsTemperatur' aus dem DataFrame
    und gibt einen neuen DataFrame zurück, der nur diese beiden Spalten enthält.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, aus dem die relevanten Spalten ausgewählt werden.

    *Returns:*
    - pandas.DataFrame
        Ein DataFrame, das nur die Spalten 'Datum' und 'MonatlicheDurchschnittsTemperatur' enthält.
    """
    df_selected = df[['Datum', 'MonatlicheDurchschnittsTemperatur']]  # Nur die relevanten Spalten auswählen
    return df_selected


def zeitreihe_ab_1880(df):
    """
    Entfernt nur Zeilen, deren Datum im Format YYYY-MM-DD erkannt wird und vor dem Jahr 1880 liegt.

    Alle anderen Zeilen (z. B. mit DD.MM.YYYY oder ungültigem Datum) bleiben erhalten.

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


def nan_pruefen(df):
    """
    Gibt die Anzahl der NaN-Werte pro Spalte aus (prozentual) und die Zeilen mit NaN-Werten.

    Diese Funktion prüft, wie viele NaN-Werte (fehlende Werte) in jeder Spalte des DataFrames vorhanden sind. Zudem gibt sie
    alle Zeilen aus, die mindestens einen NaN-Wert enthalten. Wenn NaN-Werte zu Beginn oder am Ende der Zeitreihe auftreten,
    werden diese Zeilen entfernt.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, der auf NaN-Werte geprüft werden soll.

    *Returns:*
    - pandas.DataFrame
        Der bereinigte DataFrame ohne NaN-Werte zu Beginn oder Ende.
    """
    # Prozentualer Anteil an NaN-Werten pro Spalte
    nan_percentage = df.isna().mean() * 100
    print(f"Prozentualer Anteil an NaN-Werten pro Spalte:\n{nan_percentage}\n")

    # Zeilen mit NaN-Werten
    nan_rows = df[df.isna().any(axis=1)]
    print(f"Zeilen mit NaN-Werten:\n{nan_rows}\n")

    # Prüfen, ob NaN-Werte zu Beginn oder Ende der Zeitreihe vorliegen
    if df.isna().iloc[0].any() or df.isna().iloc[-1].any():
        # Lösche die Zeilen, die NaN am Anfang oder Ende enthalten
        df_cleaned = df.dropna(subset=['MonatlicheDurchschnittsTemperatur'])
        print("NaN-Werte am Anfang oder Ende der Zeitreihe gefunden und entfernt.")
    else:
        df_cleaned = df
        print("Keine NaN-Werte zu Beginn oder Ende der Zeitreihe gefunden.")

    # Rückgabe des bereinigten DataFrames
    return df_cleaned


def datentypen_pruefen(df):
    """
    Prüft die Datentypen der Spalten.

    Diese Funktion gibt die Datentypen der Spalten im DataFrame aus und stellt sicher, dass die Spalte 'Datum' vom Typ `datetime`
    und die Spalte 'MonatlicheDurchschnittsTemperatur' vom Typ `float64` ist. Falls nötig, werden Konvertierungen durchgeführt.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, dessen Datentypen überprüft werden sollen.

    *Returns:*
    - pandas.DataFrame
        Der möglicherweise angepasste DataFrame mit korrekten Datentypen.
    """
    print(f"Datentypen der Spalten (vorher):\n{df.dtypes}\n")

    # Datum prüfen und ggf. konvertieren
    if df['Datum'].dtype != 'datetime64[ns]':
        print(" 'Datum' ist nicht vom Typ datetime. Versuche Umwandlung...")
        df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')
        if df['Datum'].isnull().any():
            print(" Fehler: Einige Werte in 'Datum' konnten nicht umgewandelt werden.")
        else:
            print(" 'Datum' erfolgreich in datetime umgewandelt.")

    # Temperatur prüfen und ggf. konvertieren
    if df['MonatlicheDurchschnittsTemperatur'].dtype != 'float64':
        print(" 'MonatlicheDurchschnittsTemperatur' ist nicht vom Typ float. Versuche Umwandlung...")
        df['MonatlicheDurchschnittsTemperatur'] = pd.to_numeric(df['MonatlicheDurchschnittsTemperatur'], errors='coerce')
        if df['MonatlicheDurchschnittsTemperatur'].isnull().any():
            print(" Fehler: Einige Werte in 'MonatlicheDurchschnittsTemperatur' konnten nicht umgewandelt werden.")
        else:
            print(" 'MonatlicheDurchschnittsTemperatur' erfolgreich in float64 umgewandelt.")

    print(f"\nDatentypen der Spalten (nachher):\n{df.dtypes}")
    return df


def duplikate_pruefen(df):
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


def bereinigte_daten_speichern(df, Dateipfad):
    """
    Speichert den DataFrame in eine neue CSV-Datei.

    Diese Funktion speichert den DataFrame im angegebenen Dateipfad als CSV-Datei ab.

    *Parameters:*
    - df: pandas.DataFrame
        Der DataFrame, der gespeichert werden soll.
    - Dateipfad: str
        Der Pfad, unter dem die CSV-Datei gespeichert werden soll.

    *Returns:*
    - None
        Diese Funktion gibt keine Werte zurück, sondern speichert die Datei.
    """
    df.to_csv(Dateipfad, index=False)  # Speichern der Daten als CSV
    print(f"Die Daten wurden erfolgreich in '{Dateipfad}' gespeichert.")