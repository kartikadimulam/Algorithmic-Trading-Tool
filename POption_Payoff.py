import numpy as np
import matplotlib.pyplot

plt.style.use('seaborn-v0_8-notebook')

def put_payoff(sT, strike_price, premium):
    pnl. np.where(sT < strike_price, strike_price-sT, 0)
    return pnl-premium

spot_price = 900
strike_price = 900
premium = 20

sT = np.arange(0.9*spot_price, 1.1*spot_price)

payoff_long_put = put_payoff(sT, strike_price, premium)

fig, ax = plt.subplots(figsize=(10,6))
ax.spines['bottom'].set_position('zero')
ax.plot(sT, payoff_long_put, label = 'Put option buyer payoff')

plt.xlabel('Infosys Stock Price')
plt.ylabel('Profit and loss')
plt.legend()
plt.show()

payoff_short_put = payoff_long_put * -1.0

fig, ax = plt.subplots(figsize=(10,6))
ax.spines['bottom'].set_position('zero')
ax.plot(sT, payoff_short_put, label='Put option seller payoff', color='r')
plt.xlabel('Infosys Stock Price')
plt.ylabel('Profit and loss')
plt.legend()
plt.show()
