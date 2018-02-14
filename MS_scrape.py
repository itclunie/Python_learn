import requests, pandas, csv, sys, json
from io import StringIO



import datetime as dt
from pandas_datareader import data, wb

start_date = dt.datetime(1980, 1, 1)
dat = data.DataReader('googl', 'yahoo', start_date, dt.datetime.today())
dat.to_csv('googl.csv', mode='w', header=True)



sys.exit()


with open('relatedCompanies.json') as tickers:
    dict_tickers = json.load(tickers)
tckrs = list(dict_tickers['relcos'])

xchngs = ["xnys", "xnas", "pinx"]
errors = []

countR = 0
for tckr in tckrs:
    if len(tckr) <= 5:
        try:
            for x in xchngs: #find out which exchange ticker belongs to
                statsURL = "http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?&callback=?&t=" + x + ":" + tckr + "&region=usa&culture=en-US&ops=clear&cur=&order=asc"
                rs = requests.get(statsURL)
                
                if len(rs.text) > 0:
                    break
          
            reader = csv.reader(StringIO(rs.text), delimiter=',') #into csv format

            myLst = list(reader)
            my_Lst = []

            headers = [] #grab header
            for item in myLst:
                if item[0] == '':
                    headers = item
                    break        

            for i in range(len(myLst)): #remove labeling/noninformative lines
                if len(myLst[i]) > 1 and myLst[i][0] not in ['Margins % of Sales','Profitability','Cash Flow Ratios','Balance Sheet Items (in %)','Liquidity/Financial Health','Efficiency'] :
                    my_Lst.append(myLst[i])
                    
            tckrLst = ['Ticker']
            for i in range(len(my_Lst[0]) - 1):
                tckrLst.append(tckr)
            
            my_Lst.append(tckrLst)
            df = pandas.DataFrame(my_Lst[1:], columns=headers) #make df from my_Lst
            df.set_index('', inplace=True)
            
            df.to_csv(tckr + '_allYrs.csv')
            
            countR += 1
            if countR % 20 == 0:
                print(countR)
            
        except:
            countR += 1
            errors.append(tckr)
            pass
        
print(errors)
        
