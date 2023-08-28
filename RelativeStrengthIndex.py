import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt

availablestyles = plt.style.available
plt.style.use('_classic_test_patch')

path = '/Users/kartikadi/downloads/PythonForTrading/gld_price_2012.csv'
gldprice = pd.read_csv(path, index_col=0)

gldprice.index = pd.to_datetime(gldprice.index)

period = 14
#default period used for RSI calculations

gldprice['RSI'] = ta.RSI(gldprice['Close'], period)
#ta.rsi always uses the close price and period as parameters


(gldprice['RSI']>70).sum()
#count the number of overbought

gldprice['Signal'] = 0

gldprice.loc[gldprice['RSI']>70, 'Signal'] = 1
gldprice.loc[gldprice['RSI']<30, 'Signal'] = -1

(gldprice['Signal']==1).sum()
#another way to count overbought days

dataforplot = gldprice[-200:]
#show last 200 points
fig = plt.figure(figsize=(15,10))

ax1 = fig.add_subplot(211)
#specifies that there are two rows of plots, 1 column of plots, and ax1 is at position 1 
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

#finds rows where the RSI goes from 0 to 1 in the close column
#marks datapoints with a size 10 green ^

#similarly, finds rows where RSI goes from 0 to -1 in the close column
#marks datapoints with a size 10 red >

ax1.legend()
#establishes legend

ax2 = fig.add_subplot(212)
# add plot into the second row first column of established figure, at pos 2


ax2.set_title('Relative Strength Index', fontsize=14)
ax2.set_xlabel('Date', fontsize=12)
ax2.set_ylabel('RSI Value', fontsize=12)
ax2.plot(dataforplot['RSI'], color='olive')
ax2.axhline(70, color = 'red')
#adds horizontal axis at value 70
ax2.axhline(30, color='green')

plt.show()




