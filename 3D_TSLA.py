import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ticker = 'TSLA'
tsla = yf.Ticker(ticker)

exp_dates = tsla.options

strike_prices = []
times_to_maturity = []
implied_vols = []

today = pd.Timestamp.today()

for exp_date in exp_dates:
    opt_chain = tsla.option_chain(exp_date)
    
    calls = opt_chain.calls
    
    ttm = (pd.to_datetime(exp_date) - today).days / 365.0
    
    strikes = calls['strike']
    ivs = calls['impliedVolatility']
    
    strike_prices.extend(strikes)
    times_to_maturity.extend([ttm] * len(strikes))
    implied_vols.extend(ivs)
    
strike_prices = np.array(strike_prices)
times_to_maturity = np.array(times_to_maturity)
implied_vols = np.array(implied_vols)


strikeprice_grid, time_grid = np.meshgrid(
    np.linspace(strike_prices.min(), strike_prices.max(), 25),
    np.linspace(times_to_maturity.min(), times_to_maturity.max(), 25)
)

from scipy.interpolate import griddata

implied_vol_grid = griddata(
    (strike_prices, times_to_maturity),
    implied_vols,
    (strikeprice_grid, time_grid),
    method='linear'
)

fig = plt.figure(figsize=(10, 7))
axis = fig.add_subplot(111, projection='3d')

surface = axis.plot_surface(
    strikeprice_grid, time_grid, implied_vol_grid,
    rstride=1, cstride=1, cmap=plt.cm.coolwarm, linewidth=0.5, antialiased=False
)

axis.set_xlabel('Strike Price')
axis.set_ylabel('Time to Maturity (Years)')
axis.set_zlabel('Implied Volatility')

fig.colorbar(surface, shrink=0.5, aspect=5)
plt.show()
