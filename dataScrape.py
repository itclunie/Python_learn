import ffn
import json
import datetime
from datetime import date
import time
import pandas as pd
import math

def deDup(inLst):
    """deDup list in order"""
    seen = set()
    result = []
    for item in inLst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


with open('relatedCompanies.json') as tickers:
    dict_tickers = json.load(tickers)
    
myLst = list(dict_tickers['relcos'])

relcos = deDup(myLst) #remove duplicates and long names
relcosClnd = []
[relcosClnd.append(item) for item in relcos if len(item) <= 5] 

startDate='2016-11-11'
endDate='2017-11-11'
#startDate='2015-11-11'
#endDate='2016-11-11'
#startDate='2014-11-11'
#endDate='2015-11-11'
#startDate='2013-11-11'
#endDate='2014-11-11'\ac

rowsLst = []
count = 0

fails = []
for ticker in relcosClnd:
    try:
        data = ffn.get(ticker, start=startDate, end=endDate)
        perf = data.calc_stats()
        statsObj = perf.stats[ticker.lower()]
        myDict = dict(statsObj)
        myDict.update({'ticker':ticker})

        rowsLst.append(myDict)
        print(ticker, count)
        count += 1
    except:
        print(ticker, count, 'Failed')
        count += 1
        fails.append([ticker, startDate, endDate])
        pass
		

df = pd.DataFrame(rowsLst)
df.to_csv(startDate + '__' + endDate + '.csv')


# for item in rowsLst: #normalize each row out of 1 
    # normalize = []
    # fieldzSelected = []
    # ticker = item['ticker']

    # for header in item:
        # if header not in ['start', 'end', 'ticker'] and math.isnan(item[header]) == False:
            # fieldzSelected.append(header)
            # normalize.append(abs(item[header]))

    # normalize = [i/sum(normalize) for i in normalize]

    # for i in range(len(normalize)):
        # item[fieldzSelected[i]] = normalize[i]
        # #print(normalize[i],fieldzSelected[i])
    

# df.to_csv(startDate + '__' + endDate + '_Normd.csv')


df.T