import pandas as pd

PATH_TS_BERLIN = "./daten/original-daten/zeitreihe_berlin.csv"
PATH_TS_BERLIN_CLEAN = "./daten/bereinigte-daten/bereinigt_zeitreihe_berlin.csv"

PATH_TS_ANGELES = "./daten/original-daten/zeitreihe_angeles.csv"
PATH_TS_ANGELES_CLEAN = "./daten/bereinigte-daten/bereinigt_zeitreihe_angeles.csv"

PATH_TS_ABAKAN = "./daten/original-daten/zeitreihe_abakan.csv"
PATH_TS_ABAKAN_CLEAN = "./daten/bereinigte-daten/bereinigt_zeitreihe_abakan.csv"



df_berlin = pd.read_csv(PATH_TS_BERLIN_CLEAN)
#seasonal_diff_berlin = df_berlin['MonatlicheDurchschnittsTemperatur'].diff(12).dropna()
temp_diff_berlin = df_berlin['MonatlicheDurchschnittsTemperatur'].diff(1)
seasonal_diff_berlin = temp_diff_berlin.diff(12).dropna()


df_angeles = pd.read_csv(PATH_TS_ANGELES_CLEAN)
temp_diff_angeles = df_angeles['MonatlicheDurchschnittsTemperatur'].diff(1)
seasonal_diff_angeles = temp_diff_angeles.diff(12).dropna()





df_seasonal_diff_berlin = df_berlin.copy()
df_seasonal_diff_berlin['MonatlicheDurchschnittsTemperatur'] = seasonal_diff_berlin

df_seasonal_diff_berlin = df_seasonal_diff_berlin[['Datum', 'MonatlicheDurchschnittsTemperatur']].dropna()





df_abakan = pd.read_csv(PATH_TS_ABAKAN_CLEAN)
seasonal_diff_abakan = df_abakan['MonatlicheDurchschnittsTemperatur'].diff(12).dropna() #für ARIMA/SARIMA nehmen

df_seasonal_diff_abakan = df_abakan.copy()
df_seasonal_diff_abakan['MonatlicheDurchschnittsTemperatur'] = seasonal_diff_abakan

df_seasonal_diff_abakan = df_seasonal_diff_abakan[['Datum', 'MonatlicheDurchschnittsTemperatur']].dropna() #für Stationaritätstest nehmen

temp_diff_abakan = df_abakan['MonatlicheDurchschnittsTemperatur'].diff(1)


#df_berlin["Datum"] = pd.to_datetime(df_berlin["Datum"])
#df_berlin.set_index("Datum", inplace=True)
#df_berlin = df_berlin.asfreq('MS')  # Setzt die Frequenz auf Monatsanfang (Monatlich)
#temp_berlin = df_berlin["MonatlicheDurchschnittsTemperatur"]

#temp_diff_berlin = df_berlin['MonatlicheDurchschnittsTemperatur'].diff(1).dropna()




df_angeles = pd.read_csv(PATH_TS_ANGELES_CLEAN)

temp_diff_angeles = df_angeles['MonatlicheDurchschnittsTemperatur'].diff(1)
seasonal_diff_angeles = temp_diff_angeles.diff(12).dropna()
#print(seasonal_diff_angeles)


df_seasonal_diff = df_angeles.copy()
df_seasonal_diff['MonatlicheDurchschnittsTemperatur'] = seasonal_diff_angeles

df_seasonal_diff = df_seasonal_diff[['Datum', 'MonatlicheDurchschnittsTemperatur']].dropna()
print(df_seasonal_diff)











#df_abakan = pd.read_csv(PATH_TS_ABAKAN_CLEAN)
#df_abakan["Datum"] = pd.to_datetime(df_abakan["Datum"])
#df_abakan.set_index("Datum", inplace=True)
#df_abakan = df_abakan.asfreq('MS')  # Setzt die Frequenz auf Monatsanfang (Monatlich)
#temp_abakan = df_abakan["MonatlicheDurchschnittsTemperatur"]



#temp_diff_abakan = df_abakan['MonatlicheDurchschnittsTemperatur'].diff(1).dropna()