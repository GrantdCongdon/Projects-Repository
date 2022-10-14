from __future__ import division
from yahoo_fin import stock_info as si
from yahoofinancials import YahooFinancials
import yfinance as yf
from time import sleep
import timeout_decorator, urllib.error
from timeout_decorator import timeout
from operator import itemgetter
from datetime import datetime, timedelta
import requests, os
@timeout(10)
def data(ticker, stock, info):
	if (len(ticker)>118):
		if (info=="price"):
			stockObject = YahooFinancials(stock)
			result = stockObject.get_current_price()
			sleep(1)
		elif (info=="float"):
			result = ticker["floatShares"]
		elif (info=="shortAverage"):
			result = ticker["fiftyDayAverage"]
		elif (info=="longAverage"):
			result = ticker["twoHundredDayAverage"]
		elif (info=="beta"):
			result = ticker["beta"]
		elif (info=="rVolume"):
			currentVolume = ticker["volume"]
			averageVolume = ticker["averageVolume"]
			result = currentVolume/averageVolume
		elif (info=="rsi"):
			highs = 0
			lows = 0
			openPrices = yf.download(stock, period="1mo").Open
			closePrices = yf.download(stock, period="1mo").Close
			for i in range(len(openPrices)):
				change = closePrices[i]-openPrices[i]
				if (change>0):
					highs+=change
				else:
					lows+=change
			lows = lows*-1
			averageHigh = highs/len(openPrices)
			averageLow = lows/len(openPrices)
			RS = averageHigh/averageLow
			result = 100-(100/(1+RS))
		else:
			result = ""
	else:
		result = ""
	return result
@timeout(10)
def getData(ticker):
	return ticker.info
class Scanner:
	def __init__(self, filter):
		self.filter = filter
	def screener(self):
		global relativeVolume
		stockDict = []
		stockList = si.tickers_nasdaq()
		interrupt = 0
		for stock in stockList:
			try:
				stock = str(stock)
				stock = stock.strip()
				ticker = yf.Ticker(stock)
				stockData = 0
				try:
					while True:
						try:
							stockData = getData(ticker)
						except timeout_decorator.timeout_decorator.TimeoutError:
							interrupt+=1
							if (interrupt>2):
								interrupt=0
								break
							else:
								continue
						except requests.exceptions.ReadTimeout:
							interrupt+=1
							if (interrupt>2):
								interrupt=0
								break
							else:
								continue
						except requests.exceptions.ConnectionError:
							interrupt+=1
							if (interrupt>2):
								interrupt=0
								break
							else:
								continue
						except urllib.error.URLError:
							interrupt+=1
							if (interrupt>2):
								interrupt=0
								break
							else:
								continue
						break
				except ValueError:
					continue
				except IndexError:
					continue
				except KeyError:
					continue
				if (stockData==0):
					continue
				sleep(1)
				floatData = data(stockData, stock, "float")
				if (floatData!="" and floatData is not None and floatData!=0):
					if (int(floatData) < 100000000):
						pass
					else:
						continue
				else:
					continue
				shortMovingAverage = data(stockData, stock, "shortAverage")
				longMovingAverage = data(stockData, stock, "longAverage")
				if (shortMovingAverage!=0 and longMovingAverage!=0 and shortMovingAverage is not None and shortMovingAverage!="" and longMovingAverage is not None and longMovingAverage!=""):
					if (shortMovingAverage>longMovingAverage):
						pass
					else:
						continue
				else:
					continue
				relativeVolume = data(stockData, stock, "rVolume")
				if (relativeVolume!=0 and relativeVolume!="" and relativeVolume is not None):
					if (relativeVolume>2):
						pass
					else:
						continue
				else:
					continue
				price=None
				interrupt=0
				while True:
					try:
						price = data(stockData, stock, "price")
					except timeout_decorator.timeout_decorator.TimeoutError:
						interrupt+=1
						if (interrupt>2):
							interrupt=0
							break
						else:
							continue
					except urllib.error.URLError:
						interrupt+=1
						if (interrupt>2):
							interrupt=0
							break
						else:
							continue
					break
				if (price is not None and price!=0):
					if (price<20):
						pass
					else:
						continue
				else:
					continue
				beta = data(stockData, stock, "beta")
				if (beta!="" and beta is not None and beta!=0):
					if (beta>2):
						pass
					else:
						continue
				else:
					continue
				stockDict.append(str(stock))
				interrupt=0
			except IndexError:
				continue
			except ZeroDivisionError:
				continue
			except timeout_decorator.timeout_decorator.TimeoutError:
				continue
			except urllib.error.URLError:
				continue
			except requests.exceptions.ReadTimeout:
                                continue
			except requests.exceptions.ConnectionError:
				continue
			except KeyboardInterrupt:
				exit(1)
		with open("preScannerStockList.txt", "w+") as f:
			f.write(str(stockDict))
		rsiList = []
		rsiDict = {}
		interrupt=0
		for stock in stockDict:
			try:
				ticker = yf.Ticker(stock)
				stockData = 0
				try:
					while True:
						try:
							stockData = getData(ticker)
						except timeout_decorator.timeout_decorator.TimeoutError:
							interrupt+=1
							if (interrupt>2):
								interrupt=0
								break
							else:
								continue
						except requests.exceptions.ReadTimeout:
                                                        interrupt+=1
                                                        if (interrupt>2):
                                                                interrupt=0
                                                                break
                                                        else:
                                                                continue
						except requests.exceptions.ConnectionError:
							interrupt+=1
							if (interrupt>2):
								interrupt=0
								break
							else:
								continue
						except urllib.error.URLError:
							interrupt+=1
							if (interrupt>2):
								interrupt=0
								break
							else:
								continue
						break
				except ValueError:
					continue
				except IndexError:
					continue
				except KeyError:
					continue
				if (stockData==0):
					continue
				sleep(1)
				rsi = data(stockData, stock, "rsi")
				if (rsi!="" and rsi is not None):
					rsiDict.update({stock:rsi})
					interrupt=0
				else:
					interrupt=0
					continue
			except timeout_decorator.timeout_decorator.TimeoutError:
				continue
			except urllib.error.URLError:
				continue
			except requests.exceptions.ReadTimeout:
                                continue
			except requests.exceptions.ConnectionError:
				continue
			except IndexError:
				continue
			except KeyboardInterrupt:
				exit(1)
		rsiDictS = sorted(rsiDict.items(), key=itemgetter(1))
		for stock in rsiDictS:
			rsiList.append(stock[0])
		rsiList = rsiList[:3]
		dateStamp = datetime.now().strftime("%d-%m-%Y")
		with open("scannerStockList.txt", "w") as f:
			f.write(str(rsiList))
			f.write("\n"+dateStamp)
		sleep(3)
		return rsiList
