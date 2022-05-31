import pandas as pd
import numpy as np

# Defining Renewable energy costs ($/MWh)
# LCOE = np.array([PV Energy (residential), 189], [PV Energy (large scale farm), 37], [Wind Energy, 40])

pv_energy_residential = 189
pv_energy_large = 37
wind_energy = 40

LCOE = {
    'pv_energy_residential': 189,
    'pv_energy_large': 37,
    'wind_energy': 40,
}

renewable_type = 'wind_energy'

#Ask user renewabe energy specs
RE_capacity = int(input("Enter RE capacity")) # MW
print("{} MW".format(RE_capacity))

eff = 0.1724 # %
E_annual = RE_capacity*4380*eff
E_annual = float(E_annual)
print(E_annual)
Lifetime = 25 # years

E_lifetime = E_annual*Lifetime
print(E_lifetime)

USD_Rand = 15

RE_cost = E_lifetime*LCOE[renewable_type]
print(RE_cost)


# Get mining equipment data
df = pd.read_excel('../Data/crypto_mining_equipment.xlsx')
#Set hardware as index
df.set_index(df["Hardware"].values)
print(df)

