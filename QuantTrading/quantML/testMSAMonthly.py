from setup import *
from features import *
from fetchData import getRawData
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas import pandas
from matplotlib.finance import candlestick2_ohlc 
from matplotlib.finance import candlestick2_ochl 
from matplotlib.finance import candlestick_ohlc

from matplotlib import pyplot as plt 
from matplotlib import dates as mdates 
import matplotlib.ticker as ticker 
from matplotlib.dates import DayLocator


#from mpl_finance import 

import numpy as np
    
def printSampleDataFrameMonthly(tickerSymbol):
    start_date="2008-11-01"
    end_date="2017-10-01"

    options={'qtype':'adjclose',
             'tables':['intStocksMonthly']}

    tickerDataRaw=getRawDataMonthly(tickerSymbol,start_date,end_date,options)
    print(tickerDataRaw.head(1))

    closingPrices = tickerDataRaw['AdjClose']
    
    monthlyAvgs = closingPrices.rolling(window=36).mean()
    
    validMonthlyAvgs = monthlyAvgs.dropna()
    print("---- 36 Month Average Prices ------ ")
    print("Total Elements = " + str(validMonthlyAvgs.size))
    print("validMonthlyAvgs[20] = " + str(validMonthlyAvgs[20]))
    print("validMonthlyAvgs Type = " + str(type(validMonthlyAvgs)))

    vlist = validMonthlyAvgs.tolist()
    print("vlist size = " + str(len(vlist)))
   
    dateL, openPL, highPL, lowPL, closePL = [], [], [], [], []
    ohlc = []
    data_dates = []
    for date, val in validMonthlyAvgs.iteritems():
        data = tickerDataRaw.loc[(tickerDataRaw['Timestamp'] == date)]
        openVal = data.loc[date,"Open"]
        highVal = data.loc[date,"High"]
        lowVal = data.loc[date,"Low"]
        closeVal = data.loc[date,"Close"]
        
        openP = (openVal/val) - 1
        highP = (highVal/val) - 1
        lowP = (lowVal/val) - 1
        closeP = (closeVal/val) - 1
        
        openPL.append(openP)
        highPL.append(highP)
        lowPL.append(lowP)
        closePL.append(closeP)
        
        new_Date = mdates.datestr2num(str(date))
        data_dates.append(new_Date)
        
        #print("Date = " + str(date) + " date type = " + str(type(date)) + " openVal = " + str(openVal) + " 36 MOnth Avg. = " + str(val) + " open Percent of avg = " + str(openP))
        print("[Date, 36 Month Average, Open, High, Low, Close] = [" + str(date) +  ", " + str(val) +  ", " + str(openP) + ", " + str(highP) + ", " + str(lowP) + ", " + str(closeP) + "]")
    #print("Open Percentage List = " + str(openPL))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    candlestick2_ohlc(ax, openPL, highPL, lowPL, closePL, width=0.4, colorup='green', colordown='red', alpha=0.75)
    
    ax.grid(True)
    #ax.xaxis.set_major_locator(ticker.MaxNLocator(25))
    
    fig.autofmt_xdate()
    fig.tight_layout()

    plt.xlabel('Date')
    plt.ylabel('monthly ranges vs. 36 months average')
    
    plt.show()
    
    
tickerSymbol ="SLV"
printSampleDataFrameMonthly(tickerSymbol)
print("done")