import numpy as np
import pandas as pd
import Capital_Outlay
import Solar_Irradiance
#import Crypto_Revenue
from datetime import datetime

disc_rate_pa = 0.06
disc_rate_pm = disc_rate_pa / 12

#Capital Outlay
C_ri = Capital_Outlay.RE_cost
C_me = Capital_Outlay.price[Capital_Outlay.m1] * Solar_Irradiance.miner_avg

#Sum monthly revenue from hrs
df = Solar_Irradiance.df
df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
monthly_df = df.resample("M", on="Date").Hourly_IPP_Revenue_Rand.sum()
print(monthly_df)

#Calculate NPV for IPP
#print("NPV for IPP sales: {}".format(np.npv(disc_rate_pm, monthly_df[1])))


# def calcNPV():
#     cf0 = float(entry1.get())
#     r = float(entry3.get()) / 100
#     cashflows = entry2.get().split(',')  # Enter values Separated by Commas
#
#     sum = 0
#     t = 0
#
#     for cf in cashflows:
#         t = t + 1
#         pv = float(cf) / (1 + r) ** t
#         sum = sum + pv
#
#     npv = sum - cf0