#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import re, json, datetime
import MySQLdb
import pandas as pd
import json
from datetime import datetime, timedelta
import requests

def get_buckets(start_date, end_date):
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    bucket_limits = [start_date_dt]
    left_limit = start_date_dt
    while left_limit <= end_date_dt:
        new_limit = left_limit + timedelta(days=181)
        if new_limit < end_date_dt:
            bucket_limits.append(new_limit)
        left_limit = new_limit
    bucket_limits.append(end_date_dt)
    return bucket_limits

def get_data(bucket_start_date,bucket_end_date, keyword):
    bucket_start_date_printed = datetime.strftime(bucket_start_date, '%Y-%m-%d')
    bucket_end_date_printed = datetime.strftime(bucket_end_date, '%Y-%m-%d')
    time_formatted = bucket_start_date_printed + '+' + bucket_end_date_printed

    req = {"comparisonItem":[{"keyword":keyword, "geo":geo, "time": time_formatted}], "category":category,"property":""}
    hl = "en-GB"
    tz = "-120"

    explore_URL = 'https://trends.google.com/trends/api/explore?hl={0}&tz={1}&req={2}'.format(hl,tz,json.dumps(req).replace(' ','').replace('+',' '))
    return requests.get(explore_URL).text

def get_token(response_text):
    try:
        return response_text.split('token":"')[1].split('","')[0]
    except:
        return None

def get_csv_request(response_text):
    try:
        return response_text.split('"widgets":')[1].split(',"lineAnno')[0].split('"request":')[1]       
    except:
        return None

def get_csv(response_text):
    request = get_csv_request(response_text)
    token = get_token(response_text)

    csv = requests.get('https://www.google.com/trends/api/widgetdata/multiline/csv?req={0}&token={1}&tz=-120'.format(request,token))
    return csv.text.encode('utf8')

def parse_csv(csv_contents):
    lines = csv_contents.split('\n')
    df = pd.DataFrame(columns = ['date','value'])
    dates = []
    values = []
    # Delete top 3 lines
    for line in lines[3:-1]:
        try:
            dates.append(line.split(',')[0].replace(' ',''))
            values.append(line.split(',')[1].replace(' ',''))
        except:
            pass
    df['date'] = dates
    df['value'] = values
    return df   

def get_daily_frames(start_date, end_date, keyword):

    bucket_list = get_buckets(start_date, end_date)
    frames = []
    for i in range(0,len(bucket_list) - 1):
        resp_text = get_data(bucket_list[i], bucket_list[i+1], keyword)
        frames.append(parse_csv(get_csv(resp_text)))
    return frames




wikiStem = 'https://en.wikipedia.org/wiki/'
wikiAPI = 'https://en.wikipedia.org/w/api.php?action=query&indexpageids=true&format=json&prop=pageviews&pvipdays=60&titles='
coTitles = []
coLinks = []
coTickLinks = []
coTickers = []
pageViews = []
pageViewsID = {}
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
response = requests.get(url)

db = MySQLdb.connect(host= "localhost", user="root", passwd="andy1999", db="SP500")
cursor = db.cursor()


for m in re.finditer('<td><a rel="nofollow(.*?)<\/tr>', response.text, re.MULTILINE|re.IGNORECASE|re.DOTALL):
    tickerInfo = re.search('href="(.*?)<\/a>', m.group(1), re.IGNORECASE|re.DOTALL)
    ticker = tickerInfo.group(1).split('">')
        
    coTickLinks.append(ticker[0])
    coTickers.append(ticker[1])
    
    
    coLink = re.search('\/wiki\/(.*?)<\/a>', m.group(1), re.MULTILINE|re.IGNORECASE|re.DOTALL)
    coTitle = re.search('title="(.*?)"', coLink.group(1), re.IGNORECASE|re.DOTALL)
    
    coTitle2 = coTitle.group(1).replace(' ','%20')
    coTitles.append(coTitle2)
    
    coLink = coLink.group(1).split('"')
    coLink = wikiStem + coLink[0]
    coLinks.append(coLink)
    

countR = 0
for title in coTitles:
    response = requests.get(wikiAPI + title)
    json_string = response.text

    pageViews = json.loads(json_string)
    
    pageid = pageViews['query']['pageids']
    pageTitle = pageViews['query']['pages'][pageid[0]]['title']
    pageViewObj = pageViews['query']['pages'][pageid[0]]['pageviews']
    
    tmpList = []
    
    for key in pageViewObj:
        tmpList.append([key, pageViewObj[key]])

    tmpList.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'))
    
    
    sqlTail = ", null, null)"
    
    
    
    pageTitle = pageTitle.replace("'","")
    pageTitle = pageTitle.replace(",","")
    pageTitlePlus = pageTitle.replace(" ","+")
    
    endInx = len(tmpList) - 1
    start_date = tmpList[0][0]
    end_date = tmpList[endInx][0]
    
    geo = ''
    category = 22

    
    daily_frames = get_daily_frames(start_date, end_date, pageTitlePlus)
    np_df = daily_frames[0].as_matrix()

#    print pageTitlePlus, [len(tmpList), len(np_df)]

    print pageTitlePlus, np_df
    
#    for i in range(len(tmpList)):
#        if tmpList[i][1] == None:
#            views = '0'
#        else:
#            views = str(tmpList[i][1])
#            
#        pageTitle = pageTitle.replace("'","")
#            
#        date = str(tmpList[i][0])
#        sql = "insert into views VALUES(null, '" + date + "', '" +  pageTitle + "', " + views + sqlTail
#        
#        print sql
##        cursor.execute(sql)
#
#
#        countR = countR + 1
#        if countR > 2: #for testing
#            break
          
         

db.commit()
db.close()