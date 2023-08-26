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

p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha = 0.3
#darkness of grid lines transparent 0 opaque 1

p.segment(df.index, df.High, df.index, df.Low, color="red")
#draws a vertical line segment from the high to low value, at the particular index

p.vbar(df.index[inc], w, df.Open[inc], df.Close[inc], fill_color='#1ED837', line_color='black')
#for increases, creates green vertical bars between open and close, w is the width,
#which should correspond to the length of each datapoint on the axis, which are in milliseconds

p.vbar(df.index[dec], w, df.Open[dec], df.Close[dec], fill_color='#F2583E', line_color='black')
#for decreases, creates red vertical bars

output_file('candlestick.html', title='candlesticks.py')
#shows graph in browser

show(p)

