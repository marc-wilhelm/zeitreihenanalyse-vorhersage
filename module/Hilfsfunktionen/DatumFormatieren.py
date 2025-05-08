import pandas as pd



def DatumFormatieren(df, datums_spalte='Datum'):
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
    df['Datum'] = df['Datum'].dt.strftime('%Y-%m-%d')
    return df

