import numpy as np
import Capital_Outlay
import Solar_Irradiance
import Crypto_Revenue


#Capital Outlay
C_ri = Capital_Outlay.RE_cost
C_me = Capital_Outlay.price[Capital_Outlay.m1] * Solar_Irradiance.miner_avg

Rev = sum(Crypto_Revenue.df["Monthly revenue (USD)"])