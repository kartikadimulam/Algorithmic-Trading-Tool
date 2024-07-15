import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file
from math import pi

df = yf.download("TSLA", start='2022-02-03', end='2024-07-03')
df.index = pd.to_datetime(df.index)


w = 12*60*60*1000

inc = df.Close > df.Open
dec = df.Open > df.Close

TOOLS = 'pan, wheel_zoom, box_zoom, reset, save'

p = figure(x_axis_type= "datetime", tools = TOOLS,
           width = 1000, title='TSLA Candlestick')

p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha = 0.3

p.segment(df.index, df.High, df.index, df.Low, color="red")

p.vbar(df.index[inc], w, df.Open[inc], df.Close[inc], fill_color='#1ED837', line_color='black')

p.vbar(df.index[dec], w, df.Open[dec], df.Close[dec], fill_color='#F2583E', line_color='black')

output_file('candlestick.html', title='candlesticks.py')

show(p)

