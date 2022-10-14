from __future__ import division
import yfinance as yf
from yahoo_fin import stock_info as si
import signal, time
class timeout(Exception):
	def __init__(self, m):
		self.message = m
	def __str__(self):
		return self.message
def handler(sig, frame):
	raise timeout("Event timed out")
def timeLimit(timeLimit):
	def intermediate(func):
		def decorator(*args, **kwargs):
			signal.signal(signal.SIGALRM, handler)
			signal.alarm(timeLimit)
			func(*args, **kwargs)
			signal.alarm(0)
		return decorator
	return intermediate
def union(li):
	finalList = []
	for item in range(len(li)):
		finalList = list(set(finalList) | set(li[item]))
	return finalList
def data(stat, ticker=0, downloads=0):
	if (stat=="beta"):
		return ticker["beta"]
	elif (stat=="float"):
		return ticker["floatShares"]
	elif (stat=="oustanding"):
		return ticker["sharesOutstanding"]
	elif (stat=="short%Float"):
		return ticker["shortPercentOfFloat"]
	elif (stat=="relativeVolume"):
		volumes = downloads.Volume
		totalVolume = 0
		for i in range(len(volumes)):
			totalVolume+=volumes[i]
		averageVolume = totalVolume/(len(volumes)/7)
		totalVolume = 0
		for i in range(len(volumes[-21:])):
			totalVolume+=volumes[i]
		currentVolume = totalVolume/(len(volumes)/7)
		return currentVolume/averageVolume
	elif (stat=="awesomeOscillator"):
		shortTotal = 0
		longTotoal = 0
		for i in range(len(downloads.Volume[-34:])):
			high = downloads.High[i]
			low = downloads.Low[i]
			midpoint = (high+low)/2
			longTotal+=midPoint
			if (i>27):
				shortTotal+=midPoint
		shortAverage = shortTotal/5
		longAverage = longTotal/34
		return shortAverage-longAverage
	elif (stat=="williamsPercentR"):
		high = 0
		low = 100000
		for i in range(len(downloads.Volume[-14:])):
			if (downloads.High[i]>high):
				high = downloads.High[i]
			if (downloads.Low[i]<low):
				low = downloads.Low[i]
		return (high-downloads.Close[-1])/(high-low)
	elif (stat=="chandeMomentum"):
		highSum = 0
		lowSum = 0
		for i in range(len(downloads.Volume[-20:])):
			if (downloads.Close[i]>downloads.Open[i]):
				highSum+=downloads.Close[i]
			elif (downloads.Close[i]<downloads.Open[i]):
				lowSum+=downloads.Close[i]
		return (highSum-lowSum)/(highSum+lowSum)
	elif (stat=="intradayMomentum"):
		gains=0
		losses=0
		for i in range(len(downloads.Volume[-14:])):
			if (downloads.Close[i]>downloads.Open[i]):
				gains+=downloads.Close[i]-downloads.Open[i]
			elif (downloads.Close[i]<downloads.Open[i]):
				losses+=downloads.Open[i]-downloads.Close[i]
		return (gains/(gains+losses))*100
	elif (stat=="ultimateOscillator"):
		bp7 = 0
		bp14 = 0
		bp28 = 0
		tr7 = 0
		tr14 = 0
		tr28 = 0
		for i in range(len(downloads.Volume[-28:])):
			if (i>20):
				bp7+=downloads.Close[-1]-min(downloads.Low[-7:])
				tr7+=max(downloads.High[-7:])-min(downloads.Low[-7:])
			if (i>13):
				bp14+=downloads.Close[-1]-min(downloads.Low[-14:])
				tr14+=max(downloads.High[-14:])-min(downloads.Low[-14:])
			bp28+=downloads.Close[-1]-min(downloads.Low)
			tr28+=max(downloads.High)-min(downloads.Low)
		average7 = bp7/tr7
		average14 = bp14/tr14
		average28 = bp28/tr28
		return (((average7*4)+(average14*2)+average28)/(4+2+1))*100
	else:
		return 0
@timeLimit(5)
def getData(stock):
	return [yf.Ticker(stock).info, yf.download(stock, period="1mo", interval="1h")]
class Scanner:
	def __init__(self, print):
		self.print = print
	def findStocks(self):
		stockList = []
		session = FTP("ftp.nasdaqtrader.com")
		session.login()
		session.cwd("Symboldirectory")
		with open("nasdaqlisted.txt", "wb") as fp:
			session.retrbinary("RETR nasdaqlisted.txt", fp.write)
		session.quit()
		with open("nasdaqlisted.txt", "r") as f:
			nasdaq = f.readlines()
		for line in nasdaq[1:-1]:
			data = line.split("|")
			etf = data[-1].strip()
			category = data[1]
			if (etf=="N" and (("common stock" in category) or ("Common Stock" in category)) and ("arrant" not in category)):
				stockList.append(data[0])
		return stockList
	def preScreener(self):
		stockList = findStocks()
		stocks = []
		for stock in stockList:
			stock = str(stock).strip()
			stockData = 0
			if (self.print and stockList.index(stock)%25==0):
				print(stockList.index(stock)+"/"+len(stockList))
			try:
				stockData = getData(stock)
				if (stockData==0):
					continue
				sleep(1)
				beta = data("beta", ticker=stockData[0])
				if (beta<2 or beta>-2):
					continue
				rVolume = data("relativeVolume", ticker=stockData[0])
				if (relativeVolume<2):
					continue
				awesomeO = data("awesomeOscillator", downloads=stockData[1])
				if (awesomeO>0):
					continue
				williamsR = data("williamsPercentR", downloads=stockData[1])
				if (williamsR>80):
					continue
				chandeM = data("chandeMomentum", downloads=stockData[1])
				if (chandeM>-50):
					continue
				intraM = data("intradayMomentum", downloads=stockData[1])
				if (intraM>30):
					continue
				ultimateO = data("ultimateOscillator", downloads=stockData[1])
				if (ultimate>30):
					continue
				stocks.append(stock)
			except (AttributeError, TypeError, requests.exceptions.ChunkedEncodingError, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, urllib2.URLError, ValueError, IndexError, ZeroDivisionError, timeout):
				continue
		dateStamp = datetime.now().strftime("%m-%d-%Y")
		with open("scannerStockList.txt", "w+") as f:
			f.write(str(stocks))
			f.write("\n"+dateStamp)
		return stocks
	def postScreener(self, stockList):
		stocks = []
		for stock in stockList:
			try:
				stockData = getData(stock)
				if (stockData==0):
					continue
				sleep(1)
				awesomeO = data("awesomeOscillator", downloads=stockData[1])
				if (awesomeO<0):
					continue
				williamsR = data("williamsPercentR", downloads=stockData[1])
				if (williamsR<80):
					continue
				chandeM = data("chandeMomentum", downloads=stockData[1])
				if (chandeM>-50):
					continue
				intraM = data("intradayMomentum", downloads=stockData[1])
				if (intraM<30):
					continue
				ultimateO = data("ultimateOscillator", downloads=stockData[1])
				if (ultimate<30):
					continue
				stocks.append(stocks)
			except (AttributeError, TypeError, requests.exceptions.ChunkedEncodingError, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, urllib2.URLError, ValueError, IndexError, ZeroDivisionError, timeout):
				continue
		return stocks
