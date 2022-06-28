import pandas as pd
import numpy as np
import Capital_Outlay
import Solar_Irradiance
from datetime import datetime

#Read BTC file
df = pd.read_csv("Data/BTC_Price_Daily.csv", parse_dates=['Date'])
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date")

#Read ETH file
# eth_df = pd.read_csv("Data/ETH_Price_Daily.csv")
# eth_df["Date"] = pd.to_datetime(eth_df["Date"])

#crypto = "BTC"

solar_idx = 0
blocks_per_hr = 6
pool_fee = 0.02

#if crypto == "BTC":
for ind, row in df.iterrows():
    miner_frac = (Capital_Outlay.hash_rate[Capital_Outlay.m1]/1000) / row["Hashrate(TH/s)"]
    df.loc[ind, "Miner Fraction"] = miner_frac

    if row["Date"] < datetime(2012, 11, 28):
        block_reward = 50
    elif row["Date"] < datetime(2016, 7, 9):
        block_reward = 25
    elif row["Date"] < datetime(2020, 5, 11):
        block_reward = 12.5
    else:
        block_reward = 6.25

    reward_per_block = miner_frac*block_reward
    reward_per_hr = reward_per_block*blocks_per_hr

    solar_row = Solar_Irradiance.df.iloc[solar_idx]
    solar_day = datetime(round(solar_row["Year"]), round(solar_row["Month"]), round(solar_row["Day"]))

    while solar_day == row["Date"]:
        USD_reward_per_hr = reward_per_hr * row["BTC Price (USD)"]
        IPP_rev = solar_row["Number of miners"] * USD_reward_per_hr
        pool_fees = pool_fee * IPP_rev
        Solar_Irradiance.df.loc[solar_idx, "Hourly Revenue (Rand)"] = round((IPP_rev - pool_fees), 2)*Capital_Outlay.USD_Rand

        solar_idx += 1
        solar_row = Solar_Irradiance.df.iloc[solar_idx]
        solar_day = datetime(round(solar_row["Year"]), round(solar_row["Month"]), round(solar_row["Day"]))

print(Solar_Irradiance.df)

# if crypto == "ETH":
#     for ind, row in eth_df.iterrows():
#         miner_frac = (Capital_Outlay.hash_rate[Capital_Outlay.m1] / 1000) / row["Hashrate(GH/s)"]
#         df.loc[ind, "Miner Fraction"] = miner_frac
#
#         if row["Date"] < datetime(2017, 1, 1):
#             block_reward = 5
#         elif row["Date"] < datetime(2019, 1, 1):
#             block_reward = 3
#         else:
#             block_reward = 2
#
#         reward_per_block = miner_frac * block_reward
#         reward_per_hr = reward_per_block * (row["Blocks per day"]/24)