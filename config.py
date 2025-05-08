import pandas as pd

PATH_TS_BERLIN = "./daten/original-daten/zeitreihe_berlin.csv"
PATH_TS_BERLIN_CLEAN = "./daten/bereinigte-daten/bereinigt_zeitreihe_berlin.csv"

PATH_TS_ANGELES = "./daten/original-daten/zeitreihe_angeles.csv"
PATH_TS_ANGELES_CLEAN = "./daten/bereinigte-daten/bereinigt_zeitreihe_angeles.csv"

PATH_TS_ABAKAN = "./daten/original-daten/zeitreihe_abakan.csv"
PATH_TS_ABAKAN_CLEAN = "./daten/bereinigte-daten/bereinigt_zeitreihe_abakan.csv"

df_berlin = pd.read_csv(PATH_TS_BERLIN_CLEAN)
temp_diff_berlin = df_berlin['MonatlicheDurchschnittsTemperatur'].diff(1).dropna()

df_angeles = pd.read_csv(PATH_TS_ANGELES_CLEAN)
temp_diff_angeles = df_angeles['MonatlicheDurchschnittsTemperatur'].diff(1).dropna()

df_abakan = pd.read_csv(PATH_TS_ABAKAN_CLEAN)
temp_diff_abakan = df_abakan['MonatlicheDurchschnittsTemperatur'].diff(1).dropna()