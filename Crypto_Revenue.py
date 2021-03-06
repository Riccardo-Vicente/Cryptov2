import pandas as pd
import Capital_Outlay
import Solar_Irradiance
from datetime import datetime
import math

crypto = Solar_Irradiance.crypto
pool_fee = 0.02
solar_idx = 0

if crypto == "BTC":
    blocks_per_hr = 6

    # Read BTC file
    df = pd.read_csv("Data/BTC_Price_Daily.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    for ind, row in df.iterrows():

        if row["Date"] < datetime(2016, 1, 1):
            miner_choice = Capital_Outlay.m1
            miner_avg = Solar_Irradiance.miner_1_avg
        elif row["Date"] < datetime(2020, 1, 1):
            miner_choice = Capital_Outlay.m2
            miner_avg = Solar_Irradiance.miner_2_avg
        else:
            miner_choice = Capital_Outlay.m3
            miner_avg = Solar_Irradiance.miner_3_avg

        miner_frac = (Capital_Outlay.hash_rate[miner_choice]/1000) / row["Hashrate(TH/s)"]
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

            if solar_row["Number of miners"] <= miner_avg:
                no_miners = solar_row["Number of miners"]
            else:
                no_miners = miner_avg

            IPP_rev = no_miners * USD_reward_per_hr
            pool_fees = pool_fee * IPP_rev
            Hrly_IPP_rev = round((IPP_rev - pool_fees), 2)
            Solar_Irradiance.df.loc[solar_idx, "BTC_Hourly_Revenue_Rand"] = Hrly_IPP_rev * Capital_Outlay.USD_Rand

            solar_idx += 1
            try:
                solar_row = Solar_Irradiance.df.iloc[solar_idx]
            except IndexError:
                break
            solar_day = datetime(round(solar_row["Year"]), round(solar_row["Month"]), round(solar_row["Day"]))

if crypto == "ETH":
    # Read ETH file
    df = pd.read_csv("Data/ETH_Price_Daily.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    for ind, row in df.iterrows():

        if row["Date"] < datetime(2020, 1, 1):
            miner_choice = Capital_Outlay.m2
            miner_avg = Solar_Irradiance.miner_2_avg
        else:
            miner_choice = Capital_Outlay.m3
            miner_avg = Solar_Irradiance.miner_3_avg

        miner_frac = (Capital_Outlay.hash_rate[miner_choice]) / row["Hashrate (GH/s)"]
        df.loc[ind, "Miner Fraction"] = miner_frac

        if row["Date"] < datetime(2017, 1, 1):
            block_reward = 5
        elif row["Date"] < datetime(2019, 1, 1):
            block_reward = 3
        else:
            block_reward = 2

        reward_per_block = miner_frac * block_reward
        reward_per_hr = reward_per_block * (row["Blocks per day"]/24)

        solar_row = Solar_Irradiance.df.iloc[solar_idx]
        solar_day = datetime(round(solar_row["Year"]), round(solar_row["Month"]), round(solar_row["Day"]))

        while solar_day == row["Date"]:

            USD_reward_per_hr = reward_per_hr * row["ETH Price (USD)"]

            if solar_row["Number of miners"] <= miner_avg:
                no_miners = solar_row["Number of miners"]
            else:
                no_miners = miner_avg

            IPP_rev = no_miners * USD_reward_per_hr
            pool_fees = pool_fee * IPP_rev
            Hrly_IPP_rev = round((IPP_rev - pool_fees), 2)
            Solar_Irradiance.df.loc[solar_idx, "ETH_Hourly_Revenue_Rand"] = Hrly_IPP_rev * Capital_Outlay.USD_Rand

            solar_idx += 1
            try:
                solar_row = Solar_Irradiance.df.iloc[solar_idx]
            except IndexError:
                break
            solar_day = datetime(round(solar_row["Year"]), round(solar_row["Month"]), round(solar_row["Day"]))

print(Solar_Irradiance.df)
Solar_Irradiance.df.to_csv('Hourly_Revenue_File.csv', sep=',')
