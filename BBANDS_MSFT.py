import talib as ta
from talib import MA_Type
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

df = yf.download('MSFT', start='2023-01-04', end='2024-05-04')
df.index = pd.to_datetime(df.index)

n=60
df['Returns'] = df['Close'].pct_change()
df['Return Std'] = df['Returns'].rolling(window=n).std()

df['upper'], df['middle'], df['lower'] = ta.BBANDS(df['Close'].values, matype=MA_Type.T3)

print(df.tail())

df['Signal'] = 0

df.loc[(df['upper'].shift(2) > df['Close'].shift(2)) & (df['upper'].shift(1) < df['Close'].shift(1))
       & (df['Return Std'].shift(1) < df['Returns'].shift(1)), 'Signal'] = -1

df.loc[(df['lower'].shift(2) < df['Close'].shift(2)) & (df['lower'].shift(1) >df['Close'].shift(1))
       & (-df['Return Std'].shift(1) > df['Returns'].shift(1)), 'Signal'] = 1

df['Strategy Returns'] = df['Signal'].shift(1)*df['Returns']
trades= np.count_nonzero(df['Signal'])

plt.figure(figsize=(11,7))
plt.plot((df['Strategy Returns']+1).cumprod())
plt.figtext(0.14, 0.9, s='\n\nTrades:%i' % trades)
plt.xlabel('Date')
plt.ylabel('Cumulative Strategy Returns')
plt.show()
