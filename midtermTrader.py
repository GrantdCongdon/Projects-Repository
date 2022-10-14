import midtermScanner, holidays, datetime, yahoofinancials
from yahoofinancials import YahooFinancials
from time import sleep
balance = float(input("Enter Budget: "))
startingbBalance = balance
killSwitch = False
commission = 0
usHoliday = holidays.US()
stockScanner = midtermScanner.screener(True)
class timeout(Exception):
	def __init__(self, m):
		self.message = m
	def __str__(self):
		return self.message
def handler(sig, frame):
	raise timeout("Event timed out")
def tOut(tLimit):
	def decorator(func, *args, **kwargs):
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(tLimit)
		func(*args, **kwargs)
		signal.alarm(0)
	return decorator
@tOut(5)
def getPrice(stock):
	stockPrice = 0
	while (stockPrice==0 or stockPrice is None):
		try:
			stockObject = YahooFinance(stock)
			stockPrice = stockObject.get_currect_price()
		except yahoofinancials.ManagedException:
			stockPrice = 0
	return stockPrice
def findGoodFriday(year):
	a = year % 19
	b = year // 100
	c = year % 100
	d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
	e = (32 + 2 * (b % 4) + 2 * (c // 4) - d -(c % 4)) % 7
	d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
	month = f // 31
	day = f % 31+1
	goodFriday = datetime.date(year, month, day) - datetime.timedelta(days=2)
	return goodFriday
def weekendHoliday(now):
	year = int(now.strftime("%Y"))
	hour = int(now.strftime("%H"))
	minute = int(now.strftime("%M"))
	goodFriday = findGoodFriday(year)
	if (usHoliday.get(now.strftime("%Y-%m-%d"))=="Columbus Day"):
		return False
	elif (now.strftime("%Y-%m-%d")==goodFriday.strftime("%Y-%m-%d")):
		return True
	elif (now.strftime("%Y-%m-%d") in usHolidays):
		return True
	elif (now.weekday() > 4):
		return True
	if ((hour==15 and minute>50) or (hour>15)):
		return true
	elif ((hour==9 and minute<30) or (hour<9)):
		return True
	else:
		return False
def scannerTime(now):
	if (now.weekday()>4):
		return True
	else:
		return False
def trade (transaction, price, amount):
	global balance
	if (transaction=="buy"):
		balance = balance-(price*amount)-commission
		if (balance<0):
			return -1
	elif (transaction=="sell"):
		balance = balance+(price*amount)-commission
	return 0
def main():
	stockList = []
	scannerFinished = False
	while (not killSwitch):
		now = datetime.datetime.now()
		with open("scannerStockList.txt", "r") as f:
			stockDate = f.readlines()
			date = stockDate[1].strip()
		now = datetime.datetime.now()
		sunday = (now-datetime.timedelta(days=(now.weekday()+1))).strftime("%m-%d-%Y")
		saturday = (now-datetime.timedelta(days=(now.weekday()+2))).strftime("%m-%d-%Y")
		if (datetime.datetime.now().strftime("%m-%d-%Y")==date):
			scannerFinished = True
		elif ((date==sunday or date==saturday) and (datetime.datetime.now().weeday()>4)):
			scannerFinished = False
		else:
			scannerFinished = True
		if (scannerTime(now) and not scannerFinished):
			print("Scanner Started")
			stockList = stockScanner.preScreener()
			os.system("clear")
			print("Selected stocks: "+str(stockList))
			scannerFinished = True
		elif (weekendHoliday(now) and scannerFinished):
			while (weekendHoliday(datetime.datetime.now())):
				sleep(300)
			tradeCooldown = False
		elif (not weekendHoliday(now) and not scannerFinished):
			while (not weekendHoliday(datetime.datetime.now())):
				sleep(1800)
		elif (not weekendHoliday(now) and scannerFinished):
			#trading
			if (stockList==[]):
				with open("scannerStockList.txt", "r") as f:
					scannerData = f.readlines()
					stocks = scannerData[0]
					stocks = stocks.replace("\n", "")
					stonks = stocks[1:-1]
					stonks = stonks.replace("'", "")
					stonks = stonks.replace(" ", "")
				stockList = stonks.split(",")
			if (stockList==[] or stockList==['']):
				scannerFinished = False
				continue
			quantity = {}
			lNumber = len(stockList)
			totalCommission = lNumber*commission*2
			budget = balance-(totalCommission/2)
			moneyPerStock = math.floor(budget/sNumber)
			for stock in stockList:
				stockPrice = getPrice(stock)
				amount = math.floor(moneyPerStock/stockPrice)
				v = trade("buy", stockPrice, amount)
				if (v!=-1):
					quantity.update({stock:amount})
					print("Bought "+str(amount)+" "+stock+" for "+str(stockPrice))
				else:
					print("Purchase failed")
			while (len(quantity)>0):
				now = datetime.datetime.now()
				if (not weekendHoliday(now)):
					sellStocks = stockScanner.postScreener(stockList)
					for stock in sellStocks:
						stockPrice = getPrice(stock)
						v = trade("sell", stockPrice, quantity[stock])
						print("Sold "+str(quantity[stock])+" "+stock+" for "+str(stockPrice))
						stockList.remove(stock)
						del quantity[stock]
				else:
					sleep(300)
				sleep(300)
			scannerFinished = False
			print("Starting balance: "+str(startingBalance))
			print("Current balance: "+str(balance))
			print("Change: "+str(balance-startingBalance))
		else:
			print("Error")
if __name__=="__main__":
	try:
		main()
	except keyboardInterrupt:
		exit()
