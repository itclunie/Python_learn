import pandas as pd
import ffn
import sys
import datetime
from datetime import date
import time

df = pd.read_csv('SP400.csv', encoding = "ISO-8859-1")

#def countDays(start,end):
#    start = start.split('-')
#    end = end.split('-')
#    d0 = date(int(start[0]), int(start[1]), int(start[2]))
#    d1 = date(int(end[0]), int(end[1]), int(end[2]))
#    delta =  d1 - d0
#    return delta.days

def makeYrBrackets(yrs2goBack):
    Year = 365
    startDateNow = datetime.datetime.now() + datetime.timedelta(-Year)
    startDateNow = startDateNow.strftime("%Y-%m-%d")
    endDateNow = datetime.datetime.now()
    endDateNow = endDateNow.strftime("%Y-%m-%d")
    yrBrackets = [[startDateNow,endDateNow]]
    
    for i in range(yrs2goBack):
        endDateTrain = datetime.datetime.now() + datetime.timedelta(-Year)
        endDateTrain = endDateTrain.strftime("%Y-%m-%d")
        Year = Year + 365
        startDateTrain = datetime.datetime.now() + datetime.timedelta(-Year)
        startDateTrain = startDateTrain.strftime("%Y-%m-%d")
        yrBrackets.append([endDateTrain,startDateTrain])
        #print(startDateTrain, endDateTrain, countDays(startDateTrain, endDateTrain))
    return yrBrackets
 

print(makeYrBrackets(2))


topLst = []
rowsLst = []
cnt = 0
for yrs in makeYrBrackets(2):
    time.sleep(3)

    for ticker in df['ticker']:
        data = ffn.get(ticker, start=yrs[0], end=yrs[1])

        perf = data.calc_stats()
        statsObj = perf.stats[ticker.lower()]

        myDict = dict(statsObj)
        myDict.update({'ticker':ticker})

        rowsLst.append(myDict)

            
    topLst.append(rowsLst)


print(topLst)


df = pd.DataFrame(rows_list)

normMe = [.89, .9, .4]
normMe = [i/sum(normMe) for i in normMe]

#for index, row in df.iterrows():
#    print(index, row)
#    break

df
    
#dfHeaders = list(df)
#for col in dfHeaders:
#    if df[col].name not in ['ticker', 'start', 'end']:
#        print(df[col].name)
        
