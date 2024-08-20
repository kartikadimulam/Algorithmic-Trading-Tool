import talib as ta
import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

df = yf.download('KO', start='2022-04-25', end='2024-04-19')
df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
print(df.head())

n=10
acc=0.04
max_step=0.2

df['SAR'] = ta.SAR(df['High'].values, df['Low'].values, acc,
                             max_step)


df['EMA'] = ta.EMA(df['Close'].values, timeperiod=n )


df['STOCHF'], df['STOCHS'] = ta.STOCH(df['High'].values, df['Low'].values,
                                      df['Close'].values, fastk_period=14,
                                      slowk_period=3, slowk_matype=0,
                                      slowd_period=3, slowd_matype=0)


df['Signal'] = 0

df.loc[(df['Close'] > df['EMA']) & (df['Close'] > df['SAR'])
       & (df['STOCHF'] > df['STOCHS']) & (df['STOCHF'] < 80), 'Signal']=1

df.loc[(df['Close'] < df['EMA']) & (df['Close'] < df['SAR'])
       & (df['STOCHF'] < df['STOCHS']) & (df['STOCHF'] > 22), 'Signal']=-1

df['Returns'] = df['Close'].pct_change()
df['Strategy Returns'] = df['Returns']*df['Signal'].shift(1)

df['Cumulative Returns'] = (df['Strategy Returns']+1).cumprod()

plt.figure(figsize=(10,6))
plt.plot(df['Cumulative Returns'])
plt.xlabel('Date')
plt.ylabel('Returns')
plt.show()

print(df.tail())

running_max = np.maximum.accumulate(df['Cumulative Returns'].dropna())
running_max[running_max<1] = 1

drawdown = ((df['Cumulative Returns'])/running_max - 1)*100
print('Maximum drawdown of the strategy equals {0:.2f}%'.format(drawdown.min()))

fig = plt.figure(figsize=(10,7))

plt.plot(drawdown, color='red')
plt.fill_between(drawdown.index, drawdown.values, color='red')
plt.title('Strategy Drawdown', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Drawdown(%)', fontsize=12)
plt.tight_layout()
plt.show()

def sharpe_ratio(strategy_returns):

    sharpe = round(strategy_returns.mean() /
                   strategy_returns.std() * np.sqrt(252), 2)
    return sharpe

sharpe = sharpe_ratio(df['Strategy Returns'])

print(f'Sharpe Ratio: {sharpe}')
