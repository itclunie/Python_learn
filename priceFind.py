statsURL = "http://performance.morningstar.com/stock/performance-return.action?t=VLKAY&region=usa&culture=en-US"

html = requests.get(statsURL)

bs = BeautifulSoup(html)
table = bs.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="Table1") 
rows = table.findAll(lambda tag: tag.name=='tr')