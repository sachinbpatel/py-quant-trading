import pandas as pd

applePrices = pd.read_csv("H:\python\QuantTrading\AAPL.csv", sep=',')

applePrices.head()

applePrices["Date"].dtype

def convert(string):
    from datetime import datetime
    return datetime.strptime(string, "%Y-%m-%d").date()

applePrices["Date"] = applePrices["Date"].apply(convert)

#change the index of the data frame
applePrices.index = applePrices["Date"]

#delete Date column from main Dataframe
del applePrices["Date"]
applePrices.head()

#compute the returns from a price series
priceSeries = applePrices["Adj Close"]
priceSeries.head()

priceSeries[1:].head()

priceSeries[:-1]/priceSeries[1:]-1


priceSeriesShifted = priceSeries[1:]
newIndex = priceSeries.index[0:-1]
print("newIndex = " + newIndex)
priceSeriesShifted.index = newIndex
priceSeriesShifted.head()

#compute a rolling average
#for each date, you want the average of prices from last 10 days
import numpy as np
pd.rolling_apply(priceSeries, 10, np.sum).head(10) 

priceSeries.sort_index(ascending=True, inplace=True)
priceSeries.head()

priceSeriesRollingSum = pd.rolling_apply(priceSeries, 10, np.sum)
priceSeriesRollingSum.sort_index(ascending=False, inplace=True)
priceSeriesRollingSum.head()

https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1432008000&period2=1495166400&interval=1d&events=history&crumb=GkeYkBGXWvM
https://query1.finance.yahoo.com/v7/finance/download/PCLN?period1=1432008000&period2=1495166400&interval=1d&events=history&crumb=GkeYkBGXWvM
https://query1.finance.yahoo.com/v7/finance/download/SHLD?period1=1432008000&period2=1495166400&interval=1d&events=history&crumb=GkeYkBGXWvM
https://query1.finance.yahoo.com/v7/finance/download/KSS?period1=1432008000&period2=1495166400&interval=1d&events=history&crumb=GkeYkBGXWvM
