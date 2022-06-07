import pandas as pd
import numpy as np
import Capital_Outlay

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

#Number of miners that can operate

    #Capacity of solar system each hour
for ind, row in df.iterrows():
    df.loc[ind, "Number of miners"] = (row["Solar Energy (kWh/h)"]*1000)/Capital_Outlay.power[Capital_Outlay.m1]
print("Number of miners that can run @ each hour:")
print(round(df["Number of miners"],0))


