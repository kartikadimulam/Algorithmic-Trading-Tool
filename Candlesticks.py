import pandas as pd

path = '/Users/kartikadi/downloads/PythonForTrading/candlestick_data.csv'
df = pd.read_csv(path, index_col=0)

import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file
#various functions imported from bokeh, for interactive data visualization


df.index = pd.to_datetime(df.index)
w = 12*60*60*1000
#half day in milliseconds

inc = df.Close > df.Open
dec = df.Open > df.Close

TOOLS = 'pan, wheel_zoom, box_zoom, reset, save'
#arguments for figure() to get tools from bokeh

p = figure(x_axis_type= "datetime", tools = TOOLS,
           plot_width = 1000, title='SPY Candlestick')


from math import pi

