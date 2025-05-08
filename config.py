PATH_TS_BERLIN = "./daten/original-daten/zeitreihe_berlin.csv"
PATH_TS_BERLIN_CLEAN = "./daten/bereinigte-daten/zeitreihe_berlin_bereinigt.csv"

PATH_TS_ANGELES = "./daten/original-daten/zeitreihe_angeles.csv"
PATH_TS_ANGELES_CLEAN = "./daten/bereinigte-daten/zeitreihe_angeles_bereinigt.csv"

import pandas as pd

df_angeles = pd.read_csv(PATH_TS_ANGELES_CLEAN)
temp_diff_angeles = df_angeles['MonatlicheDurchschnittsTemperatur'].diff(1).dropna()



PATH_TS_ABAKAN = "./daten/original-daten/zeitreihe_abakan.csv"
PATH_TS_ABAKAN_CLEAN = "./daten/bereinigte-daten/bereinigt_zeitreihe_abakan.csv"