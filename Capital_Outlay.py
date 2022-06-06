import pandas as pd
import numpy as np
#-------------------------------------------------------------------------------------------------------
#Renewable energy infrustructure
#------------------------------------------------------------------------------------------------------

# Defining Renewable energy costs ($/MWh)
LCOE = {
    'pv_energy_residential': 189,
    'pv_energy_largescale': 37,
    'wind_energy': 40,
}
renewable_type = 'pv_energy_largescale'

USD_Rand = 15

#Ask user renewable energy specs
RE_capacity = float(input("Enter RE capacity ")) # MW
print("Capacity: {} MW".format(RE_capacity))

#Determine cost of RE over lifetime
eff = 0.1724 # %
E_annual = RE_capacity*4380*eff
E_annual = float(E_annual)
print("Annual Energy generation: {} MWh.".format(E_annual))
Lifetime = 25 # years

E_lifetime = E_annual*Lifetime
print("Lifetime Energy generation: {} MWh".format(E_lifetime))

RE_cost = E_lifetime*LCOE[renewable_type]*USD_Rand
print("Capital Cost of RE infrustructure: R {:.2f}".format(RE_cost))

#------------------------------------------------------------------------------------------
#Crypto mining infrustructre
#------------------------------------------------------------------------------------------

# Get mining equipment data
df = pd.read_excel('./Data/crypto_mining_equipment.xlsx')

#Set hardware as index
df.set_index(df["Hardware"].values)
print(df)

#Declare miners to purchase
miner1 = 'Canaan (Avalon 6)'
miner2 = 'GeForce RTX 3060 Ti'
print("Miner 1: {}".format(miner1))
print("Miner 2: {}".format(miner2))

#Get miner specs
for ind, row in df:
    power1 = row["Power Consumption (W)"]
print(power1)



