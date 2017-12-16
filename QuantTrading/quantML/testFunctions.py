from setup import *
from features import *
from fetchData import getRawData
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas import pandas
from matplotlib.finance import candlestick 

def printTickerDataFrame(df):
    print("Date" + "\t" * 4 + "Price" + "\t" * 4 + "Return\n")
    print("=" * 100)
    mydf = df[['Price', "Return"]]
    for row in mydf.itertuples():
#        index,price,month,day,dayofweek,tdaysleftinmonth,tdayinmonth,tdayinweek,returns = row
        index,price,returns = row
        print(index.strftime('%Y-%m-%d') + "\t" * 3 + str(price) + "\t" * 3 + str(returns))


def printSampleDataFrame(ticker):
    start_date="2009-01-01"
    end_date="2009-01-03"

    options={'qtype':'adjclose',
             'tables':['intStocks','itradingDays']}

    tickerDataRaw=getRawData(ticker,start_date,end_date,options)
    print(tickerDataRaw.head())
    #print("\n Size => " + tickerDataRaw.size)

    for idx, row in tickerDataRaw.iteritems():
        print(idx)

#testData = getFeatures(ticker, testPeriod[0], testPeriod[1], options, supportTickers)[0]

def printSampleDataFrameWeekly(ticker):
    start_date="2008-01-01"
    end_date="2009-01-03"

    options={'qtype':'adjclose',
             'tables':['intStocksWeekly']}

    tickerDataRaw=getRawDataWeekly(ticker,start_date,end_date,options)
    print(tickerDataRaw.head(100))
    #print("\n Size => " + tickerDataRaw.size)

    for idx, row in tickerDataRaw.iteritems():
        print(idx)


def printSampleDataFrameMonthly(ticker):
    start_date="2008-11-01"
    end_date="2017-10-01"

    options={'qtype':'adjclose',
             'tables':['intStocksMonthly']}

    tickerDataRaw=getRawDataMonthly(ticker,start_date,end_date,options)
    print(tickerDataRaw.head(1))
    #print("\n Size => " + tickerDataRaw.size)

    print("Columns => " + tickerDataRaw.columns.values)
    for idx, row in tickerDataRaw.iteritems():
        #d = row['Timestamp']
        #print("d => " + d)
        #nd = (datetime.date(d) + datetime.timedelta(1*365/12)).isoformat()
        #print("Current Date => " + d + " New Date => " + nd)
        print(idx)

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
    print("---- Closing Prices ------ ")
    print(closingPrices.head(1000))
    print("Total Elements = " + str(closingPrices.size))

    monthlyAvgs = closingPrices.rolling(window=36).mean()
    print("---- 36 Month Average Prices ------ ")
    print(monthlyAvgs.head(1000))
    print("Total Elements = " + str(monthlyAvgs.size))
    print("monthlyAvgs[90] = " + str(monthlyAvgs[90]))

    validMonthlyAvgs = monthlyAvgs.dropna()
    print("---- 36 Month Average Prices ------ ")
    print(validMonthlyAvgs.head(1000))
    print("Total Elements = " + str(validMonthlyAvgs.size))
    print("validMonthlyAvgs[20] = " + str(validMonthlyAvgs[20]))
    print("validMonthlyAvgs Type = " + str(type(validMonthlyAvgs)))

    vlist = validMonthlyAvgs.tolist()
    print("vlist size = " + str(len(vlist)))
    for x in vlist:
        print("x = " + str(x))
        
    for date, val in validMonthlyAvgs.iteritems():
    #    print("Index=" + str(ind) + " Value=" + val)
    #    print(" Value=" + val)
        #print(" date=" + str(date) + " Value=" + str(val))
        print(tickerDataRaw.loc[(tickerDataRaw['Timestamp'] == date)])
        data = tickerDataRaw.loc[(tickerDataRaw['Timestamp'] == date)]
        openVal = data.loc[date,"Open"]
        highVal = data.loc[date,"High"]
        lowVal = data.loc[date,"Low"]
        closeVal = data.loc[date,"Close"]
        openP = (openVal/val) - 1
        highP = (highVal/val) - 1
        lowP = (lowVal/val) - 1
        closeP = (closeVal/val) - 1
        
        print("Date = " + str(date) + " openVal = " + str(openVal) + " 36 MOnth Avg. = " + str(val) + " open Percent of avg = " + str(openP))
        print("[Open, High, Low, Close] = [" + str(openP) + ", " + str(highP) + ", " + str(lowP) + ", " + str(closeP) + "]")

    #for item in validMonthlyAvgs:
        #d = row[0] #timestamp
     #   d = "1"
      #  avg = item
       # print("day = " + d + " avg = " + avg)


def printFeatureData(ticker):
    options = {'qtype':'adjclose',
               'tables':["intStocks","itradingDays"],
               'freq':0, # The frequency of trading, daily=0, monthly=1,weekly=2
               'offset':1, # The offset if the period > 1day, ie which trading day in the month/week the strategy will be executed
               'pure':0, # from here we have the features , the returns as is
               'cal':1, # Calendar features
               'history':0, # last 3 periods returns
               'momentum':1, # momentum features
               'jump':0, # jump features
               'value':0, # long term reversal features
               'prevWeeks':1,# Now by turning this to 1 we can run a model which includes previous weeks
               'algo':KNeighborsRegressor,
               'algo_params':{'n_neighbors':5}
               }

    supportTickers= None
    # [("BANKNIFTY",{'pure':0,'momentum':1,'jump':0,'prevWeeks':0})]

    trainStart="2006-06-01"
    #testPeriod=["2013-06-01","2016-04-01"]
    testPeriod=["2017-05-01", "2017-05-22",]
    start_date = "2017-05-01"
    end_date = "2017-05-22"

    algo = options['algo']
    algo_params = options['algo_params']

    buffer = 0
    tickerDataRaw = getRawData(ticker, start_date, end_date, options, buffer)
    tickerDataRaw["Return"] = getReturn(tickerDataRaw["Price"])
    print()
    printTickerDataFrame(tickerDataRaw)

    testData = getFeatures(ticker, testPeriod[0], testPeriod[1], options, supportTickers)[0]
    print(testData.head())

    pure = tickerDataRaw["Price"][1:]
    pureIndex = tickerDataRaw.index[0:-1]
    pure.index = pureIndex
    print("pure => " + str(pure.tolist()))
    print("pureIndex => " + str(pureIndex.tolist()))
    print(pure.head(2))
    print(pure.tail(2))
    print("testData count => " + str(len(testData.index)))
    print("Done")
    return testData


ticker ="GDXJ"
#ticker ="GLD"
#testData = printFeatureData(ticker)
#testData = printSampleDataFrameWeekly(ticker)
testData = printSampleDataFrameMonthly(ticker)
print("done")