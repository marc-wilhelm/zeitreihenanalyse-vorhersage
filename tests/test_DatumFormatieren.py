import pandas as pd
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from module.Hilfsfunktionen.DatumFormatieren import DatumFormatieren


def test_DatumFormatieren_mixed_formats():
    # Beispielhafte Eingabedaten mit gemischten Formaten
    test_data = pd.DataFrame({
        'Datum': [
            '2024-12-01',  # korrektes US-Format
            '01.12.2024',  # deutsches Format
            '31.01.2023',  # deutsches Format
            '2023-01-31',  # korrektes US-Format
            '13.04.2022',  # deutsches Format
            'invalid',     # ungültiges Datum
        ]
    })

    # Erwartete Ausgaben im einheitlichen Format
    expected_dates = [
        '2024-12-01',
        '2024-12-01',
        '2023-01-31',
        '2023-01-31',
        '2022-04-13',
        None  # invalid -> NaT -> strftime wird zu NaN
    ]

    result_df = DatumFormatieren(test_data.copy())

    # Prüfe, ob das Ergebnis korrekt ist
    for result, expected in zip(result_df['Datum'], expected_dates):
        if expected is None:
            assert pd.isna(result)
        else:
            assert result == expected
