import pandas as pd
import numpy as np
import Capital_Outlay
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
print("Solar panel area: {} m^2".format(area))
r = float(Capital_Outlay.eff)
PR = float(0.75)

#For loop to calculate energy production per hour
#year_start = int(input("Enter start date "))
#year_end = int(input("Enter end date "))

for ind, row in df.iterrows():
    df.loc[ind, "Solar Energy (kWh/h)"] = (row["Solar Irradiance (Wh/m^2)"]/1000)*area*r*PR

print(df)
#----------------------------------------------------------------------------------------
#Number of miners that can operate
#----------------------------------------------------------------------------------------

for ind, row in df.iterrows():
    df.loc[ind, "Number of miners"] = (row["Solar Energy (kWh/h)"]*1000)/Capital_Outlay.power[Capital_Outlay.m1]
print("Number of miners that can run @ each hour:")
print(round(df["Number of miners"],0))

#----------------------------------------------------------------------------------------
#Return from IPP sales
#----------------------------------------------------------------------------------------

#Read electricity tariff history
tariff_file = "Data/Electricity_Tarrifs.csv"
et = pd.read_csv(tariff_file)
print(et)

#Declare TOU tariffs
Weekday_Tariff= {
    0: 'OffPeak',
    1: 'OffPeak',
    2: 'OffPeak',
    3: 'OffPeak',
    4: 'OffPeak',
    5: 'OffPeak',
    6: 'Standard',
    7: 'Peak',
    8: 'Peak',
    9: 'Peak',
    10: 'Standard',
    11: 'Standard',
    12: 'Standard',
    13: 'Standard',
    14: 'Standard',
    15: 'Standard',
    16: 'Standard',
    17: 'Standard',
    18: 'Peak',
    19: 'Peak',
    20: 'Standard',
    21: 'Standard',
    22: 'Off-Peak',
    23: 'Off-Peak',
}

Sat_Tariff = {
    0: 'OffPeak',
    1: 'OffPeak',
    2: 'OffPeak',
    3: 'OffPeak',
    4: 'OffPeak',
    5: 'OffPeak',
    6: 'OffPeak',
    7: 'Standard',
    8: 'Standard',
    9: 'Standard',
    10: 'Standard',
    11: 'Standard',
    12: 'OffPeak',
    13: 'OffPeak',
    14: 'OffPeak',
    15: 'OffPeak',
    16: 'OffPeak',
    17: 'OffPeak',
    18: 'Standard',
    19: 'Standard',
    20: 'Off-Peak',
    21: 'Off-Peak',
    22: 'Off-Peak',
    23: 'Off-Peak',
}
#for ind, row in df.iterrows():

   # season = "LD"
   # if 5 <= row["Month"] <= 7:
   #     season = "HD"

   # if row["Day"] = weekday
   #     IPP_rev = Weekday_Tariff[row["Hour"]]*row["Solar Energy (kWh/h)"]/100

  #  if row["Day"] = Saturday
  #      IPP_rev = Sat_Tariff[row["Hour"]] * row["Solar Energy (kWh/h)"] / 100

   # df.loc[ind, "Hourly Revenue (R)"] = IPP_rev

#print(round(df,2))