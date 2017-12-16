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

def printTickerDataFrame(df):
    print("Date" + "\t" * 4 + "Price" + "\t" * 4 + "Return\n")
    print("=" * 100)
    mydf = df[['Price', "Return"]]
    for row in mydf.itertuples():
#        index,price,month,day,dayofweek,tdaysleftinmonth,tdayinmonth,tdayinweek,returns = row
        index,price,returns = row
        print(index.strftime('%Y-%m-%d') + "\t" * 3 + str(price) + "\t" * 3 + str(returns))


dateList = []

def mydate(x, pos):
    try:
        return dateList[int(x)]
    except IndexError:
        return ''
    
def printSampleDataFrameMonthly(tickerSymbol):
    start_date="2008-11-01"
    end_date="2017-10-01"

    options={'qtype':'adjclose',
             'tables':['intStocksMonthly']}

    tickerDataRaw=getRawDataMonthly(tickerSymbol,start_date,end_date,options)
    print(tickerDataRaw.head(1))
    #print("\n Size => " + tickerDataRaw.size)

    #print("Columns => " + tickerDataRaw.columns.values)
    '''
    for idx, row in tickerDataRaw.iteritems():
        #d = row['Timestamp']
        #print("d => " + d)
        #nd = (datetime.date(d) + datetime.timedelta(1*365/12)).isoformat()
        #print("Current Date => " + d + " New Date => " + nd)
        print(idx)
    '''
    for row in tickerDataRaw.iterrows():
        d = row[0] #timestamp
        print("First Element => " + str(d))
        #print("D is of type " + str(type(d)))
        #nd = (datetime.strptime(d) + datetime.timedelta(1*365/12)).isoformat()
        #nd = datetime.strptime(d, '%y-%m-%d')
        #dt = datetime.strptime(d, '%y-%m-%d')
        dt = d
        nd = (dt + relativedelta(months=-36)).isoformat()
        print("dt => " + str(dt) + " nd => " + str(nd))
        
    closingPrices = tickerDataRaw['AdjClose']
    '''
    print("---- Closing Prices ------ ")
    print(closingPrices.head(1000))
    print("Total Elements = " + str(closingPrices.size))
    '''
    
    monthlyAvgs = closingPrices.rolling(window=36).mean()
    '''
    print("---- 36 Month Average Prices ------ ")
    print(monthlyAvgs.head(1000))
    print("Total Elements = " + str(monthlyAvgs.size))
    print("monthlyAvgs[90] = " + str(monthlyAvgs[90]))
    '''
    
    validMonthlyAvgs = monthlyAvgs.dropna()
    print("---- 36 Month Average Prices ------ ")
    #print(validMonthlyAvgs.head(1000))
    print("Total Elements = " + str(validMonthlyAvgs.size))
    print("validMonthlyAvgs[20] = " + str(validMonthlyAvgs[20]))
    print("validMonthlyAvgs Type = " + str(type(validMonthlyAvgs)))

    vlist = validMonthlyAvgs.tolist()
    print("vlist size = " + str(len(vlist)))
    '''
    for x in vlist:
        print("x = " + str(x))
    ''' 
   
    dateL, openPL, highPL, lowPL, closePL = [], [], [], [], []
    ohlc = []
    data_dates = []
    for date, val in validMonthlyAvgs.iteritems():
    #    print("Index=" + str(ind) + " Value=" + val)
    #    print(" Value=" + val)
        #print(" date=" + str(date) + " Value=" + str(val))
        #print(tickerDataRaw.loc[(tickerDataRaw['Timestamp'] == date)])
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
        print("new_Date = " + str(new_Date) + " type = " + str(type(new_Date)))
        data_dates.append(new_Date)
        #data_dates.append(str(date))
        
        #dataR = new_Date, openP, highP, lowP, closeP
        #ohlc.append(dataR)
        print("Date = " + str(date) + " date type = " + str(type(date)) + " openVal = " + str(openVal) + " 36 MOnth Avg. = " + str(val) + " open Percent of avg = " + str(openP))
        print("[Open, High, Low, Close] = [" + str(openP) + ", " + str(highP) + ", " + str(lowP) + ", " + str(closeP) + "]")
    print("Open Percentage List = " + str(openPL))
    
    openPNA = np.array(openPL[0:], dtype=np.float64)
    highPNA = np.array(highPL[0:], dtype=np.float64)
    lowPNA = np.array(lowPL[0:], dtype=np.float64)
    closePNA = np.array(closePL[0:], dtype=np.float64)

    i = 0
    while i < len(data_dates):
        current_data = data_dates[i], openPNA[i], highPNA[i], lowPNA[i], closePNA[i]
        ohlc.append(current_data)
        i += 1
        
    '''
    x = np.arange(0, 5, 0.1);
    y = np.sin(x)
    plt.plot(x, y)
    '''

    #xdate = [datetime.datetime.fromtimestamp(i) for i in dateL]
    
    
    fig, ax = plt.subplots(figsize=(15, 7))
    
    #candlestick_ohlc(ax, ohlc, width=0.4, colorup='green', colordown='r', alpha='0.8')
    candlestick_ohlc(ax, ohlc, width=8, colorup='green', colordown='r', alpha=1)
    
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(MonthLocator())
    
    #fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()
    
    '''
    
    candlestick2_ohlc(ax, openPL, highPL, lowPL, closePL, width=0.4, colorup='green', colordown='red', alpha=0.75)
    #candlestick_ohlc(ax, ohlc, width=0.3, colorup='green', colordown='red')
    
    ax.grid(True)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(25))
    #xfmt = mdates.DateFormatter('%Y-%m-%d')
    #ax.xaxis.set_major_formatter(xfmt)
    #ax.xaxis.set_major_locator(mticker.AutoLocator())
    #ax.xaxis.set_major_locator(DayLocator())

    
    #ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    
    #fig.autofmt_xdate()
    fig.tight_layout()

    dayFormatter = mdates.DateFormatter('%Y-%b-%d')
    #ax.xaxis.set_major_formatter(dayFormatter)
    plt.xlabel('Date')
    plt.ylabel('monthly ranges vs. 36 months average')
    
    
    #plt.plot(data_dates, openPL)
    plt.show()
    '''
    
    
tickerSymbol ="GDXJ"
#ticker ="GLD"
#testData = printFeatureData(ticker)
#testData = printSampleDataFrameWeekly(ticker)
printSampleDataFrameMonthly(tickerSymbol)
print("done")