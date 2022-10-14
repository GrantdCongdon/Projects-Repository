import os, sys, math, datetime, holidays, yahoofinancials, timeout_decorator, scanner
import yfinance as yf
from time import sleep
from yahoofinancials import YahooFinancials
from timeout_decorator import timeout
balance = float(input("Enter Budget: "))
startingBudget = balance
killSwitch = False
tradeCooldown = False
scannerComplete = False
commission=6.99
stockList = []
usHolidays = holidays.US()
stockScanner = scanner.Scanner(0)
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
def scannerTime(now):
	hour = int(now.strftime("%H"))
	if (hour<4):
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
def trade(transaction, price, amount):
	global balance
	if (transaction=="buy"):
		balance = balance-(price*amount)-commission
	elif (transaction=="sell"):
		balance = balance+(price*amount)-commission
	else:
		print("Error")
	return 0
#Main Program
while True:
	try:
		now = datetime.datetime.now()
		if (killSwitch):
			break
		elif (tradeCooldown):
			print("Waiting for market to close")
			scannerComplete = False
			while True:
				now = datetime.datetime.now()
				if (afterHours(now)):
					tradeCooldown = False
					break
				sleep(300)
		elif (scannerTime(now) and not weekendHoliday(now)):
			print("\nScanner Started\n")
			stockList = stockScanner.screener()
			sleep(3)
			print("\nScanner Complete")
			print("Selected Stocks: "+str(stockList))
			scannerComplete = True
			while True:
				now = datetime.datetime.now()
				if (not weekendHoliday(now) and not afterHours(now)):
					tradeCooldown = False
					break
				sleep(300)
		elif (weekendHoliday(now) or afterHours(now)):
			print("Waiting for valid day/time to start scanner")
			scannerComplete = False
			while True:
				now = datetime.datetime.now()
				if ((scannerTime(now) and not weekendHoliday(now))) or (not weekendHoliday(now) and not afterHours(now)):
					break
				sleep(900)
		else:
			print("Trading Started")
			if (not scannerComplete):
				with open("scannerStockList.txt", "r") as f:
					stockDate = f.readlines()
					stocks = stockDate[0]
					date = stockDate[1].strip()
					stocks = stocks.replace("\n", "")
					stonks = stocks[1:]
					stonks = stonks[:-1]
					stonks = stonks.replace("'", "")
					stonks = stonks.replace(" ", "")
				stockList = stonks.split(",")
				todayDate = datetime.datetime.now().strftime("%d-%m-%Y")
				if (todayDate!=date):
					tradeCooldown = True
					continue
			if (stockList==[]):
				tradeCooldown = True
				continue
			quantity = []
			initialPrices = []
			indivisualHighs = []
			sNumber = len(stockList)
			totalCommission = sNumber*commission*2
			budget = balance-(totalCommission/2)
			moneyPerStock = math.floor(budget/sNumber)
			for stock in stockList:
				try:
					buyPrice = getPrice(stock)
					if (buyPrice is None or buyPrice==0):
						stockList.remove(stock)
						sNumber = len(stockList)
						totalCommission = sNumber*commission*2
						continue
					else:
						amount = math.floor(moneyPerStock/buyPrice)
						trade("buy", buyPrice, amount)
						print("Bought "+str(amount)+" "+stock)
						quantity.append(amount)
						initialPrices.append(buyPrice)
						indivisualHighs.append(-100)
				except timeout_decorator.timeout_decorator.TimeoutError:
					continue
			moneyLeft = balance
			now = datetime.datetime.now()
			while True:
				if (sNumber==0 or tradeCooldown):
					break
				i=0
				prices = []
				indivisualGains = []
				indivisualChanges = []
				indivisualDrops = []
				highChange = 0
				for stock in stockList:
					try:
						stockPrice = getPrice(stock)
						indivisualGain = stockPrice*quantity[i]
						indivisualChange = ((stockPrice-initialPrices[i])/initialPrices[i])*100
						if (indivisualChange>indivisualHighs[i]):
							indivisualHighs[i] = indivisualChange
						indivisualDrop = indivisualChange-indivisualHighs[i]
						prices.append(stockPrice)
						indivisualChanges.append(indivisualChange)
						indivisualGains.append(indivisualGain)
						indivisualDrops.append(indivisualDrop)
						i+=1
					except timeout_decorator.timeout_decorator.TimeoutError:
						continue
				netGain = sum(indivisualGains)
				totalChange = (((netGain+moneyLeft-totalCommission)-startingBudget)/startingBudget)*100
				if (totalChange>highChange):
					highChange = totalChange
				if (highChange!=0):
					percentDrop = totalChange-highChange
				i=0
				for stock in stockList:
					try:
						if (indivisualChanges[i]<-3 or (indivisualChanges[i]>4.5 and indivisualDrops[i]<-1.5)):
							trade("sell", prices[i], quantity[i])
							print("Sold "+str(quantity[i])+" "+stock)
							stockList.remove(stock)
							quantity.pop(i)
							initialPrices.pop(i)
							sNumber = len(stockList)
							if (sNumber==0):
								balanceChange = ((balance-startingBudget)/startingBudget)*100
								print("Starting Balance: "+str(startingBudget))
								print("End Balance: "+str(balance))
								print("Potential High: "+str(highChange)+"%")
								print("Change: "+str(balanceChange)+"%")
								startingBudget=balance
								tradeCooldown=True
								break
							i-=1
						i+=1
					except IndexError:
						break
				if ((totalChange>1 and percentDrop<=-1 and percentDrop>-3 and not tradeCooldown) or (afterHours(now))):
					i=0
					for stock in stockList:
						trade("sell", prices[i], quantity[i])
						print("Sold "+str(quantity[i])+" "+stock)
						quantity[i] = 0
						i+=1
					balanceChange = ((balance-startingBudget)/startingBudget)*100
					print("Starting Balance: "+str(startingBudget))
					print("End Balance: "+str(balance))
					print("Potential High: "+str(highChange)+"%")
					print("Change: "+str(balanceChange)+"%")
					startingBudget=balance
					tradeCooldown = True
					break
	except KeyboardInterrupt:
		exit(0)
