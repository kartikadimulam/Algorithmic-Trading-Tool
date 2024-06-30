import yfinance as yf
import pandas as pd

fdata = yf.download("KO", start='2019-01-01', end='2021-03-31', auto_adjust=True)
fdata.index = pd.to_datetime(fdata.index)
print(fdata)

fdata.iloc[1:3]

path = './data/Simulated_Duplicate_Values.csv'
df = pd.read_csv(path, index_col='DATE',usecols=['DATE','OPEN','HIGH','LOW','CLOSE'],parse_dates=True)

df1 = df[df.duplicated(keep=False)]
df.drop_duplicates(inplace=True)
print(df)
path ='./data/Simulated_Missing_Values.csv'
df = pd.read_csv(path, index_col=0, usecols=['DATE','OPEN','HIGH','LOW','CLOSE'],parse_dates=True)
df.reindex(pd.date_range(start=df.index[0], end=df.index[-1], freq='1min'))

df = pd.read_csv('./data/Simulated_Inconsistent_Data.csv',
                 index_col="DATE", usecols=['DATE','OPEN','HIGH','LOW','CLOSE'], parse_dates=True)

df['CLOSE'].diff() > 25

path ='./data/1_min-MARUTI.csv'
df1 = pd.read_csv(path, index_col=0, usecols=['DATE','OPEN','HIGH','LOW','CLOSE', 'VOLUME'],parse_dates=True)
df2 = df1.resample('3Min',label='right').agg({'OPEN':'first','HIGH':'max','LOW':'min','CLOSE':'last',"VOLUME":'sum'})

