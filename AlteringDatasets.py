import yfinance as yf

fdata = yf.download("KO", start='2019-01-01', end='2021-03-31')
fdata.head()

fdata = yf.download("KO", start='2019-01-01', end='2021-03-31', auto_adjust=True)

import pandas as pd

path = '/Users/kartikadi/Downloads/PythonForTrading/SeriesAndDataFrame/coca_cola_price.csv'
fdata = pd.read_csv(path, index_col=0)
fdata.head()
fdata.iloc[1:3]
fdata.index = pd.to_datetime(fdata.index)

path = '/Users/kartikadi/Downloads/PythonForTrading/FinancialMarketData/Simulated_Duplicate_Values.csv'
df = pd.read_csv(path, index_col='DATE',usecols=['DATE','OPEN','HIGH','LOW','CLOSE'],parse_dates=True)
df1 = df[df.duplicated(keep=False)]
df.drop_duplicates(inplace=True)

path ='/Users/kartikadi/Downloads/PythonForTrading/FinancialMarketData/Simulated_Missing_Values.csv'
df = pd.read_csv(path, index_col=0, usecols=['DATE','OPEN','HIGH','LOW','CLOSE'],parse_dates=True)
df.reindex(pd.date_range(start=df.index[0], end=df.index[-1], freq='1min'))

df = pd.read_csv('/Users/kartikadi/downloads/PFT_Files/data_modules/Simulated_Inconsistent_Data.csv',
                 index_col="DATE", usecols=['DATE','OPEN','HIGH','LOW','CLOSE'], parse_dates=True)

df['CLOSE'].diff() > 25

path ='/Users/kartikadi/downloads/PFT_Files/data_modules/1_min-MARUTI.csv'
df1 = pd.read_csv(path, index_col=0, usecols=['DATE','OPEN','HIGH','LOW','CLOSE', 'VOLUME'],parse_dates=True)
df2 = df1.resample('3Min',label='right').agg({'OPEN':'first','HIGH':'max','LOW':'min','CLOSE':'last',"VOLUME":'sum'})




