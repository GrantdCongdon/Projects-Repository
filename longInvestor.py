import os, sys, math, datetime, holidays, yahoofinancials, timeout_decorator
import yfinance as yf
from time import sleep
from yahoofinancials import YahooFinancials
from timeout_decorator import timeout
from ast import literal_eval
balance = float(input("Enter Budget: "))
stockList = str(input("Enter Stocks to Trade(seperate using commas): "))
stockList = stockList.split(",")
startBudget = balance
killSwitch = False
buyCooldown = False
sellCooldown = False
commission=6.99
quantity = []
initialPrices = []
buyLimit = []
sellLimit = []
profits = []
transGrad = [[50, 1], [45, 0.9], [40, 0.8], [35, 0.7], [30, 0.6], [25, 0.5], [20, 0.4], [15, 0.3], [10, 0.2], [1, 0.1]]
usHolidays = holidays.US()
def weekendHoliday(now):
	if (now.strftime("%Y-%m-%d") in usHolidays):
		return True
	if (now.weekday() > 4):
		return True
	return False
def afterHours(now):
	hour = int(now.strftime("%H"))
	minute = int(now.strftime("%M"))
	if ((hour==15 and minute>50) or (hour>15)):
		return True
	elif ((hour==9 and minute<30) or (hour<9)):
		return True
	else:
		return False
@timeout(15)
def getPrice(stock):
	stockObject = YahooFinancials(stock)
	sleep(0.1)
	try:
		stockPrice = stockObject.get_current_price()
	except yahoofinancials.ManagedException:
			stockPrice = 0
	sleep(0.1)
	return stockPrice
def movingAverage(stock, period, interval):
	startTime = datetime.datetime.now()-period
	endTime = datetime.datetime.now()
	startTime = startTime.strftime("%Y-%m-%d")
	endTime = endTime.strftime("%Y-%m-%d")
	priceList = []
	stockData = yf.download(stock, start=startTime, end=endTime, interval="1d")
	for d in range(len(stockData["High"])-1):
		high = stockData["High"][d]
		low = stockData["Low"][d]
		midpoint = (high+low)/2
		priceList.append(midpoint)
	total = sum(priceList)
	average = total/len(priceList)
	return average
def trade(transaction, price, amount):
	global balance
	if (transaction=="buy"):
		balance = balance-(price*amount)-commission
	elif (transaction=="sell"):
		balance = balance+(price*amount)-commission
	else:
		print("Error")
	return 0
#retrieve information about algorithmic chosen positions
found = False
files = os.listdir()
for i in files:
	if (i=="longData.txt"):
		found=True
		break
	else:
		pass
if (not found):
	with open("longData.txt", "w+") as f:
		f.write("")
with open("longData.txt", "r") as f:
	data = f.read()
if (data==""):
	with open("longData.txt", "w") as f:
		for stock in stockList:
			f.write(stock)
			f.write("\n0\n0\n")
			f.write(str(buyLimit)+"\n")
			f.write(str(sellLimit)+"\n!")
with open("longData.txt", "r") as f:
	data = f.read()
stockData = data.split("!")
for d in stockData:
	info = d.split("\n")
	for stock in stockList:
		if (info[0]==stock):
			quantity.append(info[1])
			initialPrices.append(info[2])
			buyLimit.append(literal_eval(info[3]))
			sellLimit.append(literal_eval(info[4]))
			profits.append(info[1]*info[2])
			break
		else:
			pass
#Main Program
while True:
	try:
		now = datetime.datetime.now()
		if (killSwitch):
			break
		elif (buyCooldown and sellCooldown):
			print("Waiting for market to close")
			while True:
				now = datetime.datetime.now()
				if (afterHours(now)):
					buyCooldown = False
					sellCooldown = False
					break
				sleep(300)
		elif (weekendHoliday(now) or afterHours(now)):
			print("Waiting for market to open")
			while True:
				now = datetime.datetime.now()
				if (not weekendHoliday(now) and not afterHours(now)):
					break
				sleep(900)
		else:
			print("Trading Started")
			if (stockList==[]):
				buyCooldown = True
				sellCooldown = True
				continue
			sNumber = len(stockList)
			while True:
				now = datetime.datetime.now()
				if (sNumber==0 or afterHours(now) or (buyCooldown and sellCooldown)):
					break
				i=0
				prices = []
				shortAverages = []
				longAverages = []
				deviations = []
				for stock in stockList:
					try:
						stockPrice = getPrice(stock)
						shortTime = datetime.timedelta(months=3)
						longTime = datetime.timedelta(years=1)
						shortAverage = movingAverage(stock, shortTime)
						longAverage = movingAverage(stock, longTime)
						deviation = ((stockPrice-shortAverage)/shortAverage)
						prices.append(stockPrice)
						shortAverages.append(shortAverage)
						longAverages.append(longAverage)
						deviations.append(deviation)
						i+=1
					except timeout_decorator.timeout_decorator.TimeoutError:
						continue
				i=0
				for stock in stockList:
					for e in range(len(transGrad)):
						if (deviations[i]<-1*transGrad[e][1] and balance>prices[i]*transGrad[e][0]+commission and not buyCooldown):
							trade("buy", prices[i], transGrad[e][0])
							print("Bought "+str(transGrad[e][0])+" "+stock)
							balanceChange = ((balance-startingBudget)/startingBudget)*100
							print("Starting Balance: "+str(startingBudget))
							print("End Balance: "+str(balance))
							print("Change: "+str(balanceChange)+"%")
							buyCooldown = True
							break
					i+=1
				i=0
				for stock in stockList:
					for e in range(len(transGrad)):
						if (deviations[i]>transGrad[e][1] and quantity[i]>=transGrad[e][0] and not sellCooldown):
							trade("sell", prices[i], quantity[i])
							print("Sold "+str(transGrad[e][0])+" "+stock)
							quantity[i] = quantity[i]-transGrad[e][0]
							balanceChange = ((balance-startingBudget)/startingBudget)*100
							print("Starting Balance: "+str(startingBudget))
							print("End Balance: "+str(balance))
							print("Change: "+str(balanceChange)+"%")
							sellCooldown = True
							break
					i+=1
				sleep(60)
	except KeyboardInterrupt:
		exit(0)
