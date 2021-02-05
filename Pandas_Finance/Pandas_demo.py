# import pandas_datareader as pdr
# import datetime
# appl = pdr.get_data_yahoo('AAPL',
#                           start=datetime.datetime(2009,10,1),
#                           end=datetime.datetime(2019,1,1))
# print(appl)

import quandl
appl = quandl.get('WIKI/AAPL',start_date='2009-10-01',end_date='2019-1-1')

import pandas as pd
appl.to_csv('data/apple_ohlc.csv')
df = pd.read_csv('data/apple_ohlc.csv',header=0,index_col='Date',parse_dates=True)
ts = df['Close'][-10:]
print(ts)
print(type(ts))