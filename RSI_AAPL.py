import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use('_classic_test_patch')

gldprice = yf.download("AAPL", start='2022-01-03', end='2023-11-03')
gldprice.index = pd.to_datetime(gldprice.index)

period = 14
gldprice['RSI'] = ta.RSI(gldprice['Close'], period)


(gldprice['RSI']>70).sum()

gldprice['Signal'] = 0

gldprice.loc[gldprice['RSI']>70, 'Signal'] = 1
gldprice.loc[gldprice['RSI']<30, 'Signal'] = -1

(gldprice['Signal']==1).sum()

dataforplot = gldprice[-200:]

fig = plt.figure(figsize=(15,10))

ax1 = fig.add_subplot(211)

ax1.set_title('Trading Signals', fontsize=14)
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Price', fontsize=12)

ax1.plot(dataforplot['Close'], label='Close' )

ax1.plot(dataforplot[(dataforplot['Signal']==1) &
                     (dataforplot['Signal'].shift(1)==0)]['Close'], r'^', ms=10,
         label='Long Signal', color='green')

ax1.plot(dataforplot[(dataforplot['Signal']==-1) &
                     (dataforplot['Signal'].shift(1)==0)]['Close'], r'>', ms=10,
         label='Short Signal', color='red')

ax1.legend()

ax2 = fig.add_subplot(212)

ax2.set_title('Relative Strength Index', fontsize=14)
ax2.set_xlabel('Date', fontsize=12)
ax2.set_ylabel('RSI Value', fontsize=12)
ax2.plot(dataforplot['RSI'], color='olive')
ax2.axhline(70, color = 'red')

ax2.axhline(30, color='green')

plt.show()




