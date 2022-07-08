import pandas as pd
import numpy as np
import Capital_Outlay
from datetime import datetime
# --------------------------------------------------------------------------------------
# Solar Irradiance data and solar energy calcs
# --------------------------------------------------------------------------------------
crypto = "BTC"
solar_irradiance_file = "Data/Hourly_solar_irradiance_Bloemfontein.csv"
if crypto == "BTC":
    df = pd.read_csv(solar_irradiance_file)     # start at 2012
if crypto == "ETH":
    df = pd.read_csv(solar_irradiance_file, header=0, skiprows=range(1, 35064))     # start at 2016
print(df)

# specs for a 250W Monocrystalline solar panel
panel_power = 250  # Watts
panel_area = 1.6236  # m^2

# Constants to calculate energy produced
area = float((Capital_Outlay.RE_capacity * 1000000 / panel_power) * panel_area)
# print("Solar panel area: {} m^2".format(area))
r = float(Capital_Outlay.eff)
PR = float(0.75)
# area = 1000
# r = 0.5

# year_start = int(input("Enter start date "))
# year_end = int(input("Enter end date "))

# Calculate energy production per hour
df["Solar Energy (kWh/h)"] = (df["Solar Irradiance (Wh/m^2)"]/1000)*area*r*PR

#miner_avg = round(np.average(df["Number of miners"]), 0)
#print("Average no. miners to purchase: {} \n".format(miner_avg))

# ----------------------------------------------------------------------------------------
# Return from IPP sales
# ----------------------------------------------------------------------------------------
# Read electricity tariff history
tariff_file = "Data/Electricity_Tariffs.csv"
et = pd.read_csv(tariff_file)

OFFPEAK = 0
STANDARD = 1
PEAK = 2
TARIFF = ["OffPeak", "Standard", "Peak"]

# Declare TOU tariffs
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

    # Assign miners to select
    if row["Year"] < 2016:
        miner_choice = Capital_Outlay.m1
    elif row["Year"] < 2020:
        miner_choice = Capital_Outlay.m2
    else:
        miner_choice = Capital_Outlay.m3

    # Number of miners that can be powered each hour
    df["Number of miners"] = round((df["Solar Energy (kWh/h)"] * 0.6 * 1000) / Capital_Outlay.power[miner_choice])

    # Assign electricity tariff seasons
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

    # Access the exact TOU tariff for each hour
    tariff_yr = et.loc[et["Year"] == row["Year"]]
    tariff_ind = tariff[season][TARIFF[TOU]]
    tariff_price = tariff_yr[tariff_ind]
    # Add tariffs to df
    df.loc[ind, "Tariffs"] = tariff_price.values[0]/100

df["Hourly_IPP_Revenue_Rand"] = round((df["Solar Energy (kWh/h)"] * df["Tariffs"]), 2)

print("Miners to purchase:")
if crypto == "BTC":
    miner_1_avg = df["Number of miners"][:35064].loc[df["Number of miners"] != 0].mean()
    miner_1_avg = round(miner_1_avg, 0)
    miner_2_avg = df["Number of miners"][35065:70128].loc[df["Number of miners"] != 0].mean()
    miner_2_avg = round(miner_2_avg, 0)
    miner_3_avg = df["Number of miners"][70128:87672].loc[df["Number of miners"] != 0].mean()
    miner_3_avg = round(miner_2_avg, 0)
    print("Miner 1 average: {}".format(miner_1_avg, 0))
    print("Miner 2 average: {}".format(miner_2_avg, 0))
    print("Miner 3 average: {}".format(miner_3_avg, 0))

if crypto == "ETH":
    miner_2_avg = df["Number of miners"][:35063].loc[df["Number of miners"] != 0].mean()
    miner_2_avg = round(miner_2_avg, 0)
    miner_3_avg = df["Number of miners"][35064:].loc[df["Number of miners"] != 0].mean()
    miner_3_avg = round(miner_3_avg, 0)
    print("Miner 2 average: {}".format(miner_2_avg, 0))
    print("Miner 3 average: {}".format(miner_3_avg, 0))

print(df)
