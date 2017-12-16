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

def printSampleDataFrameMonthly(tickerSymbol):
    start_date="2007-01-01"
    end_date="2017-11-01"

    options={'qtype':'adjclose',
             'tables':['intStocksMonthly']}

    tickerDataRaw = getRawDataMonthly(tickerSymbol,start_date,end_date,options)

    closingPrices = tickerDataRaw['AdjClose']
    _36MonthsAvgs = closingPrices.rolling(window=36).mean()
    print(str(_36MonthsAvgs))
    
    valid36MonthsAvgs = _36MonthsAvgs.dropna()
    print("---- 36 Month Average Prices ------ ")
    print("valid36MonthsAvgs Total Elements = " + str(valid36MonthsAvgs.size))
    print("valid36MonthsAvgs[0] = " + str(valid36MonthsAvgs[0]))
    print("valid36MonthsAvgs Type = " + str(type(valid36MonthsAvgs)))

    dateL, openVsMAList, highVsMAList, lowVsMAList, closeVsMAList = [], [], [], [], []
    ohlc = []
    data_dates = []
    j = 1
    for date, _36MonthsAvg in valid36MonthsAvgs.iteritems():
        
        if j == valid36MonthsAvgs.size:
            print("Final element # " + str(j) + " reached.  Stopping.")
            break
        
        #print("For " + str(date) + " 36 Months Average = " + str(_36MonthsAvg))

        #nd = (date + relativedelta(months=1)).isoformat()        
        nd = (date + relativedelta(months=1))
        print("type of nd = " + str(type(nd)))
        print("For " + str(nd) + " 36 Months Average = " + str(_36MonthsAvg))
        data = tickerDataRaw.loc[(tickerDataRaw['Timestamp'] == nd)]
        month_openVal = data.loc[nd,"Open"]
        month_highVal = data.loc[nd,"High"]
        month_lowVal = data.loc[nd,"Low"]
        month_closeVal = data.loc[nd,"AdjClose"]
        
        openVsMA = (month_openVal/_36MonthsAvg) - 1
        highVsMA = (month_highVal/_36MonthsAvg) - 1
        lowVsMA = (month_lowVal/_36MonthsAvg) - 1
        closeVsMA = (month_closeVal/_36MonthsAvg) - 1
        
        openVsMAList.append(openVsMA)
        highVsMAList.append(highVsMA)
        lowVsMAList.append(lowVsMA)
        closeVsMAList.append(closeVsMA)
        
        new_Date = mdates.datestr2num(str(nd))
        #print("new_Date = " + str(new_Date) + " type = " + str(type(new_Date)))
        data_dates.append(new_Date)
        
        print("[ " + str(nd) +  ", " + str(_36MonthsAvg) +  ", (" + 
                    str(month_openVal) + ", " + str(openVsMA) + "), (" + 
                    str(month_highVal) + ", " + str(highVsMA) + "), (" + 
                    str(month_lowVal) + ", " + str(lowVsMA) + "), (" + 
                    str(month_closeVal) + ", " + str(closeVsMA) + ") ]")
        j += 1
    
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
    
    candlestick_ohlc(ax, ohlc, width=12, colorup='green', colordown='r', alpha=1)
    
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(YearLocator())
    
    #fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()
    
    
tickerSymbol ="UUP"
printSampleDataFrameMonthly(tickerSymbol)
print("done")