import pandas as pd
import numpy as np

list1 = [1,2,3,np.nan,6,8]
s = pd.Series(list1)
s.head()
s.head(2)
s.tail()
s.tail(3)

dict1 = {'karti':5.7, 'nardo':6.4}
s = pd.Series(dict1)


df = pd.DataFrame({'one' : pd.Series(np.random.randn(3),index=['a','b','c']),
                   'two' : pd.Series(np.random.randn(4),index=['a','b','c','d']),
                   'three' : pd.Series(np.random.randn(5),index=['a','b','c','d','e'])
                   })


df.dtypes
df.head(2)
df.index
df.index[[1,2]]
df.describe()
#Summary Stats for each row
df.values
#Raw values
df.columns
df.T
# Transpose (flip values)
df.loc['a']
#takes name of row
df.iloc[1]
df.iloc[1:4]
#takes index of row
path = '/Users/kartikadi/Downloads/PythonForTrading/SeriesAndDataFrame/'
coca_cola = pd.read_csv(path+'coca_cola_price.csv', index_col=0)
#index_col determines which column from the csv file to use for indexing purposes
#values of open column biger than 48
coca_cola[coca_cola.Open > 48 ]
coca_cola['Open']
coca_cola['Open'].head()
coca_cola.loc['2019-01-02','Open']
#opens a few rows of open
coca_cola.loc['2019-01-02' : '2021-03-24','Open']

#dropping rows
coca_cola.drop(coca_cola.index[[1, 2]])
coca_cola = coca_cola.drop(coca_cola.index[[1,4]])
#another way, using names not indexes
coca_cola.drop(['2019-01-02','2019-01-04'])

#dropping columns
coca_cola.drop(['Open','Close'], axis=1)
#Axis specifies columns are being dropped but unnecessary here

#add column
coca_cola['SMA']= coca_cola['Close'].rolling(window=10).mean()
