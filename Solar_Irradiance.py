import pandas as pd
import numpy as np
import Capital_Outlay

solar_irradiance_file = "Data/Hourly_solar_irradiance_Bloemfontein.csv"
df = pd.read_csv(solar_irradiance_file)
#df = pd.read_csv(solar_irradiance_file, index_col='datetime',
               #  parse_dates={'datetime': [1,2,3,4]},
                # date_parser=lambda x: pd.datetime.strptime(x, '%Y %m %d %H'))
print(df)

#specs for a 250W Monocrystalline solar panel
panel_power = 250 #Watts
panel_area = 1.6236 #m^2

#constants to calculate energy produced
area = float((Capital_Outlay.RE_capacity*(1000000)/panel_power)*panel_area)
print("Solar panel area: {} m^2".format(area))
r = float(Capital_Outlay.eff)
PR = float(0.75)

#Nested for loop to calculate energy production per hour
#year_start = int(input("Enter start date "))
#year_end = int(input("Enter end date "))

#h = df['Hour']
#d = df['Day']
#m = df['Month']
#y = df['Year']

#solar_irradiance = df['Solar Irradiance (Wh/m^2)']

for ind, row in df.iterrows():
    df.loc[ind, "Solar Energy"] = row["Solar Irradiance (Wh/m^2)"]*area*r*PR

print(df)


