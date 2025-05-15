# Importiere die entsprechenden Funktionen aus jedem Modul
from Hilfsfunktionen.CusumTest import cusum_test  # Stelle sicher, dass du die neue Version nutzt
from Hilfsfunktionen.AdfTest import AdfTest
from Hilfsfunktionen.KruskalWallisTest import KruskalWallisTest
import sys
import os

# Übergeordnetes Verzeichnis hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Jetzt sollte config importiert werden können
import config

def main():
    
    timeseries = config.df_seasonal_diff
    
    
    # 3. Kruskal-Wallis-Test durchführen (Prüfung auf saisonale Unterschiede)
    print("Spalten im DataFrame:", timeseries.columns.tolist())

    KruskalWallisTest(timeseries)

    # 4. ADF-Test durchführen
    AdfTest(timeseries)

    # 5. CUSUM-Test durchführen
    cusum_test(timeseries, target_column='MonatlicheDurchschnittsTemperatur', date_column='Datum')

if __name__ == "__main__":
    main()
