import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt

styles = plt.style.available
plt.style.use('seaborn-v0_8-notebook')

path = '/Users/kartikadi/downloads/PythonForTrading/daily_apple_data.csv'

stockdata = pd.read_csv(path, index_col = 0)
stockdata.index = pd.to_datetime(stockdata.index)

stockdata['SAR'] = ta.SAR(stockdata['High'].values, stockdata['Low'].values,
                           acceleration = 0.02, maximum = 0.2)

#SAR calculation is done with acc start @ 0.02 max 0.2

stockdata['slowk'], stockdata['slowd'] = ta.STOCH(stockdata['High'].values,
                                                  stockdata['Low'].values,
                                                  stockdata['Close'].values,
                                                  fastk_period=5, slowk_period=3,
                                                  slowd_period = 3)


#stochastic fast

stockdata['fastk'], stockdata['fastdata'] = ta.STOCHF(stockdata['High'].values,
                                                      stockdata['Low'].values,
                                                      stockdata['Close'].values,
                                                      fastk_period=5, fastd_period=3)

#if parablic SAR is below close and fastk crosses above slowd, BUY

stockdata['signal'] = 0

stockdata.loc[(stockdata['SAR']< stockdata['Close']) &
              (stockdata['fastk'] > stockdata['slowd']), 'signal'] = 1

#if parabloc SAR above close and fastk crosses below slowd, SELL

stockdata.loc[(stockdata['SAR'] > stockdata['Close']) &
              (stockdata['fastk'] < stockdata['slowd']), 'signal'] = -1

stockdata = stockdata.fillna(method='ffill')

stockdata['returns'] = stockdata['Close'].pct_change()
stockdata['strategy returns'] = (stockdata['returns']*stockdata['signal'].shift(1))

stockdata = stockdata.dropna()

path = '/Users/kartikadi/downloads/PythonForTrading/1m_apple_data.csv'
stockdata1m = pd.read_csv(path, index_col=0)
stockdata1m.index = pd.to_datetime(stockdata1m.index)

#model slippage (stock changes as buy is happening)
stockdata1m.reset_index(inplace=True)
stockdata1m = stockdata1m.groupby([stockdata1m['Datetime'].dt.date]).tail(5)

#for each day, extract last 5 candles

#buy slippage
stockdata1m['slippagebuyorder'] =(stockdata1m['High']-stockdata1m['Close'])/stockdata1m['Close']
#sell slippage
stockdata1m['slippagesellorder'] = (stockdata1m['Close']-stockdata1m['Low'])/stockdata1m['Close']


stockdata1m = stockdata1m.groupby([stockdata1m['Datetime'].dt.date]).mean()
#mean of all values by day

slippagecost = stockdata1m[['slippagebuyorder', 'slippagesellorder']].max()


slippagecost = slippagecost.mean()
#avg of max values

print('Anticipated slippage: %.4f' % slippagecost)

transactioncost = 0.001
totalcost = transactioncost + slippagecost

#calculate cost when you close a position
tradingcost = (totalcost * np.abs(stockdata.signal - stockdata.signal.shift(1)))



