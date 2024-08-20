import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-dark-palette')

def call_payoff(sT, strike_price, premium):
    pnl = np.where(sT > strike_price, sT-strike_price, 0)
    return pnl - premium

spot_price = 900
strike_price = 900
premium = 20

sT = np.arange(0.9*spot_price, 1.1*spot_price)
payoff_long_call = call_payoff(sT, strike_price, premium)

fig, ax = plt.subplots(figsize=(10,6))
ax.spines['bottom'].set_position('zero')
ax.plot(sT, payoff_long_call, label='Call option buyer payoff')
plt.xlabel('INFSYS Asset Price')
plt.ylabel('Profit/Loss')
plt.legend()
plt.show()

payoff_short_call = payoff_long_call * -1.0

fig, ax = plt.subplots(figsize=(10,6))
ax.spines['bottom'].set_position('zero')
ax.plot(sT, payoff_short_call, label='Call option seller payoff')
plt.xlabel('INFSYS Asset Price')
plt.ylabel('Profit/Loss')
plt.legend()
plt.show()
