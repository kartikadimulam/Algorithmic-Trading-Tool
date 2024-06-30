
import pandas as pd

path = './data/jpm_and_bac_price.csv'
df1 = pd.read_csv(path,index_col=0)
df1.index = pd.to_datetime(df1.index)

df1.head()

import matplotlib.pyplot as plt
import matplotlib.style as style

style.use('seaborn-v0_8-white')

#line graph

df1['Close_BAC'].plot(figsize=(10,7),color='green')

plt.title('Closing Price of BAC', fontsize=14)
plt.xlabel('Year-Month',fontsize=12)
plt.ylabel('Price ($)', fontsize=12)


plt.show()


#scatter plot




df1.plot(x='Close_BAC', y='Close_JPM', figsize=(10,7),kind='scatter')

plt.title('BAC Price Vs. JPM Price', fontsize=14)
plt.xlabel('BAC Price', fontsize=12)
plt.ylabel('JPM Price', fontsize=12)
plt.show()


#histogram
df1['daily_returns_BAC'].plot(figsize=(10,7), color='purple', kind='hist')
#kind and color must be specified within the parameter
#ylabel, title, xtitle can be added later and should for easibility
plt.title('Daily Returns of BAC', fontsize=12)
plt.ylabel('Frequency',fontsize=12)
plt.xlabel('Returns', fontsize=12)
plt.grid(True)
plt.show()








