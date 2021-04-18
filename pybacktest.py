import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from functools import reduce

global stock


#stock = input("ENTET THE STOCK (INDIAN STOCK only):")
#df = pdr.get_data_yahoo(stock+".NS")


def RSI(df,days):
	df['UT']=np.where(df['Adj Close'] > df['Adj Close'].shift(1), df['Adj Close']-df['Adj Close'].shift(1), 0)
	df['LT']=np.where(df['Adj Close'] < df['Adj Close'].shift(1), df['Adj Close'].shift(1)-df['Adj Close'], 0)
	df['UTAvg14']=df['UT'].ewm(com=days-1, adjust=False).mean()
	df['LTAvg14']=df['LT'].ewm(com=days-1, adjust=False).mean()
	df['RS'] = df['UTAvg14']/df['LTAvg14']
	df['RSI_'+str(days)] = 100-100/(1+df['RS'])
	df.drop(columns=['UT','LT','UTAvg14',"LTAvg14",'RS'])
	return

def EMA(df,ema,column):
	df[column+"_EMA_"+str(ema)]=df[column].ewm(span=ema, adjust=False).mean()
	return


##RSI CALCULATION

# df['UT']=np.where(df['Adj Close'] > df['Adj Close'].shift(1), df['Adj Close']-df['Adj Close'].shift(1), 0)
# df['LT']=np.where(df['Adj Close'] < df['Adj Close'].shift(1), df['Adj Close'].shift(1)-df['Adj Close'], 0)
# #df['UTAvg14'] = df['UT'].rolling(window=14).mean()
# #df['UTAvg14']=df['UT'].ewm(span=14, adjust=False).mean()
# df['UTAvg14']=df['UT'].ewm(com=13, adjust=False).mean()
# #df['LTAvg14'] = df['LT'].rolling(window=14).mean()
# df['LTAvg14']=df['LT'].ewm(com=13, adjust=False).mean()
# df['RS'] = df['UTAvg14']/df['LTAvg14']
# df['RSI'] = 100-100/(1+df['RS'])

def RSIStrategy(df):
	RSI(df,14)
	RSI(df,7)
	EMA(df,10,"RSI_14")
	EMA(df,10,"RSI_7")
	buy = False
	bp = 0
	sp = 0
	txList = []
	for i in df.index:
		if not buy:
			if df["RSI_7_EMA_10"][i] > df["RSI_14_EMA_10"][i]:
				print("-"*100)
				buy	= True
				bp = df["Adj Close"][i]
				print("Bought at Rs. {}".format(bp)) 
		else:
			if df["RSI_7_EMA_10"][i] < df["RSI_14_EMA_10"][i]:
				buy = False
				sp = df["Adj Close"][i]
				txList.append((bp,sp))
				print("Sold at Rs. {} Profit Rs.{}".format(sp,sp-bp))
	PrintResult(df,txList)
	return



def PrintResult(df,txList):
	prlist = [sp-bp for (bp,sp) in txList if sp-bp>=0]
	lossList = [abs(sp-bp) for (bp,sp) in txList if sp-bp<0]
	print("Total number of trades : {}".format(len(txList)))

	print("Total number of Profitable trades : {}".format(len(prlist)))
	print("Total number of Losing trades : {}".format(len(lossList)))
	totalProfit = sum(prlist)
	totalLoss = sum(lossList)
	cProfit = totalProfit-totalLoss
	print("Total Profit : {}".format(totalProfit))
	print("Total Loss : {}".format(totalLoss))
	print("Cumulative Profit : {}".format(cProfit))
	cprofitList = [1-sp/bp if sp/bp<1 else sp/bp-1 for (bp,sp) in txList]
	print(cprofitList)
	print("Mean Profit Percentage : {}".format(np.mean(cprofitList)*100))
	# import pdb
	# pdb.set_trace()
	CD = max([e[0] for e in txList])
	print("Max Capital Employed : {}".format(CD))
	profitPercentage = round((cProfit/CD)*100,2)
	print("Profit Percentage : {}%".format(profitPercentage))
	return profitPercentage

def EmaCrossOver(df):
	EMA(df,10,"Adj Close")
	EMA(df,30,"Adj Close")
	buy = False
	bp = 0
	sp = 0
	txList = []
	for i in df.index:
		if not buy:
			if df["Adj Close_EMA_10"][i] > df["Adj Close_EMA_30"][i]:
				print("-"*100)
				buy	= True
				bp = df["Adj Close"][i]
				print("Bought at Rs. {}".format(bp)) 
		else:
			if df["Adj Close_EMA_10"][i] < df["Adj Close_EMA_30"][i]:
				buy = False
				sp = df["Adj Close"][i]
				txList.append((bp,sp))
				print("Sold at Rs. {} Profit Rs.{}".format(sp,sp-bp))

	#ax = df.plot(y="Adj Close")
	ax=df.plot(y="Adj Close_EMA_30")
	df.plot(ax=ax,y="Adj Close_EMA_10")
	plt.show()
	PrintResult(df,txList)

def MultipleEmaCrossOver(df):
	smallEmas = [5,10,15,25]
	largeEmas = [45,60,75,100]
	for ema in smallEmas+largeEmas:
		EMA(df,ema,"Adj Close")

	buy = False
	bp = 0
	sp = 0
	txList = []
	df["buy"] = np.nan
	df["sell"] = np.nan
	for i in df.index:
		minList = [df["Adj Close_EMA_{}".format(ema)][i] for ema in smallEmas]
		maxList = [df["Adj Close_EMA_{}".format(ema)][i] for ema in largeEmas]
		if not buy:
			if min(minList) > max(maxList):
				print("-"*100)
				buy	= True
				bp = df["Adj Close"][i]
				print("Bought at Rs. {}".format(bp))
				df["buy"][i] =  df["Adj Close"][i]
		else:
			if min(minList) < max(maxList):
				buy = False
				sp = df["Adj Close"][i]
				txList.append((bp,sp))
				df["sell"][i] =  df["Adj Close"][i]
				print("Sold at Rs. {} Profit Rs.{}".format(sp,sp-bp))


	#ax = df.plot(y="Adj Close")
	# ax=df.plot(y="Adj Close_EMA_30")
	# df.plot(ax=ax,y="Adj Close_EMA_10")
	# plt.show()
	returns =  PrintResult(df,txList)
	# import pdb
	# pdb.set_trace()



	ax = df.plot(y="Adj Close")
	plt.scatter(x=df.index,y=df["buy"],color="green")
	plt.scatter(x=df.index,y=df["sell"],color="red")
	#df.plot(ax=ax,y=buy)
	
	# for ema in smallEmas:
	# 	df.plot(ax=ax,y="Adj Close_EMA_{}".format(ema),color='green')
	# for ema in largeEmas:
	# 	df.plot(ax=ax,y="Adj Close_EMA_{}".format(ema),color='red')
	plt.show()

	return returns



def main():
	global stock
	niftyStocks = ['ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BPCL', 'BHARTIARTL', 'BRITANNIA', 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GRASIM', 'HCLTECH', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR', 'HDFC', 'ICICIBANK', 'ITC', 'IOC', 'INDUSINDBK', 'INFY', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NTPC', 'NESTLEIND', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBILIFE', 'SHREECEM', 'SBIN', 'SUNPHARMA', 'TCS', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'WIPRO']
	
	yf.pdr_override()
	start = dt.datetime(2015,2,20)
	end = dt.datetime.now()
	ofil = r"C:\Users\Gopikrishnan R\Documents\PYBACKTEST\out.csv"

	#single stock
	df =  pdr.get_data_yahoo("SBIN.NS",start,end)
	returns = MultipleEmaCrossOver(df)

	#df =  pdr.get_data_yahoo(stock,start,end)
	# with open(ofil,'w') as of:
	# 	for stock in niftyStocks:

	# 		#skip this
	# 		if stock in ["BHARTIARTL"]:
	# 			continue

	# 		stock = stock+".NS"
	# 		print("Processing for STOCK : {}".format(stock))
	# 		df = pdr.get_data_yahoo(stock,start,end)
	# 		returns = MultipleEmaCrossOver(df)
	# 		of.write(stock+","+str(returns)+"\n")



	# fig, axes = plt.subplots(nrows=2, ncols=1)
	# df.plot(ax=axes[1],y="RSI_14_EMA_10")
	# df.plot(ax=axes[1],y=RSI_7_EMA_10)
	# df.plot(ax=axes[0],y="Adj Close")
	# plt.title(stock,loc = 'center')
	# plt.show()
	# import pdb
	# pdb.set_trace()

	#RSIStrategy(df)
	#EmaCrossOver(df)
	



if __name__ == "__main__":
	main()



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