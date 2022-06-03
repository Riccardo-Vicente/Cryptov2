import pandas as pd
import numpy as np
import Capital_Outlay

solar_irradiance_file = "Data/Hourly_solar_irradiance_Bloemfontein.csv"
df = pd.read_csv(solar_irradiance_file)
#df = pd.read_csv(solar_irradiance_file, index_col='datetime',
               #  parse_dates={'datetime': [1,2,3,4]},
                # date_parser=lambda x: pd.datetime.strptime(x, '%Y %m %d %H'))
print(df.head())

#specs for a 250W Monocrystalline solar panel
panel_power = 250 #Watts
panel_area = 1.6236 #m^2

#constants to calculate energy produced
area = (Capital_Outlay.RE_capacity*(1000000)/panel_power)*panel_area
print("Solar panel area: {} m^2".format(area))
r = Capital_Outlay.eff
PR = 0.75

#Nested for loop to calculate energy production per hour
#year_start = int(input("Enter start date "))
#year_end = int(input("Enter end date "))

h = df['Hour']
d = df['Day']
m = df['Month']
y = df['Year']
print(y)
#solar_irradiance = float(df['Solar Irradiance (Wh/m^2)'])

while y <= 2022:
    solar_energy = area*r*solar_irradiance*PR
    print("Solar energy: {} Wh".format(solar_energy))


