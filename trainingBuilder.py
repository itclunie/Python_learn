#http://pmorissette.github.io/ffn/quick.html

import ffn

# data = ffn.get('agg,hyg,spy,eem,efa', start='2010-01-01', end='2014-01-01')
# print(data.head())

# data = ffn.get('aapl:Open,aapl:High,aapl:Low,aapl:Close', start='2010-01-01', end='2014-01-01').head()
# print(data.head())

data = ffn.get('agg,hyg,spy,eem,efa', start='2010-01-01', end='2014-01-01')
perf = data.calc_stats()
print(perf.display())