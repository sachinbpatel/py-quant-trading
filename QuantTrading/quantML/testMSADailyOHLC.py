from setup import *
from features import *
from fetchData import getRawData
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from pandas import pandas
from matplotlib.finance import candlestick2_ohlc 
from matplotlib.finance import candlestick2_ochl 
from matplotlib.finance import candlestick_ohlc

from matplotlib import pyplot as plt 
from matplotlib import dates as mdates 
import matplotlib.ticker as ticker 
from matplotlib.dates import DayLocator
from matplotlib.dates import MonthLocator
from matplotlib.dates import YearLocator



import numpy as np

def printSampleDataFrameDaily(tickerSymbol):
    start_date="2017-01-01"
    end_date="2017-10-01"

    options={'qtype':'adjclose',
             'tables':['intStocks']}

    tickerDataRaw = getRawDataDaily(tickerSymbol,start_date,end_date,options)

    closingPrices = tickerDataRaw['AdjClose']
    _3MonthsAvgs = closingPrices.rolling(window=60).mean()
    #_3MonthsAvgs = closingPrices.rolling(window=10).mean()
    print(str(_3MonthsAvgs))
    
    valid3MonthsAvgs = _3MonthsAvgs.dropna()
    print("---- 3 Month Average Prices ------ ")
    print("valid3MonthsAvgs Total Elements = " + str(valid3MonthsAvgs.size))
    print("valid3MonthsAvgs[0] = " + str(valid3MonthsAvgs[0]))
    print("valid3MonthsAvgs Type = " + str(type(valid3MonthsAvgs)))

    dateL, openVsMAList, highVsMAList, lowVsMAList, closeVsMAList = [], [], [], [], []
    ohlc = []
    data_dates = []
    j = 1
    prev_3MonthAvg = 0.0
    for date, _3MonthsAvg in valid3MonthsAvgs.iteritems():
        
        if j == valid3MonthsAvgs.size:
            print("Final element # " + str(j) + " reached.  Stopping.")
            break
        
        if prev_3MonthAvg == 0.0:
            print("First element # " + str(j) + " Skip and Continue.")
            prev_3MonthAvg = _3MonthsAvg
            continue
        
        
        #print("For " + str(date) + " 3 Months Average = " + str(_3MonthsAvg))

        #nd = (date + relativedelta(months=1)).isoformat()        
        #nd = (date + relativedelta(days=1))
        
        #print("type of nd = " + str(type(nd)))
        print("For " + str(date) + " 3 Months Average = " + str(prev_3MonthAvg))
        data = tickerDataRaw.loc[(tickerDataRaw['Timestamp'] == date)]
        month_openVal = data.loc[date,"Open"]
        month_highVal = data.loc[date,"High"]
        month_lowVal = data.loc[date,"Low"]
        month_closeVal = data.loc[date,"AdjClose"]
        
        openVsMA = (month_openVal/prev_3MonthAvg) - 1
        highVsMA = (month_highVal/prev_3MonthAvg) - 1
        lowVsMA = (month_lowVal/prev_3MonthAvg) - 1
        closeVsMA = (month_closeVal/prev_3MonthAvg) - 1
        
        openVsMAList.append(openVsMA)
        highVsMAList.append(highVsMA)
        lowVsMAList.append(lowVsMA)
        closeVsMAList.append(closeVsMA)
        
        #new_Date = mdates.datestr2num(str(nd))
        new_Date = mdates.datestr2num(str(date))
        #print("new_Date = " + str(new_Date) + " type = " + str(type(new_Date)))
        data_dates.append(new_Date)
        
        print("[ " + str(date) +  ", " + str(prev_3MonthAvg) +  ", (" + 
                    str(month_openVal) + ", " + str(openVsMA) + "), (" + 
                    str(month_highVal) + ", " + str(highVsMA) + "), (" + 
                    str(month_lowVal) + ", " + str(lowVsMA) + "), (" + 
                    str(month_closeVal) + ", " + str(closeVsMA) + ") ]")
        j += 1
        prev_3MonthAvg = _3MonthsAvg
    
    openVsMA_NA = np.array(openVsMAList[0:], dtype=np.float64)
    highVsMA_NA = np.array(highVsMAList[0:], dtype=np.float64)
    lowVsMA_NA = np.array(lowVsMAList[0:], dtype=np.float64)
    closeVsMA_NA = np.array(closeVsMAList[0:], dtype=np.float64)

    i = 0
    while i < len(data_dates):
        current_data = data_dates[i], openVsMA_NA[i], highVsMA_NA[i], lowVsMA_NA[i], closeVsMA_NA[i]
        ohlc.append(current_data)
        i += 1
        
    fig, ax = plt.subplots(figsize=(15, 7))
    
    candlestick_ohlc(ax, ohlc, width=0.5, colorup='green', colordown='r', alpha=1)
    
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(MonthLocator())
    
    #fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()
    
    
tickerSymbol ="GLD"
printSampleDataFrameDaily(tickerSymbol)
print("done")