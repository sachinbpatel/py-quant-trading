import plotly.plotly as py
import plotly.graph_objs as go

import pandas_datareader.data as web
from datetime import datetime
from fetchData import getRawData

#df = web.DataReader("^vix", 'yahoo', datetime(2007, 10, 1), datetime(2009, 4, 1))

ticker, start_date, end_date = "VIX", datetime(2007, 10, 1), datetime(2009, 4, 1)
df = getRawData(ticker, start_date, end_date)
print(df.head())

trace = go.Candlestick(x=df.index,
                       open=df.Open,
                       high=df.High,
                       low=df.Low,
                       close=df.AdjClose)
data = [trace]
py.iplot(data, filename='simple_candlestick')