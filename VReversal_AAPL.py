import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

data = yf.download('AAPL', start='2022-01-19', end = '2023-05-04')
print(data.head())

data['5d_change'] = data['Close'].shift(1)-data['Close'].shift(6)

data['100d_std'] = data['5d_change'].rolling(window=100).std()

data['5d_avgvol'] = data['Volume'].shift(1).rolling(window=5).mean()

data['prev 5d_avgvol'] = data['5d_avgvol'].shift(5)

data['signal'] = 0

data.loc[( (data['5d_change'].abs() > data['100d_std']) &
          (data['5d_avgvol']<data['prev 5d_avgvol']) & (data['5d_change']<0)), 'signal'] = 1

print(data[data['signal']==1])

data['c_signal'] = 0
data['exit'] = 0

for i in range(len(data)):
    if (data.iloc[i]['signal'] != 0) & (data.iloc[i]['signal']!= data.iloc[i-1]['c_signal']):
        data.iloc[i, data.columns.get_loc('c_signal')] = data.iloc[i, data.columns.get_loc('signal')]

        if data['signal'].iloc[i] == 1:
            data.iloc[i, data.columns.get_loc('exit')] = 1
        else:
            data.iloc[i, data.columns.get_loc('exit')] = -1

    if (data['signal'].iloc[i] != 0) & (data['signal'].iloc[i] == data['c_signal'].iloc[i-1]):
        data.iloc[i, data.columns.get_loc('c_signal')] = data['c_signal'].iloc[i-1]

        if data['c_signal'].iloc[i-1] == 1:
            data.iloc[i, data.columns.get_loc('exit')] = int(data['exit'].iloc[i-1]) + 1

        else:
            data.iloc[i, data.columns.get_loc('exit')] = int(data['exit'].iloc[i-1]) - 1

    if (data['signal'].iloc[i] == 0) & (data['exit'].iloc[i-1]<5) & (data['exit'].iloc[i-1]>0):
        data.iloc[i, data.columns.get_loc('c_signal')] = data['c_signal'].iloc[i-1]
        data.iloc[i, data.columns.get_loc('exit')] = int(data['exit'].iloc[i-1]) + 1

    if (data['signal'].iloc[i]==0) & (data['exit'].iloc[i-1] > -5) & (data['exit'].iloc[i-1] < 0):
        data.iloc[i, data.columns.get_loc('c_signal')] = data['c_signal'].iloc[i-1]
        data.iloc[i, data.columns.get_loc('exit')] = int(data['exit'].iloc[i-1]) - 1

    if (data['signal'].iloc[i]==0) & ((data['exit'].iloc[i-1]==5) | (data['exit'].iloc[i-1]==-5)):
        data.iloc[i, data.columns.get_loc('c_signal')] = 0
        data.iloc[i, data.columns.get_loc('exit')] = 0

print(data[data['exit'] != 0])

data['returns'] = data['Close'].pct_change()

data['strat returns'] = data['returns'] * data['c_signal'].shift(1)
data['cumulative strat returns'] = 0.0
data['cumulative market returns'] = 0.0

data['cumulative strat returns'] = data['cumulative strat returns'].astype(float)
data['cumulative market returns'] = data['cumulative market returns'].astype(float)

data.iloc[100:, data.columns.get_loc('cumulative strat returns')] = (data['strat returns'].iloc[100:]+1).cumprod()
data.iloc[100:, data.columns.get_loc('cumulative market returns')] = (data['returns'].iloc[100:]+1).cumprod()

print(data[['cumulative market returns', 'cumulative strat returns', 'c_signal']].tail())

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.figure(figsize=(10,7))
plt.plot(data['cumulative strat returns'].iloc[100:], color='g', label='Volume Reversal Strategy Returns')
plt.plot(data['cumulative market returns'].iloc[100:], color='r', label = 'Regular Market Returns')
plt.xlabel('Date')
plt.ylabel('Returns')
plt.show()

sharpe = (data['cumulative strat returns'].iloc[-1]-data['cumulative market returns'].iloc[-1])/data['cumulative strat returns'].std()
print(sharpe)
