import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt


yf.pdr_override()

start = dt.datetime(2020,1,1)

end = dt.datetime.now()


#stock = input("ENTET THE STOCK (INDIAN STOCK only):")
#df = pdr.get_data_yahoo(stock+".NS")



class StockData():
	def __init__(self):
		yf.pdr_override()
		self.df = None
		start = dt.datetime(2020,1,1)
		end = dt.datetime.now()
		self.rsi = {}


	def RSI(df,days):
		if not self.rsi.has_key(days):
			UT=np.where(df['Adj Close'] > df['Adj Close'].shift(1), df['Adj Close']-df['Adj Close'].shift(1), 0)
			LT=np.where(df['Adj Close'] < df['Adj Close'].shift(1), df['Adj Close'].shift(1)-df['Adj Close'], 0)
			UTAvg14=df['UT'].ewm(com=days, adjust=False).mean()
			LTAvg14=df['LT'].ewm(com=days, adjust=False).mean()
			RS = df['UTAvg14']/df['LTAvg14']
			self.rsi[days] = 100-100/(1+df['RS'])
		return self.rsi[days]

	def GetStockData(symbol,ticker=None,start=None,end=None):
		self.df =  pdr.get_data_yahoo(symbol+".NS",start,end)




##RSI CALCULATION

df['UT']=np.where(df['Adj Close'] > df['Adj Close'].shift(1), df['Adj Close']-df['Adj Close'].shift(1), 0)
df['LT']=np.where(df['Adj Close'] < df['Adj Close'].shift(1), df['Adj Close'].shift(1)-df['Adj Close'], 0)
#df['UTAvg14'] = df['UT'].rolling(window=14).mean()
#df['UTAvg14']=df['UT'].ewm(span=14, adjust=False).mean()
df['UTAvg14']=df['UT'].ewm(com=13, adjust=False).mean()
#df['LTAvg14'] = df['LT'].rolling(window=14).mean()
df['LTAvg14']=df['LT'].ewm(com=13, adjust=False).mean()
df['RS'] = df['UTAvg14']/df['LTAvg14']
df['RSI'] = 100-100/(1+df['RS'])




# print(df.tail())
# df.head()
# import pdb
# pdb.set_trace()
##PLOTTING OF RSI
# fig, axes = plt.subplots(nrows=2, ncols=1)
# df.plot(ax=axes[0],y="Adj Close")
# df.plot(ax=axes[1],y="RSI")
# #df.plot(y="Adj Close")
# plt.axhline(y = 80, color = 'b', linestyle = '-')
# plt.axhline(y = 20, color = 'r', linestyle = '-')
# plt.show()