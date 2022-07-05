import numpy as np
import pandas as pd
import Capital_Outlay
import Solar_Irradiance
import Crypto_Revenue
from datetime import datetime

disc_rate_pa = 0.06
disc_rate_pm = disc_rate_pa / 12

#Capital Outlay
C_ri = Capital_Outlay.RE_cost
C_me = Capital_Outlay.price[Capital_Outlay.m1] * Solar_Irradiance.miner_avg

#Sum monthly IPP revenue from hrs
df = Solar_Irradiance.df
df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
monthly_df = df.resample("M", on="Date").Hourly_IPP_Revenue_Rand.sum()
print("\nMonthly revenue for IPP sales:\n")
print(monthly_df)

#Calculate NPV for IPP
r = disc_rate_pm
sum = 0
t = 0
for row in monthly_df:
    t = t + 1
    pv = float(monthly_df[1]) / (1 + r) ** t
    sum = sum + pv
PV = round(sum, 2)
print("\nPV for IPP sales: R{}".format(PV))

NPV = PV - C_ri
print("\nNPV for IPP sales: R{}\n".format(round(NPV, 2)))

#Sum monthly Crypto revenue from hrs
if Solar_Irradiance.crypto == "BTC":
    monthly_df = df.resample("M", on="Date").BTC_Hourly_Revenue_Rand.sum()
if Solar_Irradiance.crypto == "ETH":
    monthly_df = df.resample("M", on="Date").ETH_Hourly_Revenue_Rand.sum()
print("\nMonthly revenue for Crypto mining:\n")
print(monthly_df)

#Calculate NPV for Crypto
r = disc_rate_pm
sum = 0
t = 0
for row in monthly_df:
    t = t + 1
    pv = float(monthly_df[1]) / (1 + r) ** t
    sum = sum + pv
PV = round(sum, 2)
print("\nPV for crypto mining: R{}".format(PV))

NPV = PV - C_ri - C_me
print("\nNPV for crypto mining: R{}\n".format(round(NPV, 2)))
