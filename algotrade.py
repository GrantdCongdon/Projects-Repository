import json, logging, configparser, random, re, accounts, market, datetime, accounts, database, pymail, math, scanner, timeout_decorator, yahoofinancials
from logging.handlers import RotatingFileHandler
from Tkinter import *
import quote as q
import order as Order
import datetime, holidays
from time import sleep
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import mysql.connector
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from timeout_decorator import timeout
from retrying import retry
from rauth import OAuth1Service
from yahoofinancials import YahooFinancials
import yfinance as yf
def sqlLog():
	mydb = mysql.connector.connect(
        	host="localhost",
        	user="oscar",
        	password="JimmyJohn",
        	database="algotrading"
	)
	cursor = mydb.cursor()
	return mydb,cursor
dValues = sqlLog()
mydb = dValues[0]
cursor = dValues[1]
killSwitch = False
tradeCooldown = False
stockData = []
quantity = []
purchaseArray = []
#order parameters
order = {"price_type": "",
        "order_term": "",
        "symbol": "",
        "order_action": "",
        "limit_price":"",
        "quantity": ""}
#Buttons
mainMenuItems = ["Configure AlgoTrading", "Manage Database", "Go Back"]
algoTradeItems = ["Begin Long AlgoTrading", "Begin Day AlgoTrading", "AlgoMenu"]
actualMainMenuItems = ["Get Market Quotes", "Begin Algotrading", "Manage Accounts", "Exit"]
algoingOptions = ["Cancel", "Reset Deviations"]
AP = [[50, 2], [45, 1.9], [40, 1.8], [35, 1.7], [30, 1.6], [25, 1.5], [20, 1.4], [15, 1.3], [10, 1.2], [1,1.1]]
g = len(AP)
bD = ["bd10", "bd9", "bd8", "bd7", "bd6", "bd5", "bd4", "bd3", "bd2", "bd1"]
sD = ["sd10", "sd9", "sd8", "sd7", "sd6", "sd5", "sd4", "sd3", "sd2", "sd1"]
commission=6.99
labelWidth=5
screenWidth=100
stocks = 0
buy=True
sell=True
#email
sendText = pymail.emailModule()
# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("python_client.log", maxBytes=5 * 1024 * 1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)
us_holidays = holidays.US()
#config
configLive = configparser.ConfigParser()
configLive.read('live/config.ini')
configSandbox = configparser.ConfigParser()
configSandbox.read('sandbox/config.ini')
#browser
opts = Options()
#opts.set_headless()
#scanner
stockScanner = scanner.Scanner(0)
def afterHours(now):
        # If a holiday
        if now.strftime('%Y-%m-%d') in us_holidays:
            return True
        # If it's a weekend
        if now.weekday() > 4:
            return True
        return False
def afterTime(now):
	hour = now.strftime("%H")
	minute = now.strftime("%M")
	if (int(hour)>=16):
		return True
	elif ((int(hour)==9 and int(minute)<30) or (int(hour)<9)):
		return True
	else:
		return False
def scannerTime(now):
        hour = now.strftime("%H")
        if (int(hour)<4):
                return True
        else:
                return False
def leapyear(year):
        if ((year % 4)==0):
                if ((year % 100)==0):
                        if ((year % 400) == 0):
                                leapyear = True
                        else:
                                leapyear = False
                else:
                        leapyear = True
        else:
                leapyear = False
        return leapyear
def historicalMovingAverage(start, stop, x, dataType="Open"):
        dataList = []
        generalData = stockData[x].data(start=start, stop=stop)
        for a in range(len(generalData[dataType])-1):
                dataList.append(generalData[dataType][a])
        total = sum(dataList)
        average = total/len(dataList)
        return average
def output(w, y, message):
	y.config(state="normal")
        y.delete(1.0, END)
        y.insert(END, message)
	y.config(state="disabled")
        w.update()
        return 0
def ramble(w, y, message):
	y.config(state="normal")
        y.insert(END, message)
	y.config(state="disabled")
        w.update()
        return 0
def createFrame(w, row, column, columnspan, stick):
        display = Frame(w)
        display.grid(row=row, column=column, columnspan=columnspan, sticky=stick)
        return display
def createButtons(y, buttons, w, account, base_url, etrade, live, username, password, session, accountId, messageInterface=None, y2=None, width=24, stick=S):
        r=0
        c=0
        for b in buttons:
                def cmd(x=b):
                        click(x, y, w, messageInterface, account, base_url, etrade, session, y2, live, accountId, username, password)
                Button(y, text=b, width=width, command=cmd).grid(row=r, column=c,sticky=stick)
                c=c+1
                if (c>5):
                        c=0
                        r=r+1
@retry(stop_max_attempt_number=3)
def signIn(base_url, w, mI, username, password):
	if (base_url==configLive["DEFAULT"]["PROD_BASE_URL"]):
		etrade = OAuth1Service(
        	name="etrade",
        	consumer_key=configLive["DEFAULT"]["CONSUMER_KEY"],
        	consumer_secret=configLive["DEFAULT"]["CONSUMER_SECRET"],
        	request_token_url="https://api.etrade.com/oauth/request_token",
        	access_token_url="https://api.etrade.com/oauth/access_token",
        	authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        	base_url="https://api.etrade.com")
		request_token, request_token_secret = etrade.get_request_token(params={"oauth_callback": "oob", "format": "json"})
                # Step 2: Go through the authentication flow. Login to E*TRADE.
                # After you login, the page will provide a text code to enter.
                authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
                browser = Firefox(options=opts)
        	browser.get(authorize_url)
        	usernameP = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "USER")))
        	passwordP = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "PASSWORD")))
        	logon = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.ID, "logon_button")))
        	usernameP.send_keys(username)
        	passwordP.send_keys(password)
        	logon.click()
        	acceptAgreement = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "submit")))
        	sleep(1)
		acceptAgreement.click()
		WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "api-footer")))
        	codeBox = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
        	code = codeBox.get_attribute('value')
        	browser.close()
                session = etrade.get_auth_session(request_token, request_token_secret, params={"oauth_verifier": code})
		return session
	elif (base_url==configSandbox["DEFAULT"]["SANDBOX_BASE_URL"]):
		etrade = OAuth1Service(
        	name="etrade",
        	consumer_key=configSandbox["DEFAULT"]["CONSUMER_KEY"],
        	consumer_secret=configSandbox["DEFAULT"]["CONSUMER_SECRET"],
        	request_token_url="https://api.etrade.com/oauth/request_token",
        	access_token_url="https://api.etrade.com/oauth/access_token",
        	authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        	base_url="https://api.etrade.com")
		request_token, request_token_secret = etrade.get_request_token(params={"oauth_callback": "oob", "format": "json"})
                # Step 2: Go through the authentication flow. Login to E*TRADE.
                # After you login, the page will provide a text code to enter.
                authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
                browser = Firefox(options=opts)
        	browser.get(authorize_url)
        	usernameP = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "USER")))
        	passwordP = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "PASSWORD")))
        	logon = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.ID, "logon_button")))
		sleep(1)
        	usernameP.send_keys(username)
        	passwordP.send_keys(password)
        	logon.click()
        	acceptAgreement = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "submit")))
        	sleep(1)
		acceptAgreement.click()
		WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "api-footer")))
        	codeBox = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
        	code = codeBox.get_attribute('value')
        	browser.close()
                session = etrade.get_auth_session(request_token, request_token_secret, params={"oauth_verifier": code})
		return session
	else:
		output(w, mI, "Error")
def getStockPrice(stock, base_url, session):
        # URL for the API endpoint
        url = base_url + "/v1/market/quote/" + stock + ".json"
        # Make API call for GET request
        response = session.get(url)
        logger.debug("Request Header: %s", response.request.headers)
	quoteData = []
        if response is not None and response.status_code == 200:
        	parsed = json.loads(response.text)
            	logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
            	# Handle and parse response
            	data = response.json()
		if data is not None and "QuoteResponse" in data and "QuoteData" in data["QuoteResponse"]:
                	for quote in data["QuoteResponse"]["QuoteData"]:
				if quote is not None and "All" in quote and "open" in quote["All"]:
                        		price = quote["All"]["open"]
				else:
					output(w, mI, "Error")
					price=0
		else:
			output(w, mI, "Error")
			price=0
	else:
		price=0
	return price
@timeout(15)
def getStockData(stock, open=0):
        stockObject = YahooFinancials(stock)
        sleep(0.1)
        try:
                stockPrice = stockObject.get_current_price()
        except yahoofinancials.ManagedException:
                stockPrice = 0
        sleep(0.1)
        if (open==0):
                stockInitialPrice = stockObject.get_open_price()
        else:
                stockInitialPrice = open
        if (stockInitialPrice is None or stockPrice is None):
                stockPriceChange = 0
        else:
                stockPriceChange = ((stockPrice-stockInitialPrice)/stockInitialPrice) * 100
        sleep(0.1)
        return stockPrice, stockPriceChange, stockInitialPrice
def trade(transaction, price, amount, day, date, quantity, x, budget, w, mI, account, base_url, commission, deviation, accountId, session, live, username, password, type="MARKET"):
	global balance, orderParameters
	order["client_order_id"] = random.randint(1000000000, 9999999999)
	if (type=="LIMIT"):
	        if (transaction=="buy"):
	                if (buy):
				order["price_type"] = type
				order["order_term"] = "GOOD_FOR_DAY"
				order["symbol"] = x
				order["order_action"] = "BUY"
				order["limit_price"] = price
				order["quantity"] = amount
				budget = float(budget) - (price*amount) - commission
				orderObject = Order.Order(session, account, base_url, accountId, live, username, password)
	                	orderObject.preview_order(w, mI, order)
	                else:
				order["price_type"] = type
	                        order["order_term"] = "GOOD_FOR_DAY"
	                        order["symbol"] = x
	                        order["order_action"] = "BUY"
	                        order["limit_price"] = price
	                        order["quantity"] = amount
				budget = float(budget) - (price*amount)
				orderObject = Order.Order(session, account, base_url, accountId, live, username, password)
	                	orderObject.preview_order(w, mI, order)
	                l = [date, 1, price, amount]
			if (deviation!=""):
				body = "Bought "+str(l[3])+" "+x+" for  "+str(l[2])+". Deviation "+str(deviation)+" disabled for buy"
			else:
				body = "Bought "+str(l[3])+" "+x+" for  "+str(l[2])
	                quantity = quantity+amount
			moneySpent = price*amount
	                ramble(w, mI, "\n\n"+body)
			sendText.sendMail("iotgearemail@gmail.com", "JimmyJohn", "4404136432@vtext.com", "Stock Purchase Update", 0, body)
	                return quantity, l, budget, moneySpent
	        elif (transaction=="sell"):
	                if (sell):
				order["price_type"] = type
	                        order["order_term"] = "GOOD_FOR_DAY"
	                        order["symbol"] = x
	                        order["order_action"] = "SELL"
	                        order["limit_price"] = price
	                        order["quantity"] = amount
				budget = float(budget) + (price*amount) - commission
	                        orderObject = Order.Order(session, account, base_url, accountId, live, username, password)
	                        orderObject.preview_order(w, mI, order)
	                else:
	                	order["price_type"] = type
	                        order["order_term"] = "GOOD_FOR_DAY"
	                        order["symbol"] = x
	                        order["order_action"] = "SELL"
	                        order["limit_price"] = price
	                        order["quantity"] = amount
				budget = float(budget) + (price*amount)
	                        orderObject = Order.Order(session, account, base_url, accountId, live, username, password)
	                        orderObject.preview_order(w, mI, order)
			l = [date, 0, price, amount]
			if (deviation!=""):
				body = "Sold "+str(l[3])+" "+x+" for  "+str(l[2])+". Deviation "+str(deviation)+" disabled for sell"
			else:
				body = "Sold "+str(l[3])+" "+x+" for  "+str(l[2])
	                quantity = quantity-amount
			profit = price*amount
	                ramble(w, mI, "\n\n"+body)
			sendText.sendMail("iotgearemail@gmail.com", "JimmyJohn", "4404136432@vtext.com", "Stock Purchase Update", 0, body)
	                return quantity, l, budget, profit
	        else:
	                output(w, mI, "Error")
	elif (type=="MARKET"):
		if (transaction=="buy"):
	                if (buy):
				order["price_type"] = type
				order["order_term"] = "GOOD_FOR_DAY"
				order["symbol"] = x
				order["order_action"] = "BUY"
				order["limit_price"] = None
				order["quantity"] = amount
				budget = float(budget) - (price*amount) - commission
				orderObject = Order.Order(session, account, base_url, accountId, live, username, password)
	                	orderObject.preview_order(w, mI, order)
	                else:
				order["price_type"] = type
	                        order["order_term"] = "GOOD_FOR_DAY"
	                        order["symbol"] = x
	                        order["order_action"] = "BUY"
	                        order["limit_price"] = None
	                        order["quantity"] = amount
				budget = float(budget) - (price*amount)
				orderObject = Order.Order(session, account, base_url, accountId, live, username, password)
	                	orderObject.preview_order(w, mI, order)
	                l = [date, 1, price, amount]
			if (deviation!=""):
				body = "Bought "+str(l[3])+" "+x+" for  "+str(l[2])+". Deviation "+str(deviation)+" disabled for buy"
			else:
				body = "Bought "+str(l[3])+" "+x+" for  "+str(l[2])
	                quantity = quantity+amount
			moneySpent = price*amount
	                ramble(w, mI, "\n\n"+body)
			sendText.sendMail("iotgearemail@gmail.com", "JimmyJohn", "4404136432@vtext.com", "Stock Purchase Update", 0, body)
	                return quantity, l, budget, moneySpent
	        elif (transaction=="sell"):
	                if (sell):
				order["price_type"] = type
	                        order["order_term"] = "GOOD_FOR_DAY"
	                        order["symbol"] = x
	                        order["order_action"] = "SELL"
	                        order["limit_price"] = None
	                        order["quantity"] = amount
				budget = float(budget) + (price*amount) - commission
	                        orderObject = Order.Order(session, account, base_url, accountId, live, username, password)
	                        orderObject.preview_order(w, mI, order)
	                else:
	                	order["price_type"] = type
	                        order["order_term"] = "GOOD_FOR_DAY"
	                        order["symbol"] = x
	                        order["order_action"] = "SELL"
	                        order["limit_price"] = None
	                        order["quantity"] = amount
				budget = float(budget) + (price*amount)
	                        orderObject = Order.Order(session, account, base_url, accountId, live, username, password)
	                        orderObject.preview_order(w, mI, order)
			l = [date, 0, price, amount]
			if (deviation!=""):
				body = "Sold "+str(l[3])+" "+x+" for  "+str(l[2])+". Deviation "+str(deviation)+" disabled for sell"
			else:
				body = "Sold "+str(l[3])+" "+x+" for  "+str(l[2])
	                quantity = quantity-amount
			profit = price*amount
	                ramble(w, mI, "\n\n"+body)
			sendText.sendMail("iotgearemail@gmail.com", "JimmyJohn", "4404136432@vtext.com", "Stock Purchase Update", 0, body)
	                return quantity, l, budget, profit
	        else:
	                output(w, mI, "Error")
def unionLists(l1, l2):
	return (list(set(l1) | set(l2)))
def compareLists(l1, l2):
	return (list(list(set(l1)-set(l2)) + list(set(l2)-set(l1))))
def intersectLists(l1, l2):
	return list(set(l1) & set(l2))
def totalProfit(table, set=False, stock=None, price=None):
	if (not set):
		cursor.execute("SELECT profit FROM "+table)
		profits = cursor.fetchall()
		floatProfits = []
		for e in range(len(profits)):
			floatProfits.append(float(profits[e][0]))
		totalProfit = sum(floatProfits)
		return totalProfit
	else:
		cursor.execute("SELECT profit FROM "+table+" WHERE stonks='"+stock+"'")
		profit = cursor.fetchall()[0][0]
		cursor.execute("SELECT quantity FROM "+table+" WHERE stonks='"+stock+"'")
		quantity = cursor.fetchall()[0][0]
		totalProfit = profit+(quantity*price)
		return totalProfit
def click(key, y, w, mI, account, base_url, etrade, session, y2, live, accountId, username, password):
	global killSwitch, table
	if (key==mainMenuItems[0]):
		y.destroy()
		algotMenu = AlgoTrade(w, mI, session, account, base_url, accountId, etrade, live, username, password)
		algotMenu.algoMenu()
	elif (key==mainMenuItems[1]):
		y.destroy()
		databaseMenu = database.Database(w, mI, session, base_url, etrade, live, username, password, account, accountId)
		databaseMenu.mainMenu()
	elif (key==mainMenuItems[2]):
		y.destroy()
		btnFrame = createFrame(w, 1, 0, 2, W)
		btns = createButtons(btnFrame, actualMainMenuItems, w, account, base_url, etrade, live, username, password, session, accountId, messageInterface=mI)
	elif (key==actualMainMenuItems[0]):
                y.destroy()
                market = market.Market(session, base_url, w, mI, etrade, live, username, password)
                market.quotes()
        elif (key==actualMainMenuItems[2]):
                y.destroy()
                numList = []
                listAccounts = accounts.Accounts(session, base_url, w, mI, etrade, live, username, password)
                listAccounts.account_list()
        elif (key==actualMainMenuItems[1]):
                y.destroy()
                algoAccount = accounts.Accounts(session, base_url, w, mI, etrade, live, username, password)
               	algoAccount.algoMainMenu()
        elif (key==actualMainMenuItems[3]):
                w.destroy()
                exit()
	elif (key==algoTradeItems[0]):
		output(w, mI, "Beginning AlgoTrading...")
                stonks = stocks.get()
                cashMoney = budget.get()
                if (cashMoney==""):
                        cursor.execute("SELECT longbudget FROM "+str(tBudget))
                        cashMoney = float(cursor.fetchall()[0][0])
                else:
                        cashMoney = float(cashMoney)
                        cursor.execute("UPDATE "+str(tBudget)+" SET longbudget="+str(cashMoney))
                        mydb.commit()
                y.destroy()
                y2.destroy()
                stockList = stonks.split(",")
		killSwitch=False
		algorithmicTrader = AlgoTrade(w, mI, session, account, base_url, accountId, etrade, live, username, password)
		algorithmicTrader.longAlgotrading(stockList, cashMoney)
	elif (key==algoTradeItems[1]):
		output(w, mI, "Beginning AlgoTrading...")
                stonks = stocks.get()
                cashMoney = budget.get()
                if (cashMoney==""):
                        cursor.execute("SELECT daybudget FROM "+str(tBudget))
                        cashMoney = float(cursor.fetchall()[0][0])
                else:
                        cashMoney = float(cashMoney)
                        cursor.execute("UPDATE "+str(tBudget)+" SET daybudget="+str(cashMoney))
                        mydb.commit()
		if (stonks=="" and scannerTime(datetime.datetime.now())):
			stockList = stockScanner.screener()
		elif (stonks!=""):
			 stockList = stonks.split(",")
		else:
			stockList = []
                y.destroy()
                y2.destroy()
		killSwitch=False
		algorithmicTrader = AlgoTrade(w, mI, session, account, base_url, accountId, etrade, live, username, password)
		algorithmicTrader.dayAlgotrading(stockList, cashMoney)
	elif (key==algoTradeItems[2]):
		y.destroy()
		y2.destroy()
		algotMenu = AlgoTrade(w, mI, session, account, base_url, accountId, etrade, live, username, password)
		algotMenu.mainMenu()
	elif (key==algoingOptions[0]):
                killSwitch=True
                y.destroy()
                algotMenu = AlgoTrade(w, mI, session, account, base_url, accountId, etrade, live, username, password)
                algotMenu.algoMenu()
        elif (key==algoingOptions[1]):
                cursor.execute("SELECT ID FROM "+table)
                sks = cursor.fetchall()
                for i in range(len(sks)):
                        command = "UPDATE "+table+" SET bd1=0, bd2=0, bd3=0, bd4=0, bd5=0, bd6=0, bd7=0, bd8=0, bd9=0, bd10=0, sd10=0, sd9=0, sd8=0, sd7=0, sd6=0, sd5=0, sd4=0, sd3=0, sd2=0, sd1=0 WHERE ID = %s"
                        value = (sks[i])
                        cursor.execute(command, value)
                mydb.commit()
                ramble(w, mI, "\n\nDeviations Reset")
	else:
		output("Error")
class AlgoTrade:
	def __init__(self, w, mI, session, account, base_url, accountId, etrade, live, username, password):
		global table, tBudget
		self.accountId = accountId
		table = "t"+str(accountId)
		tBudget = "b"+str(accountId)
        	self.session = session
        	self.account = account
        	self.base_url = base_url
		self.live = live
		self.etrade = etrade
		self.w = w
		self.mI = mI
		self.username = username
		self.password = password
	def mainMenu(self):
		buttonFrame = createFrame(self.w, 1, 0, 2, W)
		btns = createButtons(buttonFrame, mainMenuItems, self.w, self.account, self.base_url, self.etrade, self.live, self.username, self.password, self.session, self.accountId, messageInterface=self.mI)
	@retry(stop_max_attempt_number=3)
	def longAlgotrading(self, stockList, budget):
		global killSwitch, g, mydb, cursor
		btnFrame = createFrame(self.w, 1, 0, 2, W)
		btns = createButtons(btnFrame, algoingOptions, self.w, self.account, self.base_url, self.etrade, self.live, self.username, self.password, self.session, self.accountId, messageInterface=self.mI)
		currentDate = datetime.date.now()
		monthsAgo = datetime.datetime.now() - datetime.timedelta(months=3)
		yearAgo = datetime.datetime.now() - datetime.timedelta(years=1)
		x1 =  int(currentDate.strftime("%Y"))
		y1 =  int(currentDate.strftime("%m"))
		z1 =  int(currentDate.strftime("%d"))

		x2 = int(monthsAgo.strftime("%Y"))
		y2 = int(monthsAgo.strftime("%m"))
		z2 = int(monthsAgo.strftime("%d"))

		x3 = int(yearAgo.strftime("%Y"))
		y3 = int(yearAgo.strftime("%m"))
		z3 = int(yearAgo.strftime("%d"))
		sNumber = len(stockList)
		for i in range(sNumber):
			stockData.append(q.Quote(stockList[i]))
		accountBalance = accounts.Accounts(self.session, self.base_url, self.w, self.mI, self.etrade, self.live, self.username, self.password)
		balance = accountBalance.getBalance(self.account, self.w, self.mI)
		if (budget > balance):
			output(self.w, self.mI, "Error: Insufficient Funds Inputted")
			sleep(1)
		        killSwitch=True
		cursor.execute("SELECT stonks FROM "+table)
		stonks = cursor.fetchall()
		stunks = []
		for xi in range(len(stonks)):
			stunks.append(str(stonks[xi][0]))
		if (len(stunks)==0):
			for i in range(sNumber):
				command = "INSERT INTO "+table+" (id, stonks, quantity, profit, bd1, bd2, bd3, bd4, bd5, bd6, bd7, bd8, bd9, bd10, sd1, sd2, sd3, sd4, sd5, sd6, sd7, sd8, sd9, sd10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				values = (i, stockList[i], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
				cursor.execute(command, values)
			mydb.commit()
		else:
			totalList = unionLists(stunks, stockList)
			if (len(totalList)>len(stunks)):
				difference = compareLists(stunks, totalList)
				cursor.execute("SELECT id FROM "+table)
				id = cursor.fetchall()
				ids = []
				for y in range(len(id)):
					ids.append(id[y][0])
				ids.sort()
				startID = int(ids[-1])
				for i in range(len(difference)):
					startID = startID+1
					command = "INSERT INTO "+table+" (id, stonks, quantity, profit, bd1, bd2, bd3, bd4, bd5, bd6, bd7, bd8, bd9, bd10, sd1, sd2, sd3, sd4, sd5, sd6, sd7, sd8, sd9, sd10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					values = (startID, str(difference[i]), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
					cursor.execute(command, values)
				mydb.commit()
		qu = []
		for e in range(sNumber):
			cursor.execute("SELECT quantity FROM " +table+" WHERE stonks = '"+stockList[e]+"'")
			qu.append(cursor.fetchall()[0][0])
		for i in range(sNumber):
			quantity.append(qu[i])
		while True:
			if (killSwitch):
				output(self.w, self.mI, "AlgoTrading Stopped")
				break
			if  (afterHours(datetime.datetime.now()) or afterTime(datetime.datetime.now())):
				sendText.sendMail("iotgearemail@gmail.com", "JimmyJohn", "4404136432@vtext.com", "AlgoTrader Update", 0, "AlgoTrading Stopped: Outside of market hours")
				cursor.execute("SELECT ID FROM "+table)
				sks = cursor.fetchall()
				for i in range(len(sks)):
					command = "UPDATE "+table+" SET bd1=0, bd2=0, bd3=0, bd4=0, bd5=0, bd6=0, bd7=0, bd8=0, bd9=0, bd10=0, sd1=0, sd2=0, sd3=0, sd4=0, sd5=0, sd6=0, sd7=0, sd8=0, sd9=0, sd10=0 WHERE ID = %s"
					value = (sks[i])
					cursor.execute(command, value)
				mydb.commit()
				while True:
					output(self.w, self.mI, "Unable to trade: outside of market hours")
					if (not afterHours(datetime.datetime.now()) and not afterTime(datetime.datetime.now())):
						output(self.w, self.mI, "Relogging in...")
						self.session=""
						while (self.session==""):
							try:
								self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
							except:
								sleep(5)
								self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
						sqlValues = sqlLog()
						mydb = sqlValues[0]
						cursor = sqlValues[1]
						sendText.sendMail("iotgearemail@gmail.com", "JimmyJohn", "4404136432@vtext.com", "AlgoTrader Update", 0, "AlgoTrading Started: Market Trading has begun")
						output(self.w, self.mI, "AlgoTrading Started")
						sleep(1)
						break
					elif (killSwitch):
						self.session=""
						while (self.session==""):
							try:
								self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
							except:
								sleep(5)
								self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
						sqlValues = sqlLog()
						mydb = sqlValues[0]
						cursor = sqlValues[1]
						break
					for h in range(1800):
						sleep(1)
						ramble(self.w, self.mI, "")
						if (killSwitch):
							break
			else:
				shortAverages = []
		        	longAverages = []
		        	lastPrices = []
		        	prices = []
		        	for i in range(sNumber):
		                	shortAverage = historicalMovingAverage(start=str(x2)+"-"+str(y2)+"-"+str(z2), stop=str(x1)+"-"+str(y1)+"-"+str(z1), x=i)
		                	sleep(0.1)
		                	longAverage = historicalMovingAverage(start=str(x3)+"-"+str(y3)+"-"+str(z3), stop=str(x1)+"-"+str(y1)+"-"+str(z1), x=i)
		                	price = getStockPrice(stockList[i], self.base_url, self.session)
		               		shortAverages.append(shortAverage)
		                	longAverages.append(longAverage)
		                	prices.append(price)
				output(self.w, self.mI, "")
				for i in range(sNumber):
		                	ramble(self.w, self.mI, "\n\n"+stockList[i])
		                	ramble(self.w, self.mI, "\n3 Month Moving Average: " + str(shortAverages[i]))
		                	ramble(self.w, self.mI, "\n1 Year Moving Average: " + str(longAverages[i]))
		                	ramble(self.w, self.mI, "\nStock Price: " + str(prices[i]))
					if ((prices[i]/shortAverages[i])>1):
						devan = prices[i]/shortAverages[i]
						ramble(self.w, self.mI, "\nPositive Deviance: " + str(devan))
					elif ((prices[i]/shortAverages[i])<1):
						devan = prices[i]/shortAverages[i]
		                                ramble(self.w, self.mI, "\nNegative Deviance: " + str(devan))
					else:
						ramble(self.w, self.mI, "\nNeutral Deviance: 1")
		                	ramble(self.w, self.mI, "\nQuantity: " + str(quantity[i]))
		        	ramble(self.w, self.mI, "\n\nGENERAL DATA\n")
		        	ramble(self.w, self.mI, "\nBudget: " +str(budget))
				#ramble(self.w, self.mI, "\nTotal Profit: "+str(totalProfit(table)))
		        	ramble(self.w, self.mI, "\nDate: " + (str(x1)+"-"+str(y1)+"-"+str(z1)))
		        	#check which stock to trade
		        	growths = []
		        	for i in range(sNumber):
		                	growth = (prices[i]-shortAverages[i])/shortAverages[i]*100
		                	growths.append(growth)
		        	sellStockList = sorted(growths)
		        	buyStockList = sorted(growths, reverse=True)
		        	sellStock = max(growths)
		        	buyStock = min(growths)
				selector = 1
				selector2 = 1
				loop = True
				loop2 = True
				if (len(growths)>1):
                        		for r in range(len(growths)):
                                        	if (sellStock==growths[r] and sellStock>0 and quantity[i]>0):
                                                	loop=False
                                                	break
						elif (sellStock==growths[r] and (quantity[r]<=0 or sellStock<0)):
							sellStock = sellStockList[selector]
							selector = selector + 1
                        		for e in range(len(growths)):
                                        	if (buyStock==growths[e] and buyStock<0 and budget>prices[e]+commission):
                                                	loop2=False
                                                	break
						elif (buyStock==growths[e] and (budget<prices[e]+commission or buyStock>0)):
							buyStock = buyStockList[selector2]
							selector2 = selector2 + 1
				if (loop):
					sellStock = max(growths)
				if (loop2):
					buyStock = min(growths)
		        	counter = 0
				counter2 = 0
				for i in range(sNumber):
		                	if (sellStock == growths[i] and sellStock>0 and shortAverages[i]>longAverages[i]):
						cursor.execute("SELECT sd10, sd9, sd8, sd7, sd6, sd5, sd4, sd3, sd2, sd1 FROM "+table +" WHERE stonks = '"+stockList[i]+"'")
						dev = cursor.fetchall()[0]
						for e in range(g):
							if (prices[i]==0 or len(dev)<10):
								break
							deviation = dev[e]
							if (quantity[i]>=AP[e][0] and prices[i]>shortAverages[i]*AP[e][1] and AP[e][0]*prices[i]>commission and deviation==0):
								tradeInfo = trade("sell", prices[i], AP[e][0], day, str(datetime.datetime.now().strftime("%Y"))+"-"+str(datetime.datetime.now().strftime("%m"))+"-"+str(datetime.datetime.now().strftime("%d")), quantity[i], stockList[i], budget, self.w, self.mI, self.account, self.base_url, commission, AP[e][1], self.accountId, self.session, self.live, self.username, self.password)
								quantity[i] = tradeInfo[0]
								budget = tradeInfo[2]
								#profit = totalProfit(table, set=True, stock=stockList[i], price=prices[i]) +tradeInfo[3]
								cursor.execute("UPDATE "+table+" SET "+sD[e]+" = 1 WHERE stonks = '" +stockList[i]+ "'")
								cursor.execute("UPDATE "+table+" SET quantity = "+str(quantity[i])+" WHERE stonks = '" +stockList[i]+ "'")
								#cursor.execute("UPDATE "+table+" SET profit = "+str(profit)+" WHERE stonks='"+stockList[i]+"'")
								cursor.execute("UPDATE "+tBudget+" SET longbudget = " + str(budget))
								mydb.commit()
								break
		                        		else:
								counter2 = counter2 + 1
						if (counter2==g):
		                                	ramble(self.w, self.mI, "\n\nCan't Preform Sell("+str(stockList[i])+")")
		                	else:
		                        	counter = counter + 1
		        	if (counter==sNumber):
		                	ramble(self.w, self.mI, "\n\nSell Wait")
		        	counter = 0
				counter2 = 0
				for i in range(sNumber):
		                	if (buyStock == growths[i] and buyStock<0 and shortAverages[i]<longAverages[i]):
						cursor.execute("SELECT bd10, bd9, bd8, bd7, bd6, bd5, bd4, bd3, bd2, bd1 FROM "+table+" WHERE stonks = '"+stockList[i]+"'")
						dev = cursor.fetchall()[0]
						for e in range(g):
							if (prices[i]==0 or len(dev)<10):
								break
							deviation = dev[e]
							if (prices[i]*AP[e][0]+commission<=budget and prices[i]*AP[e][1]<shortAverages[i] and deviation==0):
								t = trade("buy", prices[i], AP[e][0], day, str(datetime.datetime.now().strftime("%Y"))+"-"+str(datetime.datetime.now().strftime("%m"))+"-"+str(datetime.datetime.now().strftime("%d")), quantity[i], stockList[i], budget, self.w, self.mI, self.account, self.base_url, commission, AP[e][1], self.accountId, self.session, self.live, self.username, self.password)
								quantity[i] = t[0]
								budget = t[2]
								#profit = totalProfit(table, set=True, stock=stockList[i], price=prices[i]) + t[3]
								cursor.execute("UPDATE "+table+" SET "+bD[e]+" = 1 WHERE stonks = '" +stockList[i]+ "'")
								cursor.execute("UPDATE "+table+" SET quantity = "+str(quantity[i])+" WHERE stonks = '" +stockList[i]+ "'")
								#cursor.execute("UPDATE "+table+" SET profit = "+str(profit)+" WHERE stonks='"+stockList[i]+"'")
								cursor.execute("UPDATE "+tBudget+" SET longbudget = " + str(budget))
								mydb.commit()
		                        		else:
								counter2 = counter2 + 1
		                                if (counter2==g):
							ramble(self.w, self.mI, "\n\nCan't Preform Buy("+str(stockList[i])+")")
		                	else:
		                        	counter = counter + 1
		        	if (counter==sNumber):
		                	ramble(self.w, self.mI, "\n\nBuy Wait")
				for i in range(60):
					ramble(self.w, self.mI, "")
					sleep(1)
					if (killSwitch):
						break
	def dayAlgotrading(self, stockList, budget):
		global killSwitch, g, mydb, cursor
		btnFrame = createFrame(self.w, 1, 0, 2, W)
		btns = createButtons(btnFrame, algoingOptions, self.w, self.account, self.base_url, self.etrade, self.live, self.username, self.password, self.session, self.accountId, messageInterface=self.mI)
		tradeCooldown = False
		scannerComplete = False
		sNumber = 0
		accountBalance = accounts.Accounts(self.session, self.base_url, self.w, self.mI, self.etrade, self.live, self.username, self.password)
		balance = accountBalance.getBalance(self.account, self.w, self.mI)
		balance = 1000
		startingBudget = budget
		day=0
		if (budget > balance):
			output(self.w, self.mI, "Error: Insufficient Funds Inputted")
			sleep(1)
		        killSwitch=True
		#if (killSwitch):
		while True:
			if (killSwitch):
				output(self.w, self.mI, "AlgoTrading Stopped")
				self.session=""
				while (self.session==""):
					try:
						self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
					except:
						sleep(5)
						self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
				sqlValues = sqlLog()
				mydb = sqlValues[0]
				cursor = sqlValues[1]
				break
			elif (tradeCooldown):
				ramble(self.w, self.mI, "Day Trading Complete: waiting for market to close")
				scannerComplete=False
				while True:
					if (killSwitch):
						self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
						sqlValues = sqlLog()
						mydb = sqlValues[0]
						cursor = sqlValues[1]
						break
					if (afterHours(datetime.datetime.now()) or afterTime(datetime.datetime.now()) or day>1):
						tradeCooldown=False
						day=0
						break
					for wait in range(900):
						sleep(1)
						if (killSwitch):
							break
			elif (scannerTime(datetime.datetime.now()) and not afterHours(datetime.datetime.now())):
				output(self.w, self.mI, "Scanner Started")
	                        try:
	                                stockList = stockScanner.screener()
	                        except KeyboardInterrupt:
	                                exit(1)
	                        sleep(10)
				sNumber = len(stockList)
	                        scannerComplete = True
				sqlValues = sqlLog()
                                mydb = sqlValues[0]
                                cursor = sqlValues[1]
				cursor.execute("SELECT stonks FROM "+table)
				stonks = cursor.fetchall()
				stunks = []
				initialPrices = []
				for xi in range(len(stonks)):
					stunks.append(str(stonks[xi][0]))
				if (len(stunks)==0):
					for i in range(sNumber):
						command = "INSERT INTO "+table+" (id, stonks, quantity, profit, bd1, bd2, bd3, bd4, bd5, bd6, bd7, bd8, bd9, bd10, sd1, sd2, sd3, sd4, sd5, sd6, sd7, sd8, sd9, sd10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
						values = (i, stockList[i], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
						cursor.execute(command, values)
					mydb.commit()
				else:
					totalList = unionLists(stunks, stockList)
					if (len(totalList)>len(stunks)):
						difference = compareLists(stunks, totalList)
						cursor.execute("SELECT id FROM "+table)
						id = cursor.fetchall()
						ids = []
						for y in range(len(id)):
							ids.append(id[y][0])
						ids.sort()
						startID = int(ids[-1])
						for i in range(len(difference)):
							startID = startID+1
							command = "INSERT INTO "+table+" (id, stonks, quantity, profit, bd1, bd2, bd3, bd4, bd5, bd6, bd7, bd8, bd9, bd10, sd1, sd2, sd3, sd4, sd5, sd6, sd7, sd8, sd9, sd10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
							values = (startID, str(difference[i]), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
							cursor.execute(command, values)
						mydb.commit()
	                        output(self.w, self.mI, "Scanner Complete\nChosen stocks for trading: "+str(stockList))
	                        ramble(self.w, self.mI, "\nWaiting For Market To Open Or Reopen")
	                        while True:
	                                if (not afterTime(datetime.datetime.now()) and not afterHours(datetime.datetime.now())):
	                                        tradeCooldown = False
						output(self.w, self.mI, "Relogging in...")
						self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
						sqlValues = sqlLog()
						mydb = sqlValues[0]
						cursor = sqlValues[1]
	                                        break
	                                elif (killSwitch):
						self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
						sqlValues = sqlLog()
						mydb = sqlValues[0]
						cursor = sqlValues[1]
	                                        break
	                                elif (afterHours(datetime.datetime.now())):
	                                        for wait in range(3600):
	                                                sleep(1)
	                                                if (killSwitch):
	                                                        break
	                                else:
	                                        for wait in range(180):
	                                                sleep(1)
	                                                if (killSwitch):
	                                                        break
	                                if (killSwitch):
	                                        break
			elif  (afterHours(datetime.datetime.now()) or afterTime(datetime.datetime.now())):
				output(self.w, self.mI, "Unable to trade: outside of market hours")
				scannerComplete = False
				while True:
					if (not afterHours(datetime.datetime.now()) and not afterTime(datetime.datetime.now()) and day>2):
						output(self.w, self.mI, "Relogging in...")
		                                self.session=""
						day=0
						while (self.session==""):
							try:
								self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
							except:
								sleep(5)
								self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
						sqlValues = sqlLog()
						mydb = sqlValues[0]
						cursor = sqlValues[1]
						break
					elif (scannerTime(datetime.datetime.now()) and not afterHours(datetime.datetime.now()) and day>2):
						day=0
						break
					if (killSwitch):
						self.session = signIn(self.base_url, self.w, self.mI, self.username, self.password)
						sqlValues = sqlLog()
						mydb = sqlValues[0]
						cursor = sqlValues[1]
						break
					for h in range(180):
						sleep(1)
						ramble(self.w, self.mI, "")
						if (killSwitch):
							break
			else:
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
	                                        tradeCooldown=True
	                                        continue
				if (stockList==[]):
		                        tradeCooldown = True
					continue
                                output(self.w, self.mI, "AlgoTrading Started")
                               	for yote in range(60):
					sleep(1)
					if (killSwitch):
						break
				tradeList = []
	                        quantity = []
	                        initialPrices = []
	                        sNumber = 0
	                        interruptor = 0
	                        listLoop=0
				while (sNumber==0):
	                                if (listLoop>2):
	                                        listLoop=0
	                                        output(self.w, self.mI, "Stocks in list are not increasing in value")
	                                for stock in stockList:
	                                        try:
	                                                interruptor=0
	                                                totalChange=-100
	                                                while True:
								if (killSwitch):
									break
	                                                        try:
	                                                                totalChange = getStockData(stock)[1]
	                                                        except timeout_decorator.timeout_decorator.TimeoutError:
	                                                                interruptor+=1
	                                                                if (interruptor>2):
	                                                                        interruptor=0
	                                                                        break
	                                                                else:
	                                                                        continue
	                                                        break
	                                                if (totalChange<0):
	                                                        interruptor=0
	                                                        continue
	                                                else:
	                                                        ramble(self.w, self.mI, str(stock)+" added to trade list")
	                                                        tradeList.append(stock)
	                                                        quantity.append(0)
	                                                        interruptor=0
	                                        except ValueError:
	                                                continue
	                                sNumber = len(tradeList)
	                                listLoop+=1
					for yeet in range(5):
						sleep(1)
						if (killSwitch):
							break
				totalCommission = sNumber*commission*2
	                        investMoney = budget-(totalCommission/2)
	                        moneyPerStock = math.floor(investMoney/sNumber)
	                        c = 0
	                        highGain = 0
	                        interruptor = 0
	                        for stock in tradeList:
	                                buyPrice=None
	                                while True:
						if (killSwitch):
							break
	                                        try:
	                                                buyPrice = getStockData(stock)[0]
	                                        except timeout_decorator.timeout_decorator.TimeoutError:
	                                                interruptor+=1
	                                                if (interruptor>2):
	                                                        interruptor=0
	                                                        break
	                                                else:
	                                                        continue
	                                        break
					if (killSwitch):
						break
	                                interruptor=0
	                                if (buyPrice is None):
	                                        tradeList.remove(stock)
	                                        quantity.pop(c)
	                                        sNumber = len(tradeList)
						totalCommission = sNumber*commission*2
	                                        continue
	                                else:
	                                        amount = math.floor(moneyPerStock/buyPrice)
						t = trade("buy", buyPrice, amount, day, str(datetime.datetime.now().strftime("%Y"))+"-"+str(datetime.datetime.now().strftime("%m"))+"-"+str(datetime.datetime.now().strftime("%d")), quantity[c], stockList[c], budget, self.w, self.mI, self.account, self.base_url, commission, "", self.accountId, self.session, self.live, self.username, self.password, type="MARKET")
						#profit = totalProfit(table, set=True, stock=stockList[c], price=buyPrice) + t[3]
						cursor.execute("UPDATE "+table+" SET quantity = "+str(quantity[c])+" WHERE stonks = '" +stockList[c]+ "'")
						#cursor.execute("UPDATE "+table+" SET profit = "+str(profit)+" WHERE stonks='"+stockList[c]+"'")
						cursor.execute("UPDATE "+tBudget+" SET daybudget = " + str(budget))
						mydb.commit()
	                                        quantity[c] = t[0]
						budget = t[2]
	                                        initialPrices.append(buyPrice)
	                                c+=1
	                        moneyLeft = budget
	                        moneyInvested = 0
				for i in range(len(quantity)):
					moneyInvest+=(quantity[i]*initialPrices[i])
				output(self.w, self.mI, "")
				while True:
					prices = []
	                                openPrices = []
	                                indivisualGain = []
	                                totalChanges = []
	                                i = 0
	                                interruptor = 0
	                                if (sNumber==0 or tradeCooldown or killSwitch):
	                                        break
	                                for stock in tradeList:
	                                        stockData=0
						stockPrice = 0
						if (killSwitch):
							break
	                                        while True:
	                                                try:
								if (killSwitch):
									break
	                                                        stockData = getStockData(stock, initialPrices[i])
								stockPrice = getStockPrice(stock, self.base_url, self.session)
	                                                except timeout_decorator.timeout_decorator.TimeoutError:
	                                                        interruptor+=1
	                                                        if (interruptor>2):
	                                                                interruptor=0
	                                                                break
	                                                        else:
	                                                                continue
	                                                break
	                                        if (stockData==0 or stockPrice==0):
	                                                continue
						interruptor=0
						stockPrice = stockData[0]
	                                        openPrice = stockData[2]
	                                        totalChange = stockData[1]
	                                        iG = stockPrice*quantity[i]
	                                        prices.append(stockPrice)
	                                        openPrices.append(openPrice)
	                                        indivisualGain.append(iG)
	                                        totalChanges.append(totalChange)
	                                        output(self.w, self.mI, str(stock))
	                                        ramble(self.w, self.mI, "\nStock Price: $"+str(stockPrice))
	                                        ramble(self.w, self.mI, "\nOpen Price: $"+str(openPrice))
	                                        ramble(self.w, self.mI, "\nRealized Stock Change: "+str(totalChange)+"%")
						ramble(self.w, self.mI, "\nQuantity: "+str(quantity[i]))
	                                        ramble(self.w, self.mI, "\n"+str(i+1)+"/"+str(len(tradeList)))
	                                        i+=1
	                                netGain = sum(indivisualGain)
	                                realizedChange = (((netGain+moneyLeft-totalCommission)-startingBudget)/startingBudget)*100
	                                if (realizedChange>highGain):
	                                        highGain = realizedChange
	                                if (highGain!=0):
	                                        percentDrop = realizedChange-highGain
	                                else:
	                                        percentDrop = 0
	                                hour = int(datetime.datetime.now().strftime("%H"))
	                                minute = int(datetime.datetime.now().strftime("%M"))
	                                v = 0
					for stock in tradeList:
						if (killSwitch):
							break
	                                        if (totalChanges[v]<-3 and not tradeCooldown):
							t = trade("sell", prices[v], quantity[v], day, str(datetime.datetime.now().strftime("%Y"))+"-"+str(datetime.datetime.now().strftime("%m"))+"-"+str(datetime.datetime.now().strftime("%d")), quantity[v], stockList[v], budget, self.w, self.mI, self.account, self.base_url, commission, "", self.accountId, self.session, self.live, self.username, self.password, type="MARKET")
							quantity[v] = t[0]
							budget = t[2]
							#profit = totalProfit(table, set=True, stock=stockList[v], price=prices[v]) + t[3]
							cursor.execute("UPDATE "+table+" SET quantity = "+str(quantity[v])+" WHERE stonks = '" +stockList[v]+ "'")
							#cursor.execute("UPDATE "+table+" SET profit = "+str(profit)+" WHERE stonks='"+stockList[v]+"'")
							cursor.execute("UPDATE "+tBudget+" SET daybudget = " + str(budget))
							mydb.commit()
	                                                tradeList.remove(stock)
	                                                quantity.pop(v)
	                                                initialPrices.pop(v)
	                                                sNumber = len(tradeList)
	                                                if (sNumber==0):
	                                                        tradeCooldown=True
								day+=1
								ramble(self.w, self.mI, "\nStarting Budget: $"+str(startingBudget))
								ramble(self.w, self.mI, "\nEnd Budget: $"+str(budget))
								startingBudget = budget
	                                                        break
							else:
	                                                        tempCommission = sNumber*commission*2
	                                                        investMoney = budget-(tempCommission/2)
	                                                        moneyPerStock = math.floor(budget/sNumber)
								totalCommission+=(tempCommission/2)
	                                                        c = 0
	                                                        interruptor = 0
	                                                        for stock in tradeList:
	                                                                buyPrice=None
									if (killSwitch):
										break
	                                                                while True:
										if (killSwitch):
											break
	                                                                        try:
	                                                                                buyPrice = getStockData(stockList[c], initialPrices[c])[0]
	                                                                        except timeout_decorator.timeout_decorator.TimeoutError:
	                                                                                interruptor+=1
	                                                                                if (interruptor>2):
	                                                                                        interruptor=0
	                                                                                        break
	                                                                                else:
	                                                                                        continue
	                                                                        break
	                                                                interruptor=0
	                                                                if (buyPrice is None):
	                                                                        tradeList.remove(stock)
	                                                                        quantity.pop(c)
	                                                                        sNumber = len(tradeList)
										totalCommission-=commission
	                                                                        continue
	                                                                else:
	                                                                        amount = math.floor(moneyPerStock/buyPrice)
			                                                        t = trade("buy", prices[c], quantity[c], day, str(datetime.datetime.now().strftime("%Y"))+"-"+str(datetime.datetime.now().strftime("%m"))+"-"+str(datetime.datetime.now().strftime("%d")), quantity[c], stockList[c], budget, self.w, self.mI, self.account, self.base_url, commission, "", self.accountId, self.session, self.live, self.username, self.password, type="MARKET")
										quantity[c] = t[0]
										budget = t[2]
										#profit = totalProfit(table, set=True, stock=stockList[i], price=prices[i]) + t[3]
										cursor.execute("UPDATE "+table+" SET quantity = "+str(quantity[c])+" WHERE stonks = '" +stockList[c]+ "'")
										#cursor.execute("UPDATE "+table+" SET profit = "+str(profit)+" WHERE stonks='"+stockList[c]+"'")
										cursor.execute("UPDATE "+tBudget+" SET daybudget = " + str(budget))
										mydb.commit()
	                                                                        initialPrices[c] = (initialPrices[c]*quantity[c]+buyPrice*amount)/prices[c]
	                                                                c+=1
	                                                        moneyLeft = budget
								moneyInvested=0
	                                                        for i in range(len(quantity)):
									moneyInvested+=(quantity[i]*initialPrices[i])
	                                        v+=1
	                                if (realizedChange>1 and percentDrop<=-1 and percentDrop>-3  and not tradeCooldown):
	                                        n=0
	                                        for stock in tradeList:
							t = trade("sell", prices[n], quantity[n], day, str(datetime.datetime.now().strftime("%Y"))+"-"+str(datetime.datetime.now().strftime("%m"))+"-"+str(datetime.datetime.now().strftime("%d")), quantity[n], stockList[n], budget, self.w, self.mI, self.account, self.base_url, commission, "", self.accountId, self.session, self.live, self.username, self.password, type="MARKET")
							quantity[n] = t[0]
							budget = t[2]
							#profit = totalProfit(table, set=True, stock=stockList[n], price=prices[n]) + t[3]
							cursor.execute("UPDATE "+table+" SET quantity = "+str(quantity[n])+" WHERE stonks = '" +stockList[n]+ "'")
							#cursor.execute("UPDATE "+table+" SET profit = "+str(profit)+" WHERE stonks='"+stockList[n]+"'")
							cursor.execute("UPDATE "+tBudget+" SET daybudget = " + str(budget))
							mydb.commit()
	                                                n+=1
	                                        tradeCooldown = True
						day+=1
						ramble(self.w, self.mI, "\nStarting Budget: $"+str(startingBudget))
						ramble(self.w, self.mI, "\nEnd Budget: $"+str(budget))
						startingBudget = budget
						#sendText.sendMail()
	                                        break
					if (afterTime(datetime.datetime.now()) or afterHours(datetime.datetime.now())):
	                                        f=0
	                                        for stock in tradeList:
	                                                t = trade("sell", prices[f], quantity[f], day, str(datetime.datetime.now().strftime("%Y"))+"-"+str(datetime.datetime.now().strftime("%m"))+"-"+str(datetime.datetime.now().strftime("%d")), quantity[f], stockList[f], budget, self.w, self.mI, self.account, self.base_url, commission, "", self.accountId, self.session, self.live, self.username, self.password, type="MARKET")
							quantity[f] = t[0]
							budget = t[2]
							#profit = totalProfit(table, set=True, stock=stockList[f], price=prices[f]) + t[3]
							cursor.execute("UPDATE "+table+" SET quantity = "+str(quantity[f])+" WHERE stonks = '" +stockList[f]+ "'")
							#cursor.execute("UPDATE "+table+" SET profit = "+str(profit)+" WHERE stonks='"+stockList[f]+"'")
							cursor.execute("UPDATE "+tBudget+" SET daybudget = " + str(budget))
							mydb.commit()
	                                                f+=1
	                                        tradeCooldown = True
						day+=1
						ramble(self.w, self.mI, "\nStarting Budget: $"+str(startingBudget))
						ramble(self.w, self.mI, "\nEnd Budget: $"+str(budget))
						startingBudget = budget
						#sendText.sendMail()
	                                        break
			        	ramble(self.w, self.mI, "\n\nGENERAL DATA\n")
					ramble(self.w, self.mI, "\nTotal Realized Gain: "+str(realizedChange)+"%")
	                                ramble(self.w, self.mI, "\n% Drop: %"+str(percentDrop))
	                                ramble(self.w, self.mI, "\nCommission: $"+str(sNumber*commission*2))
			        	ramble(self.w, self.mI, "\nBudget: " +str(budget))
					#ramble(self.w, self.mI, "\nTotal Profit: "+str(totalProfit(table)))
			        	ramble(self.w, self.mI, "\nDate: " + str(datetime.datetime.now().strftime("%m"))+"-"+str(datetime.datetime.now().strftime("%d"))+"-"+str(datetime.datetime.now().strftime("%Y")))
			        	sleep(1)
	def algoMenu(self, day=False):
		global stocks, budget
		"""
		Provides the different options for preview orders: select new order or select from previous order

		:param session: authenticated session
		:param account: information on selected account
		:param prev_orders: list of instruments from previous orders
		"""
		#y.destroy()
		inputFrame = createFrame(self.w, 1, 0, 2, W)
		stocks = Entry(inputFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
		stocks.grid(row=0, column=1, sticky=N)
		stockLabel = Label(inputFrame, width=labelWidth, height=1, text="Stocks").grid(row=0, column=0, stick=W)
		budget = Entry(inputFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
		budget.grid(row=1, column=1, sticky=N)
		budgetLabel = Label(inputFrame, width=labelWidth, height=1, text="Budget").grid(row=1, column=0, sticky=W)
		buttonFrame = createFrame(self.w, 2, 0, 2, W)
		btns = createButtons(buttonFrame, algoTradeItems, self.w, self.account, self.base_url, self.etrade, self.live, self.username, self.password, self.session, self.accountId, messageInterface=self.mI, y2=inputFrame)
		b = accounts.Accounts(self.session, self.base_url, self.w, self.mI, self.etrade, self.live, self.username, self.password)
		balance = b.balance(self.account, self.w, self.mI)
		output(self.w, self.mI, "Enter stocks you want to trade seperated by commas with no spaces, then enter your budget and begin algo trading")
