from __future__ import division
from yahoofinancials import YahooFinancials
import yfinance as yf
from timeout_decorator import timeout
from time import sleep
import timeout_decorator, urllib2
from math import isnan
from requests.exceptions import ConnectionError
import pymail, datetime
senderObject = pymail.Pymail()
@timeout(10)
def data(ticker, stock, info):
	try:
		result = ""
	        if (len(ticker)>118):
	                if (info=="price"):
	                        result = YahooFinancials(stock).get_current_price()
	                        sleep(0.1)
			elif (info=="mr"):
	                        stockObject = YahooFinancials(stock)
	                        currentPrice = stockObject.get_prev_close_price()
	                        lastClose = float(yf.download(stock, period="1mo", interval="1d").Close[-3])
	                        result = ((currentPrice-lastClose)/lastClose)*100
	                elif (info=="float"):
	                        result = ticker["floatShares"]
	                elif (info=="shortAverage"):
	                        result = ticker["fiftyDayAverage"]
			elif (info=="longAverage"):
				result = ticker["twoHundredDayAverage"]
	                elif (info=="cVolume"):
	                        result = ticker["volume"]
	                elif (info=="aVolume"):
	                        result = ticker["averageVolume"]
			elif (info=="rVolume"):
				volume = ticker["volume"]
				averageVolume = ticker["averageVolume"]
				result = volume/averageVolume
	                elif (info=="beta"):
	                        result = ticker["beta"]
			elif (info=="averageDeviance"):
				shortAverage = ticker["fiftyDayAverage"]
				longAverage = ticker["twoHundredDayAverage"]
				result = ((shortAverage-longAverage)/longAverage)*100
			elif (info=="baRatio"):
				bid = ticker["bid"]
				ask = ticker["ask"]
				result = ((ask-bid)/bid)
			elif (info=="growth"):
				startPrice = YahooFinancials(stock).get_open_price()
				endPrice = YahooFinancials(stock).get_current_price()
				result = ((endPrice-startPrice)/startPrice)*100
			elif (info=="paRatio"):
				result = ticker["priceToBook"]
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
			elif (info=="swingState"):
	                        highs = 0
                                lows = 0
                                openPrices = yf.download(stock, period="5d").Open
                                closePrices = yf.download(stock, period="5d").Close
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
			elif (info=="kst"):
				close = yf.download(stock, period="1mo").Close[-1]
				closePrices = yf.download(stock, period="3mo").Close
				rocs = []
				rmcas = []
				for i in range(4):
				        loopLap=0
				        origin=0
				        subRoc = []
				        for prices in closePrices:
				                try:
				                        if (loopLap>9 and i==0):
				                                subRoc.append((prices-closePrices[origin])/closePrices[origin])
				                        elif (loopLap>14 and i==1):
				                                subRoc.append((prices-closePrices[origin])/closePrices[origin])
				                        elif (loopLap>19 and i==2):
				                                subRoc.append((prices-closePrices[origin])/closePrices[origin])
				                        elif (loopLap>29 and i==3):
				                                subRoc.append((prices-closePrices[origin])/closePrices[origin])
				                except TypeError:
				                        continue
						finally:
				                        loopLap+=1
				                        if (loopLap>9 and i==0):
				                                origin+=1
				                        elif (loopLap>14 and i==1):
				                                origin+=1
				                        elif (loopLap>19 and i==2):
				                                origin+=1
				                        elif (loopLap>29 and i==3):
				                                origin+=1
				        rocs.append(subRoc)
				for e in range(len(rocs)):
				        total=0
				        if (e!=3):
				                for roc in rocs[e][-10:]:
				                        total+=roc
				                rmcas.append(total/10)
				        else:
				                for roc in rocs[e][-15:]:
				                        total+=roc
				                rmcas.append(total/15)
				kts=0
				loopLap=1
				for values in rmcas:
				        kts+=values*loopLap
				        loopLap+=1
				result=kts
	                else:
	                        result = ""
	        else:
	                result = ""
	except ValueError:
		result = ""
	except IndexError:
		result = ""
	except ZeroDivisionError:
		result = ""
	finally:
		if (result is None or result=="" or isnan(result)):
			result = ""
       	return result
@timeout(10)
def getData(stock):
	ticker = yf.Ticker(stock)
        return ticker.info
compactDate = datetime.datetime.now().strftime("%m%d%y")
saveFile = "stockData"+compactDate+".txt"
with open("preScannerStockList.txt", "r") as f:
	stocks = f.readlines()[0]
	stocks = stocks.replace("\n","")
        stonks = stocks[1:]
        stonks = stonks[:-1]
        stonks = stonks.replace("'", "")
        stonks = stonks.replace(" ", "")
stockList = stonks.split(",")
with open(saveFile, "w+") as f:
	f.write("")
allData = []
n=1
interrupt=0
for stock in stockList:
	try:
		print("\n"+stock)
		stockData = []
		stockObject=0
		while True:
			try:
				stockObject = getData(stock)
			except timeout_decorator.timeout_decorator.TimeoutError:
				interrupt+=1
				if (interrupt>2):
		                	interrupt=0
					break
				else:
					continue
		        except urllib2.URLError:
		                interrupt+=1
                                if (interrupt>2):
                                        interrupt=0
                                        break
                                else:
                                        continue
			break
		if (stockObject==0):
			continue
		interrupt=0
		stockData.append(data(stockObject, stock, "beta"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "shortAverage"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "longAverage"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "averageDeviance"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "float"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "cVolume"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "aVolume"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "baRatio"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "growth"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "paRatio"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "mr"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "rsi"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "rVolume"))
		sleep(0.25)
		stockData.append(data(stockObject, stock, "swingState"))
		sleep(0.25)
		stockData.append(stock)
		sleep(0.25)
		stockData.append(data(stockObject, stock, "kst"))
		sleep(1)
		print("Beta: "+str(stockData[0]))
		print("50 Day Average: "+str(stockData[1]))
		print("200 Day Average: "+str(stockData[2]))
		print("Difference from moving average: "+str(stockData[3]))
		print("Float: "+str(stockData[4]))
		print("Current Volume: "+str(stockData[5]))
		print("Average Volume: "+str(stockData[6]))
		print("Relative Volume: "+str(stockData[12]))
		print("Bid/Ask Ratio: "+str(stockData[7]))
		print("Growth: "+str(stockData[8]))
		print("Price/Book Ratio: "+str(stockData[9]))
		print("Momentum: "+str(stockData[10]))
		print("Relative Strength Index: "+str(stockData[11]))
		print("Relative Volume: "+str(stockData[12]))
		print("KST: "+str(stockData[15]))
		print(str(n)+"/"+str(len(stockList)))
		allData.append(stockData)
		interrupt=0
	except ValueError:
		continue
	except IndexError:
		continue
	except ZeroDivisionError:
		continue
	except timeout_decorator.timeout_decorator.TimeoutError:
		continue
	except ConnectionError:
		continue
	except KeyboardInterrupt:
		exit()
	finally:
		n+=1
with open(saveFile, "a") as f:
	f.write(str(allData))
senderObject.sendMail("iotgearemail@gmail.com", "JimmyJohn", "grantdcongdon@gmail.com", "Stock Data", filename=saveFile)
