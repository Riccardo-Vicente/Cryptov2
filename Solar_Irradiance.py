import pandas as pd
import numpy as np
import Capital_Outlay
from datetime import datetime
#--------------------------------------------------------------------------------------
#Solar Irradiance data and solar energy calcs
#--------------------------------------------------------------------------------------
solar_irradiance_file = "Data/Hourly_solar_irradiance_Bloemfontein.csv"
df = pd.read_csv(solar_irradiance_file)
print(df)

#specs for a 250W Monocrystalline solar panel
panel_power = 250 #Watts
panel_area = 1.6236 #m^2

#constants to calculate energy produced
area = float((Capital_Outlay.RE_capacity*(1000000)/panel_power)*panel_area)
#area = 0
print("Solar panel area: {} m^2".format(area))
r = float(Capital_Outlay.eff)
PR = float(0.75)

#For loop to calculate energy production per hour

#year_start = int(input("Enter start date "))
#year_end = int(input("Enter end date "))

#for ind, row in df.iterrows():
  #  df.loc[ind, "Solar Energy (kWh/h)"] = (row["Solar Irradiance (Wh/m^2)"]/1000)*area*r*PR
df["Solar Energy (kWh/h)"] = (df["Solar Irradiance (Wh/m^2)"]/1000)*area*r*PR

#for ind, row in df.iterrows():
    # Number of miners that can operate
  #  df.loc[ind, "Number of miners"] = (row["Solar Energy (kWh/h)"]*1000)/Capital_Outlay.power[Capital_Outlay.m1]
df["Number of miners"] = round((df["Solar Energy (kWh/h)"]*1000)/Capital_Outlay.power[Capital_Outlay.m1])
print(df)
#print("Number of miners that can run @ each hour:")
#print(round(df["Number of miners"],0))

miner_avg = round(np.average((df["Number of miners"])), 0)
print("Average no. miners to purchase: {}".format(miner_avg))

#----------------------------------------------------------------------------------------
#Return from IPP sales
#----------------------------------------------------------------------------------------

#Read electricity tariff history
tariff_file = "Data/Electricity_Tarrifs.csv"
et = pd.read_csv(tariff_file)
print(et)

OFFPEAK = 0
STANDARD = 1
PEAK = 2
TARIFF = ["OffPeak", "Standard", "Peak"]

#Declare TOU tariffs
Weekday_Tariff = {
    0: OFFPEAK, 1: OFFPEAK, 2: OFFPEAK, 3: OFFPEAK, 4: OFFPEAK, 5: OFFPEAK, 6: STANDARD, 7: PEAK,
    8: PEAK, 9: PEAK, 10: STANDARD, 11: STANDARD, 12: STANDARD, 13: STANDARD, 14: STANDARD,
    15: STANDARD, 16: STANDARD, 17: STANDARD, 18: PEAK, 19: PEAK, 20: STANDARD, 21: STANDARD,
    22: OFFPEAK, 23: OFFPEAK
}
Sat_Tariff = {
    0: OFFPEAK, 1: OFFPEAK, 2: OFFPEAK, 3: OFFPEAK, 4: OFFPEAK, 5: OFFPEAK, 6: OFFPEAK, 7: STANDARD,
    8: STANDARD, 9: STANDARD, 10: STANDARD, 11: STANDARD, 12: OFFPEAK, 13: OFFPEAK, 14: OFFPEAK,
    15: OFFPEAK, 16: OFFPEAK, 17: OFFPEAK, 18: STANDARD, 19: STANDARD, 20: OFFPEAK, 21: OFFPEAK,
    22: OFFPEAK, 23: OFFPEAK
}
Sun_Tariff = {
    0: OFFPEAK, 1: OFFPEAK, 2: OFFPEAK, 3: OFFPEAK, 4: OFFPEAK, 5: OFFPEAK, 6: OFFPEAK, 7: OFFPEAK,
    8: OFFPEAK, 9: OFFPEAK, 10: OFFPEAK, 11: OFFPEAK, 12: OFFPEAK, 13: OFFPEAK, 14: OFFPEAK,
    15: OFFPEAK, 16: OFFPEAK, 17: OFFPEAK, 18: OFFPEAK, 19: OFFPEAK, 20: OFFPEAK, 21: OFFPEAK,
    22: OFFPEAK, 23: OFFPEAK
}

tariff = {"HD": {"Peak": "HD-Peak", "Standard": "HD-Standard", "OffPeak": "HD-OffPeak"},
          "LD": {"Peak": "LD-Peak", "Standard": "LD-Standard", "OffPeak": "LD-OffPeak"}}

# Iterate through solar irradiance file
for ind, row in df.iterrows():
    # if month is June - Aug: (High demand season), else its Low demand season
    if (row["Month"] >= 5) and (row["Month"] <= 7):
        season = "HD"
    else:
        season = "LD"

    day = datetime.weekday(datetime(round(row["Year"]), round(row["Month"]), round(row["Day"])))
    # if day is weekday
    if day < 5:
        TOU = Weekday_Tariff[row["Hour"]]
    # if day is saturday
    elif day == 5:
        TOU = Sat_Tariff[row["Hour"]]
    # if day is sunday
    else:
        TOU = Sun_Tariff[row["Hour"]]

    tariff_row = et.loc[et["Year"] == row["Year"]]
    tariff_ind = tariff[season][TARIFF[TOU]]
    tariff_price = tariff_row[tariff_ind]
   # t = tariff_price[ind]
    #df.loc[ind, "Tariffs"] = t
    #df["Tariff"] = t
    print(tariff_price[0])
   # df.loc[ind, "Hourly Revenue (R)"] = row["Solar Energy (kWh/h)"] * (tariff_price[0] / 100)

# df["Hourly Revenue (R)"] = df["Solar Energy (kWh/h)"] * (tariff_row[tariff_ind] / 100)

#print(df)
#print(round(df, 2))
