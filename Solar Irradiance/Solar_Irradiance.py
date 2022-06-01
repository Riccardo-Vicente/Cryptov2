import pandas as pd
import numpy as np
import Capital_Outlay

solar_irradiance_file = "../Data/Hourly_solar_irradiance_Bloemfontein.csv"
df = pd.read_csv(solar_irradiance_file)
#df = pd.read_csv(solar_irradiance_file, index_col='datetime',
               #  parse_dates={'datetime': [1,2,3,4]},
                # date_parser=lambda x: pd.datetime.strptime(x, '%Y %m %d %H'))
print(df.head())

#specs for a 250W Monocrystalline solar panel
panel_power = 250 #Watts
panel_area = 1.6236 #m^2

#constants to calculate energy produced
area = (Capital_Outlay.RE_capacity*(10^6)/panel_power)*panel_area
r = Capital_Outlay.eff
PR = 0.75
print(r)