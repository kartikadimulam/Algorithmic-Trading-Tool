import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use('seaborn-v0_8-notebook')

path = './data/daily_apple_data.csv'

stock_data = yf.download("NVDA", start='2021-01-03', end='2023-11-03')
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

stock_data.loc[(stock_data['SAR']< stock_data['Close']) & (stock_data['fastd']>stock_data['slowd']) & 
              (stock_data['fastk'] > stock_data['slowk']), 'signal'] = 1

stock_data.loc[(stock_data['SAR'] > stock_data['Close']) & (stock_data['fastd']<stock_data['slowd']) &
              (stock_data['fastk'] < stock_data['slowk']), 'signal'] = -1

stock_data = stock_data.ffill()


stock_data['stock_returns'] = stock_data['Close'].pct_change()
stock_data['strategy_returns'] = (stock_data['stock_returns']*stock_data['signal'].shift(1))

stock_data = stock_data.dropna()

path = './data/1m_apple_data.csv'
stock_data_1m = pd.read_csv(path, index_col=0)
stock_data_1m.index = pd.to_datetime(stock_data_1m.index)
stock_data_1m.reset_index(inplace=True)

stock_data_1m = stock_data_1m.groupby([stock_data_1m['Datetime'].dt.date]).tail(5)

stock_data_1m['slippage_buy_order'] =(stock_data_1m['High']-stock_data_1m['Close'])/stock_data_1m['Close']
stock_data_1m['slippage_sell_order'] = (stock_data_1m['Close']-stock_data_1m['Low'])/stock_data_1m['Close']

stock_data_1m = stock_data_1m.groupby([stock_data_1m['Datetime'].dt.date]).mean()

slippage_cost = stock_data_1m[['slippage_buy_order', 'slippage_sell_order']].max()
slippage_cost = slippage_cost.mean()

print('Estimated slippage: %.4f' % slippage_cost)

transaction_cost = 0.001
total_cost = transaction_cost + slippage_cost

trading_cost = (total_cost * np.abs(stock_data.signal - stock_data.signal.shift(1)))

stock_data['net_strategy_returns'] = stock_data['strategy_returns'] - trading_cost

cum_strategy_returns = ((stock_data['net_strategy_returns']+1).cumprod())
cum_strategy_returns.plot(figsize=(10,7))

plt.title('Long and Short Strategy Returns', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Strategic Net Returns', fontsize= 12)
plt.show()
total_returns = (cum_strategy_returns.iloc[-1]-1)*100
print('Total Strategy Returns are %.2f' %total_returns + '%')

days = len(cum_strategy_returns)
cagr = (cum_strategy_returns.iloc[-1]**(252/days)-1)*100
print('Strategy CAGR is %.2f' % cagr + '%')

risk_free_rate = 0.04/252
sharpe= np.sqrt(252)*(np.mean(stock_data.strategy_returns) -
                      (risk_free_rate))/np.std(stock_data.strategy_returns)
print('Sharpe ratio of this strategy is %.2f' % sharpe)

running_max = np.maximum.accumulate(cum_strategy_returns.dropna())
running_max[running_max < 1] = 1

drawdown = (cum_strategy_returns)/running_max -1
max_dd = drawdown.min()*100

drawdown.plot(figsize=(10,7), color='r')
plt.ylabel('Drawdown', fontsize=12)
plt.title('Long and Short Strategy Drawdown', fontsize=14)
plt.fill_between(drawdown.index, drawdown.values, color='red')
plt.grid(which='major', color='k', linestyle='-.', linewidth=0.2)
plt.show()

print('Maximum drawdown of Long and Short strategy is %.2f' % max_dd + '%')


stock_data['new_signal'] = np.nan

stock_data.loc[(stock_data['SAR'] < stock_data['Close']) & (stock_data['fastk'] > stock_data['slowd']),
              'new_signal'] = 1

stock_data.loc[(stock_data['SAR'] > stock_data['Close']) & (stock_data['fastk'] < stock_data['slowd']),
              'new_signal'] = 0

stock_data = stock_data.ffill()

stock_data['new_strategy_returns'] = (stock_data['stock_returns']*stock_data['new_signal'].shift(1))

stock_data['net_new_strategy_returns'] = stock_data['new_strategy_returns'] - trading_cost

stock_data = stock_data.dropna()

cum_new_strategy_returns = (stock_data['net_new_strategy_returns']+1).cumprod()
cum_new_strategy_returns.plot(figsize=(10,7))

plt.title('Long Only Strategy Returns', fontsize=15)
plt.xlabel('Date', fontsize = 13)
plt.ylabel('New Strategy Returns', fontsize= 12)
plt.show()

total_new_returns = (cum_new_strategy_returns.iloc[-1]-1)*100
print('Total Long Only Strategy Returns are %.2f' %total_new_returns + '%')

new_cagr = (cum_new_strategy_returns.iloc[-1]**(252/days)-1)*100
print('Long Only Strategy CAGR is %.2f' % new_cagr + '%')

new_sharpe = np.sqrt(252)*(np.mean(stock_data.new_strategy_returns) -
                           (risk_free_rate))/np.std(stock_data.new_strategy_returns)
print('The Sharpe ratio of the long only strategy is %.2f' % sharpe)

new_running_max = np.maximum.accumulate(cum_new_strategy_returns.dropna())
new_running_max[new_running_max<1]=1
new_drawdown = (cum_new_strategy_returns)/new_running_max - 1
new_max_dd = new_drawdown.min()*100

new_drawdown.plot(figsize=(10,7))
plt.ylabel('Long Only Drawdown', fontsize=12)
plt.title('Long Only Strategy Drawdown', fontsize=14)
plt.fill_between(new_drawdown.index, new_drawdown.values, color='red')
plt.grid(which='major',color='k', linestyle = '-.', linewidth=0.2)
plt.show()

print('Maximum drawdown of Long Only Strategy is %.2f' % new_max_dd + '%')

from tabulate import tabulate 

stats = tabulate(
    [
        ['Strategy Returns', total_returns, total_new_returns],
        ['Sharpe', sharpe, new_sharpe],
        ['CAGR', cagr, new_cagr],
        ['Maximum Drawdown', max_dd, new_max_dd]
        ],
    headers = ['Stats Name', 'Long and Short Strategy', 'Long Only Strategy'],
    tablefmt = 'orgtbl')

print(stats)



