"""purpose of script is to take csv with one ticker and data on that ticker over 5 years
and to split that data up by year and write each year to separate csvs for training"""

import csv, sys, pandas, os, math

stemPath = os.path.abspath('CSVs')

Yrs = ['2016-12','2015-12','2014-12','2013-12','2012-12','2011-12','2010-12','2009-12','2008-12','2007-12','TTM']

countR = 0

CSVs = os.listdir('CSVs')

for myCSV in CSVs:
    myCSVpath = stemPath + '\\' + myCSV

    opener = open(myCSVpath, 'r')
    reader = csv.reader(opener)
    headers = next(reader)

    df = pandas.read_csv(myCSVpath)
    
    for yr in Yrs:
        if yr in headers:
            yrLst = list(df[yr]) #essentially this will transpose 
            YrNoNaN = []

            for i in range(len(yrLst)): #remove NaN
                if type(yrLst[i]) == str:
                    YrNoNaN.append(yrLst[i])
                elif type(yrLst[i]) == float and math.isnan(yrLst[i]) == True:
                    YrNoNaN.append('')
                else:
                    YrNoNaN.append(yrLst[i])

            
            myYRpath = os.path.abspath('') + '\\' + yr + '.csv'

            with open(myYRpath, 'a') as f:
                writer = csv.writer(f, lineterminator = '\n')
                writer.writerows([YrNoNaN]) #for item in yrLst]

    countR += 1
    if countR % 50 == 0:
        print(countR, len(CSVs))