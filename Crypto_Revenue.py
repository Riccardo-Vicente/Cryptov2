import pandas as pd
import Capital_Outlay
import Solar_Irradiance
from datetime import datetime

df = pd.read_csv("Data/BTC_Price_Daily.csv", parse_dates=['Date'])
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date")

solar_idx = 0
blocks_per_hr = 6

for ind, row in df.iterrows():
    miner_frac = (Capital_Outlay.hash_rate[Capital_Outlay.m1]/1000) / row["Hashrate(TH/s)"]
    df.loc[ind, "Miner Fraction"] = miner_frac

    if row["Date"] < datetime(2012,11,28):
        block_reward = 50
    elif row["Date"] < datetime(2016,7,9):
        block_reward = 25
    elif row["Date"] < datetime(2020,5,11):
        block_reward = 12.5
    else:
        block_reward = 6.25

    reward_per_block = miner_frac*block_reward
    reward_per_hr = reward_per_block*blocks_per_hr

   # df.loc[ind, "Miner reward per hr (USD)"] = reward_per_hr*row["BTC Price (USD)"]

    solar_row = Solar_Irradiance.df.iloc[solar_idx]
    solar_day = datetime(round(solar_row["Year"]), round(solar_row["Month"]), round(solar_row["Day"]))

    while solar_day == row["Date"]:
        # DO STUFF
        USD_reward_per_hr = reward_per_hr * row["BTC Price (USD)"]
        Solar_Irradiance.df.loc[ind, "Miner reward per hr (USD)"] = solar_row["Number of miners"] * USD_reward_per_hr

        solar_idx += 1
        solar_row = Solar_Irradiance.df.iloc[solar_idx]
        solar_day = datetime(round(solar_row["Year"]), round(solar_row["Month"]), round(solar_row["Day"]))

print(Solar_Irradiance.df)