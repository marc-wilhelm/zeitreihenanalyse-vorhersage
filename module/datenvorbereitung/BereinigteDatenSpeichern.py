def BereinigteDatenSpeichern(df, Dateipfad):
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
