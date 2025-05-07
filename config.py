import pandas as pd

datapathzeitreiheberlin = "./daten/original-daten/zeitreihe_berlin.csv"
datapathzeitreiheberlinbereinigt = "./daten/bereinigte-daten/zeitreihe_berlin_bereinigt.csv"

datapathzeitreiheangeles = "./daten/original-daten/zeitreihe_angeles.csv"
datapathzeitreiheangelesbereinigt = "./daten/bereinigte-daten/zeitreihe_angeles_bereinigt.csv"


df_angeles = pd.read_csv(datapathzeitreiheangelesbereinigt)
temp_diff_angeles = df_angeles['MonatlicheDurchschnittsTemperatur'].diff(1).dropna()

