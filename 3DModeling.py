import numpy as np

strikeprice = np.linspace(50,150, 25)
time = np.linspace(0.5,2,25)

strikeprice, time=np.meshgrid(strikeprice, time)
strikeprice_time = np.meshgrid(strikeprice,time)


implied_volatility = (strikeprice-100)**2 / (100*strikeprice)/time

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize = (10,7))
axis = fig.add_subplot(111, projection = '3d')

surface = axis.plot_surface(strikeprice, time, implied_volatility,
                           rstride = 1, cstride =1,cmap = plt.cm.coolwarm, linewidth=0.5, antialiased=False )

axis.set_xlabel('strike')
axis.set_ylabel('time-to-maturity')
axis.set_zlabel('implied volatility')

fig.colorbar(surface, shrink=0.5, aspect=5)
plt.show()
