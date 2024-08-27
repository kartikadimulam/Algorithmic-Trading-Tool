import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import math 
import warnings

plt.style.use('tableau-colorblind10')

data = yf.download('WFC', start='2021-12-25', end='2023-05-04')

data['Daily Returns'] = data['Adj Close'].pct_change()*100

data['SD'] = data['Daily Returns'].rolling(window=14).std()

data['Annual Volatility'] = data['SD']*(math.sqrt(252))
print(data.head())

data.dropna(inplace=True)

warnings.filterwarnings('ignore')

plt.figure(figsize=(16,8))
plt.plot(data['Daily Returns'])
plt.title('WFC Daily Return')
plt.xlabel('Date')
plt.ylabel('Daily % Return')
plt.legend(['Daily Return'])
plt.show()

from statsmodels.tsa.stattools import adfuller

p_value = adfuller(data['Daily Returns'])[1]

if p_value > 0.05:
    print('P Value: {} > 0.05, fail to reject null, nonstationary time series'
          .format(p_value))
else:
    print('P Value: {} < 0.05, reject null, stationary time series'
          .format(p_value))

plt.figure(figsize=(16,8))
plt.plot(data['Annual Volatility'])
plt.title('WFC Annual Volatility')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend(['Volatility'])
plt.show()

split = int(len(data)*0.87)
train_set, test_set = data[:split], data[split:]

from arch import arch_model

aic=[]

p = range(1,6)
q = range(1,6)

dist = ['Normal', 't', 'skewt']

p_q_dist = []

for i in p:
    for j in q:
        for k in dist:
            garch = arch_model(train_set['Daily Returns'],
                               vol='Garch', p=i, q=j, dist=k)
            garch_fit = garch.fit(disp='off')
            
            aic_temp = garch_fit.aic
            keys_temp = (i, j, k)
            p_q_dist.append(keys_temp)
            aic.append(aic_temp)

aic_dict = {'p_q_dist': p_q_dist, 'aic':aic}

df = pd.DataFrame(aic_dict)

print(df[df['aic'] == df['aic'].min()])

garch = arch_model(train_set['Daily Returns'], vol='Garch',
                   p=1, q=1, dist='t')

garch_fit = garch.fit(disp='off')

garch_resid = garch_fit.resid
garch_sd = garch_fit.conditional_volatility

garch_sd_resid = garch_resid/garch_sd

plt.figure(figsize=(16,8))
plt.plot(garch_sd_resid)
plt.title('GARCH Standardized Residuals')
plt.xlabel('Date')
plt.ylabel('Standardized Residuals')
plt.legend(['Standardized Residuals'])
plt.show()

plt.figure(figsize=(14,6))
sns.distplot(garch_sd_resid, hist=False, kde=True)
plt.show()

past = train_set['Daily Returns'].tolist()

predictions=[]

for i in range(len(test_set)):
    garch = arch_model(past, vol='Garch',
                       p=1, q=1, dist='t')
    garch_fit = garch.fit(disp='off')
    temp_forecasts = garch_fit.forecast(horizon=1).variance

    temp_pred = temp_forecasts.iloc[-1].values[0]

    predictions.append((temp_pred**0.5) * (252**0.5) )

    past.append(test_set['Daily Returns'].iloc[i])

for i in range(0,10):
    print('Predicted = {}, Actual = {}'
          .format(predictions[i],test_set['Annual Volatility'].iloc[i]))

residual = []

for i in range(len(test_set)):
    residual.append(predictions[i]-test_set['Annual Volatility'].iloc[i])

plt.figure(figsize=(16,8))
sns.distplot(residual, hist=False, kde=True)
plt.show()

from sklearn.metrics import mean_squared_error as mse

error_mse = mse(test_set['Annual Volatility'], predictions)
print('MSE: {}'.format(error_mse))

plt.figure(figsize=(16,8))
plt.plot(test_set['Annual Volatility'])
plt.plot(test_set.index, predictions, color='red')
plt.title('WFC Volatility')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend(['test_set', 'predictions'])
plt.show()


