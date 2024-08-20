import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use('seaborn-v0_8-notebook')

data = yf.download('AAPL', start='2020-04-20', end='2022-04-13')

data['Log Returns'] = np.log(data['Adj Close']/data['Adj Close'].shift(1))

print(data.head())

data['20 day Volatility'] = 100*data['Log Returns'].rolling(window=20).std()*np.sqrt(20)

plt.figure(figsize=(9,6))
plt.plot(data['20 day Volatility'], color='b')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Volatility', fontsize=12)
plt.title('20 day Volatility', fontsize=14)
plt.show()

