import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-notebook')

path = '/Users/kartika/downloads/PythonForTrading/daily_apple_data.csv'

stock_data = pd.read_csv(path, index_col = 0)
stock_data.index = pd.to_datetime(stock_data.index)

stock_data['SAR'] = ta.SAR(stock_data['High'].values, stock_data['Low'].values,
                           acceleration = 0.02, maximum = 0.2)

stock_data['slowk'], stock_data['slowd'] = ta.STOCH(stock_data['High'].values,
                                                  stock_data['Low'].values,
                                                  stock_data['Close'].values,
                                                  fastk_period=5, slowk_period=3,
                                                  slowd_period = 3)

stock_data['fastk'], stock_data['fastd'] = ta.STOCHF(stock_data['High'].values,
                                                      stock_data['Low'].values,
                                                      stock_data['Close'].values,
                                                      fastk_period=5, fastd_period=3)
stock_data['signal'] = np.nan

stock_data.loc[(stock_data['SAR']< stock_data['Close']) &
              (stock_data['fastk'] > stock_data['slowd']), 'signal'] = 1

stock_data.loc[(stock_data['SAR'] > stock_data['Close']) &
              (stock_data['fastk'] < stock_data['slowd']), 'signal'] = -1

stock_data = stock_data.ffill()


stock_data['stock_returns'] = stock_data['Close'].pct_change()
stock_data['strategy_returns'] = (stock_data['stock_returns']*stock_data['signal'].shift(1))

stock_data = stock_data.dropna()

path = '/Users/kartika/downloads/PythonForTrading/1m_apple_data.csv'
stock_data_1m = pd.read_csv(path, index_col=0)
stock_data_1m.index = pd.to_datetime(stock_data_1m.index)
stock_data_1m.reset_index(inplace=True)

stock_data_1m = stock_data_1m.groupby([stock_data_1m['Datetime'].dt.date]).tail(5)

stock_data_1m['slippage_buy_order'] =(stock_data_1m['High']-stock_data_1m['Close'])/stock_data_1m['Close']
stock_data_1m['slippage_sell_order'] = (stock_data_1m['Close']-stock_data_1m['Low'])/stock_data_1m['Close']

stock_data_1m = stock_data_1m.groupby([stock_data_1m['Datetime'].dt.date]).mean()

print(stock_data_1m)

slippage_cost = stock_data_1m[['slippage_buy_order', 'slippage_sell_order']].max()
slippage_cost = slippage_cost.mean()

print('Estimated slippage: %.4f' % slippage_cost)

transaction_cost = 0.001
total_cost = transaction_cost + slippage_cost

trading_cost = (total_cost * np.abs(stock_data.signal - stock_data.signal.shift(1)))

stock_data['net_strategy_returns'] = stock_data['strategy_returns'] - trading_cost

cum_strategy_returns = (stock_data['net_strategy_returns']+1).cumprod()

cum_strategy_returns.plot(figsize=(10,7))

plt.title('Long Short Strategy Returns', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Strategic Net Returns', fontsize= 12)
plt.show()

total_returns = (cum_strategy_returns.iloc[-1]-1)*100
print('Total Strategy Returns are %.2f' %total_returns + '%')
