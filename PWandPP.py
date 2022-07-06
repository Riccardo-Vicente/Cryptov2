import pandas as pd
import Capital_Outlay
import Solar_Irradiance
import Crypto_Revenue
from datetime import datetime

# ----------------------------------------------------------------------------------
# Present Worth
# ----------------------------------------------------------------------------------
disc_rate_pa = 0.1
disc_rate_pm = disc_rate_pa / 12
four_yr_fact = 0.9674
eight_yr_fact = 0.9358

# Capital Outlay
C_ri = Capital_Outlay.RE_cost
# PV of mining equipment
C_m1 = Capital_Outlay.price[Capital_Outlay.m1] * Solar_Irradiance.miner_1_avg
C_m2 = Capital_Outlay.price[Capital_Outlay.m2] * Solar_Irradiance.miner_2_avg
C_m3 = Capital_Outlay.price[Capital_Outlay.m3] * Solar_Irradiance.miner_3_avg
C_me = C_m1 + C_m2 + C_m3
# Sum monthly IPP revenue from hrs
df = Solar_Irradiance.df
df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
monthly_df = df.resample("M", on="Date").Hourly_IPP_Revenue_Rand.sum()
print("\nMonthly revenue for IPP sales:\n")
print(monthly_df)

# Calculate NPV for IPP
r = disc_rate_pm
sum = 0
t = 0
for row in monthly_df:
    t = t + 1
    pv = float(row) / (1 + r) ** t
    sum = sum + pv
PV = round(sum, 2)
print("\nPV for IPP sales: R{}".format(PV))
print("Cost of renewable infrustructure: R{}".format(C_ri))

NPV = PV - C_ri
print("\nPresent Worth for IPP sales: R{}\n".format(round(NPV, 2)))

# Sum monthly Crypto revenue from hrs
if Solar_Irradiance.crypto == "BTC":
    monthly_df = df.resample("M", on="Date").BTC_Hourly_Revenue_Rand.sum()
if Solar_Irradiance.crypto == "ETH":
    monthly_df = df.resample("M", on="Date").ETH_Hourly_Revenue_Rand.sum()
print("\nMonthly revenue for Crypto mining:\n")
print(monthly_df)

# Calculate NPV for Crypto
r = disc_rate_pm
sum = 0
t = 0
for row in monthly_df:
    t = t + 1
    pv = float(row) / (1 + r) ** t
    sum = sum + pv
PV = round(sum, 2)
print("\nPV for crypto mining: R{}".format(PV))
print("Cost of renewable infrastructure: R{}".format(C_ri))
print("Cost of crypto mining equipment: R{}".format(C_me))

NPV = PV - C_ri - (C_m1 + C_m2*four_yr_fact + C_m3*eight_yr_fact)
print("\nPresent Worth for crypto mining: R{}\n".format(round(NPV, 2)))

# ----------------------------------------------------------------------------------
# Payback Period
# ----------------------------------------------------------------------------------

# Calculate PP for IPP sales
annual_df = df.resample("Y", on="Date").Hourly_IPP_Revenue_Rand.sum()
print("\nAnnual revenue for IPP sales:\n")
print(annual_df)

capital = C_ri
cum_sum = - capital
yr_count = 0
for row in annual_df:
    cf = row
    yr_partial = abs(cum_sum/cf)
    cum_sum = cum_sum + cf
    yr_count += 1

    if cum_sum > 0:
        break
print(yr_count)
print(yr_partial)
pp = round(yr_count - 1 + yr_partial, 1)
print("Payback period for IPP sales: {} years".format(pp))

# Calculate PP for crypto mining
if Solar_Irradiance.crypto == "BTC":
    annual_df = df.resample("Y", on="Date").BTC_Hourly_Revenue_Rand.sum()
if Solar_Irradiance.crypto == "ETH":
    annual_df = df.resample("Y", on="Date").ETH_Hourly_Revenue_Rand.sum()
print("\nAnnual revenue for Crypto mining:\n")
print(annual_df)

if Solar_Irradiance.crypto == "BTC":
    capital = C_ri + C_m1
if Solar_Irradiance.crypto == "ETH":
    capital = C_ri + C_m2
cum_sum = - capital
yr_count = 0

for row in annual_df:
    cf = row
    yr_partial = abs(cum_sum/cf)
    cum_sum = cum_sum + cf
    if yr_count == 4:
        if Solar_Irradiance.crypto == "BTC":
            cum_sum = cum_sum - C_m2
        else:
            cum_sum = cum_sum - C_m3
    yr_count += 1

    if cum_sum > 0:
        break
print(yr_count)
print(yr_partial)
pp = round(yr_count - 1 + yr_partial, 1)
print("Payback period for Crypto mining: {} years".format(pp))
