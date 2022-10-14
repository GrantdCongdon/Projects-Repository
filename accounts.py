import json
import logging
import configparser
from logging.handlers import RotatingFileHandler
from order import Order
from Tkinter import *
import market
import algotrade
# loading configuration file
configLive = configparser.ConfigParser()
configLive.read('live/config.ini')
configSandbox = configparser.ConfigParser()
configSandbox.read('sandbox/config.ini')
algo = False
# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("python_client.log", maxBytes=5 * 1024 * 1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)
# general variables
screenWidth=75
numList = []
leave = ["Go Back"]
mainMenuItems = ["Get Market Quotes", "Begin Algotrading", "Manage Accounts", "Exit"]
brokeMenuItems = ["Get Account Balance", "Get Account Portfolio", "Manage Orders", "Go Back"]
instMenuItems = ["Balance", "Go Back"]
goBack = ["Go Back"]
accountIds = []
# tkinter functions
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
def createButtons(y, buttons, w, account, session, base_url, etrade, live, username, password, messageInterface=None, width=18, stick=S):
        r=0
        c=0
        for b in buttons:
                def cmd(x=b):
                        click(x, y, messageInterface, w, account, session, base_url, etrade, live, username, password)
                Button(y, text=b, width=width, command=cmd).grid(row=r, column=c,sticky=stick)
                c=c+1
                if (c>5):
                        c=0
                        r=r+1
def click(key, y, messageInterface, w, accounts, session, base_url, etrade, live, username, password):
	global market, numList, account, accountIds, accountId
	for a in numList:
		if (key==a and isinstance(a, (int, long)) and not algo):
			account = accounts[int(a)]
			accountId = accountIds[int(a)]
			accounts = Accounts(session, base_url, w, messageInterface, etrade, live, username, password)
			output(w, messageInterface, "Account "+str(key)+" selected")
			accounts.account_menu(account, y, w, session, base_url, etrade, messageInterface)
			break
		elif (key==a and isinstance(a, (int,long)) and algo):
			y.destroy()
			account = accounts[int(a)]
			accountId = accountIds[int(a)]
			algotradeMenu = algotrade.AlgoTrade(w, messageInterface, session, account, base_url, accountId, etrade, live, username, password)
			output(w, messageInterface, "Account "+str(key)+" selected")
			algotradeMenu.mainMenu()
			break
	if (key==numList[len(numList)-1]):
		y.destroy()
		output(w, messageInterface, "")
                buttonFrame = createFrame(w, 1, 0, 2, W)
        	btns = createButtons(buttonFrame, mainMenuItems, w, accounts, session, base_url, etrade, live, username, password, messageInterface=messageInterface)
	elif (key==mainMenuItems[0]):
		y.destroy()
		market = market.Market(session, base_url, w, messageInterface, etrade, live, username, password)
                market.quotes()
	elif (key==mainMenuItems[2]):
		y.destroy()
		numList = []
		accounts = Accounts(session, base_url, w, messageInterface, etrade, live, username, password)
        	accounts.account_list()
	elif (key==mainMenuItems[1]):
		y.destroy()
		numList = []
		algoLogin = Accounts(session, base_url, w, messageInterface, etrade, live, username, password)
                algoLogin.algoMainMenu()
    	elif (key==mainMenuItems[3]):
		w.destroy()
		exit()
	elif (key==brokeMenuItems[0]):
        	accounts = Accounts(session, base_url, w, messageInterface, etrade, live, username, password)
        	accounts.balance(account, w, messageInterface)
	elif (key==brokeMenuItems[1]):
        	accounts = Accounts(session, base_url, w, messageInterface, etrade, live, username, password)
        	accounts.portfolio(account, w, messageInterface)
	elif (key==brokeMenuItems[2]):
		y.destroy()
        	order = Order(session, accounts, base_url, accountId, live, username, password)
        	order.view_orders(w, messageInterface, account, etrade, base_url)
	elif (key==brokeMenuItems[3]):
		y.destroy()
		numList = []
		accounts = Accounts(session, base_url, w, messageInterface, etrade, live, username, password)
		accounts.account_list()
	elif (key==instMenuItems[0]):
        	accounts = Account(session, base_url, w, messageInterface, etrade, live, username, password)
        	accounts.balance(account, w, messageInterface)
	elif (key==instMenuItems[1]):
		y.destroy()
		numList = []
		accounts = Accounts(session, base_url, w, messageInterface, etrade, live, username, password)
		accounts.account_list()
    	elif (key==goBack[0]):
        	y.destroy()
		numList = []
		accounts = Accounts(session, base_url, w, messageInterface, etrade, live, username, password)
		accounts.account_list()
	elif (isinstance(key, (int, long))):
		ramble(w, messageInterface, "")
	else:
		output(w, messageInterface, "Error")

class Accounts:
    def __init__(self, session, base_url, w, mI, etrade, live, username, password):
        """
        Initialize Accounts object with session and account information

        :param session: authenticated session
        """
	self.username = username
	self.password = password
        self.session = session
        self.account = {}
        self.base_url = base_url
        self.w = w
        self.mI = mI
	self.etrade = etrade
	self.live = live
    def account_list(self):
        global numList, accountIds, algo
	"""
        Calls account list API to retrieve a list of the user's E*TRADE accounts

        :param self:Passes in parameter authenticated session
        """
        # URL for the API endpoint
        url = self.base_url + "/v1/accounts/list.json"
        # Make API call for GET request
        response = self.session.get(url, header_auth=True)
        logger.debug("Request Header: %s", response.request.headers)
	if (numList is not None):
		numList = []
        # Handle and parse response
        if response is not None and response.status_code == 200:
            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))

            data = response.json()
            if data is not None and "AccountListResponse" in data and "Accounts" in data["AccountListResponse"] \
                    and "Account" in data["AccountListResponse"]["Accounts"]:
                accounts = data["AccountListResponse"]["Accounts"]["Account"]
                # Display account list
                output(self.w, self.mI, "Brokerage Account List:")
                accounts[:] = [d for d in accounts if d.get('accountStatus') != 'CLOSED']
		count = 0
                for account in accounts:
			print_str = str(count) + ")\t"
                       	if account is not None and "accountId" in account:
                            print_str = print_str + (account["accountId"])
			    accountIds.append(account["accountId"])
                        if account is not None and "accountDesc" in account \
                                and account["accountDesc"].strip() is not None:
                            print_str = print_str + ", " + account["accountDesc"].strip()
                        if account is not None and "institutionType" in account:
                            print_str = print_str + ", " + account["institutionType"]
                        ramble(self.w, self.mI, "\n"+print_str)
                        numList.append(count)
			count = count + 1
		ramble(self.w, self.mI, "\nSelect an account")
		# Select account option
		numList.append("Main Menu")
                inputFrame = createFrame(self.w, 1, 0, 2, W)
		btns = createButtons(inputFrame, numList, self.w, accounts, self.session, self.base_url, self.etrade, self.live, self.username, self.password, messageInterface=self.mI)
		algo = False
            else:
                # Handle errors
                logger.debug("Response Body: %s", response.text)
                if response is not None and response.headers['Content-Type'] == 'application/json' \
                        and "Error" in response.json() and "message" in response.json()["Error"] \
                        and response.json()["Error"]["message"] is not None:
                    output(self.w, self.mI, "Error: " + data["Error"]["message"])
                else:
                    output(self.w, self.mI, "Error: AccountList API service error")
        else:
            # Handle errors
            logger.debug("Response Body: %s", response.text)
            if response is not None and response.headers['Content-Type'] == 'application/json' \
                    and "Error" in response.json() and "message" in response.json()["Error"] \
                    and response.json()["Error"]["message"] is not None:
                output(self.w, self.mI, "Error: " + response.json()["Error"]["message"])
            else:
                output(self.w, self.mI, "Error: AccountList API service error")
    def algoMainMenu(self):
        global numList, accountIds, algo
	"""
        Calls account list API to retrieve a list of the user's E*TRADE accounts

        :param self:Passes in parameter authenticated session
        """
        # URL for the API endpoint
        url = self.base_url + "/v1/accounts/list.json"
        # Make API call for GET request
        response = self.session.get(url, header_auth=True)
        logger.debug("Request Header: %s", response.request.headers)
	if (numList is not None):
		numList = []
        # Handle and parse response
        if response is not None and response.status_code == 200:
            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))

            data = response.json()
            if data is not None and "AccountListResponse" in data and "Accounts" in data["AccountListResponse"] \
                    and "Account" in data["AccountListResponse"]["Accounts"]:
                accounts = data["AccountListResponse"]["Accounts"]["Account"]
                # Display account list
                output(self.w, self.mI, "Brokerage Account List:")
                accounts[:] = [d for d in accounts if d.get('accountStatus') != 'CLOSED']
		count = 0
                for account in accounts:
			print_str = str(count) + ")\t"
                       	if account is not None and "accountId" in account:
                            print_str = print_str + (account["accountId"])
			    accountIds.append(account["accountId"])
                        if account is not None and "accountDesc" in account \
                                and account["accountDesc"].strip() is not None:
                            print_str = print_str + ", " + account["accountDesc"].strip()
                        if account is not None and "institutionType" in account:
                            print_str = print_str + ", " + account["institutionType"]
                        ramble(self.w, self.mI, "\n"+print_str)
                        numList.append(count)
			count = count + 1
		ramble(self.w, self.mI, "\nSelect an account")
		# Select account option
		numList.append("Main Menu")
                inputFrame = createFrame(self.w, 1, 0, 2, W)
		btns = createButtons(inputFrame, numList, self.w, accounts, self.session, self.base_url, self.etrade, self.live, self.username, self.password, messageInterface=self.mI)
		algo = True
            else:
                # Handle errors
                logger.debug("Response Body: %s", response.text)
                if response is not None and response.headers['Content-Type'] == 'application/json' \
                        and "Error" in response.json() and "message" in response.json()["Error"] \
                        and response.json()["Error"]["message"] is not None:
                    output(self.w, self.mI, "Error: " + data["Error"]["message"])
                else:
                    output(self.w, self.mI, "Error: AccountList API service error")
        else:
            # Handle errors
            logger.debug("Response Body: %s", response.text)
            if response is not None and response.headers['Content-Type'] == 'application/json' \
                    and "Error" in response.json() and "message" in response.json()["Error"] \
                    and response.json()["Error"]["message"] is not None:
                output(self.w, self.mI, "Error: " + response.json()["Error"]["message"])
            else:
                output(self.w, self.mI, "Error: AccountList API service error")

    def portfolio(self, account, w, messageInterface):
        """
        Call portfolio API to retrieve a list of positions held in the specified account

        :param self: Passes in parameter authenticated session and information on selected account
        """
	self.account = account
        # URL for the API endpoint
        url =self.base_url + "/v1/accounts/" + self.account["accountIdKey"] + "/portfolio.json"

        # Make API call for GET request
        response = self.session.get(url, header_auth=True)
        logger.debug("Request Header: %s", response.request.headers)

        output(w, messageInterface, "\nPortfolio:")

        # Handle and parse response
        if response is not None and response.status_code == 200:
            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
            data = response.json()

            if data is not None and "PortfolioResponse" in data and "AccountPortfolio" in data["PortfolioResponse"]:
                # Display balance information
                for acctPortfolio in data["PortfolioResponse"]["AccountPortfolio"]:
                    if acctPortfolio is not None and "Position" in acctPortfolio:
                        for position in acctPortfolio["Position"]:
                            print_str = "\n"
                            if position is not None and "symbolDescription" in position:
                                print_str = print_str + "Symbol: " + str(position["symbolDescription"])
                            if position is not None and "quantity" in position:
                                print_str = print_str + " | " + "Quantity #: " + str(position["quantity"])
                            if position is not None and "Quick" in position and "lastTrade" in position["Quick"]:
                                print_str = print_str + " | " + "Last Price: " \
                                            + str('${:,.2f}'.format(position["Quick"]["lastTrade"]))
                            if position is not None and "pricePaid" in position:
                                print_str = print_str + " | " + "Price Paid: " \
                                            + str('${:,.2f}'.format(position["pricePaid"]))
                            if position is not None and "totalGain" in position:
                                print_str = print_str + " | " + "Total Gain: " \
                                            + str('${:,.2f}'.format(position["totalGain"]))
                            if position is not None and "marketValue" in position:
                                print_str = print_str + " | " + "Value: " \
                                            + str('${:,.2f}'.format(position["marketValue"]))
                            ramble(w, messageInterface, print_str)
                    else:
                        output(w, messageInterface, "None")
            else:
                # Handle errors
                logger.debug("Response Body: %s", response.text)
                if response is not None and "headers" in response and "Content-Type" in response.headers \
                        and response.headers['Content-Type'] == 'application/json' \
                        and "Error" in response.json() and "message" in response.json()["Error"] \
                        and response.json()["Error"]["message"] is not None:
                    output(w, messageInterface, "Error: " + response.json()["Error"]["message"])
                else:
                    output(w, messageInterface, "Error: Portfolio API service error")
        elif response is not None and response.status_code == 204:
            output(w, messageInterface, "None")
        else:
            # Handle errors
            logger.debug("Response Body: %s", response.text)
            if response is not None and "headers" in response and "Content-Type" in response.headers \
                    and response.headers['Content-Type'] == 'application/json' \
                    and "Error" in response.json() and "message" in response.json()["Error"] \
                    and response.json()["Error"]["message"] is not None:
                output(w, messageInterface, "Error: " + response.json()["Error"]["message"])
            else:
                output(w, messsageInterface, "Error: Portfolio API service error")

    def balance(self, account, w, messageInterface):
        """
        Calls account balance API to retrieve the current balance and related details for a specified account

        :param self: Pass in parameters authenticated session and information on selected account
        """
	self.account = account
        # URL for the API endpoint
        url = self.base_url + "/v1/accounts/" + self.account["accountIdKey"] + "/balance.json"

        # Add parameters and header information
        params = {"instType": self.account["institutionType"], "realTimeNAV": "true"}
	if (self.live):
        	headers = {"consumerkey": configLive["DEFAULT"]["CONSUMER_KEY"]}
	else:
		headers = {"consumerkey": configSandbox["DEFAULT"]["CONSUMER_KEY"]}
        # Make API call for GET request
        response = self.session.get(url, header_auth=True, params=params, headers=headers)
        logger.debug("Request url: %s", url)
        logger.debug("Request Header: %s", response.request.headers)

        # Handle and parse response
        if response is not None and response.status_code == 200:
            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
            data = response.json()
            if data is not None and "BalanceResponse" in data:
                balance_data = data["BalanceResponse"]
                if balance_data is not None and "accountId" in balance_data:
                    output(w, messageInterface, "\n\nBalance for " + balance_data["accountId"] + ":")
                else:
                    output(w, messageInterface, "\n\nBalance:")
                # Display balance information
                if balance_data is not None and "accountDescription" in balance_data:
                    ramble(w, messageInterface, "\nAccount Nickname: " + balance_data["accountDescription"])
                if balance_data is not None and "Computed" in balance_data \
                        and "RealTimeValues" in balance_data["Computed"] \
                        and "totalAccountValue" in balance_data["Computed"]["RealTimeValues"]:
                    ramble(w, messageInterface, "\nNet Account Value: "
                          + str('${:,.2f}'.format(balance_data["Computed"]["RealTimeValues"]["totalAccountValue"])))
                if balance_data is not None and "Computed" in balance_data \
                        and "marginBuyingPower" in balance_data["Computed"]:
                    ramble(w, messageInterface, "\nMargin Buying Power: " + str('${:,.2f}'.format(balance_data["Computed"]["marginBuyingPower"])))
                if balance_data is not None and "Computed" in balance_data \
                        and "cashBuyingPower" in balance_data["Computed"]:
                    ramble(w, messageInterface, "\nCash Buying Power: " + str('${:,.2f}'.format(balance_data["Computed"]["cashBuyingPower"])))
		    return balance_data["Computed"]["cashBuyingPower"]
            else:
                # Handle errors
                logger.debug("Response Body: %s", response.text)
                if response is not None and response.headers['Content-Type'] == 'application/json' \
                        and "Error" in response.json() and "message" in response.json()["Error"] \
                        and response.json()["Error"]["message"] is not None:
                    output(w, messageInterface, "Error: " + response.json()["Error"]["message"])
                else:
                    output(w, messageInterface, "Error: Balance API service error")
        else:
            # Handle errors
            logger.debug("Response Body: %s", response.text)
            if response is not None and response.headers['Content-Type'] == 'application/json' \
                    and "Error" in response.json() and "message" in response.json()["Error"] \
                    and response.json()["Error"]["message"] is not None:
                output(w, messageInterface, "Error: " + response.json()["Error"]["message"])
            else:
                output(w, messageInterface, "Error: Balance API service error")
    def getBalance(self, account, w, messageInterface):
	self.account = account
        # URL for the API endpoint
        url = self.base_url + "/v1/accounts/" + self.account["accountIdKey"] + "/balance.json"

        # Add parameters and header information
        params = {"instType": self.account["institutionType"], "realTimeNAV": "true"}
        if (self.live):
                headers = {"consumerkey": configLive["DEFAULT"]["CONSUMER_KEY"]}
        else:
                headers = {"consumerkey": configSandbox["DEFAULT"]["CONSUMER_KEY"]}

        # Make API call for GET request
        response = self.session.get(url, header_auth=True, params=params, headers=headers)
        logger.debug("Request url: %s", url)
        logger.debug("Request Header: %s", response.request.headers)

        # Handle and parse response
        if response is not None and response.status_code == 200:
            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
            data = response.json()
            if data is not None and "BalanceResponse" in data:
                balance_data = data["BalanceResponse"]
                if balance_data is not None and "Computed" in balance_data \
                        and "cashBuyingPower" in balance_data["Computed"]:
		    return balance_data["Computed"]["cashBuyingPower"]
            else:
                # Handle errors
                logger.debug("Response Body: %s", response.text)
                if response is not None and response.headers['Content-Type'] == 'application/json' \
                        and "Error" in response.json() and "message" in response.json()["Error"] \
                        and response.json()["Error"]["message"] is not None:
                    output(w, messageInterface, "Error: " + response.json()["Error"]["message"])
                else:
                    output(w, messageInterface, "Error: Balance API service error")
        else:
            # Handle errors
            logger.debug("Response Body: %s", response.text)
            if response is not None and response.headers['Content-Type'] == 'application/json' \
                    and "Error" in response.json() and "message" in response.json()["Error"] \
                    and response.json()["Error"]["message"] is not None:
                output(w, messageInterface, "Error: " + response.json()["Error"]["message"])
            else:
                output(w, messageInterface, "Error: Balance API service error")
    def account_menu(self, account, y, w, session, base_url, etrade, messageInterface):
        """
        Provides the different options for the sample application: balance, portfolio, view orders

        :param self: Pass in authenticated session and information on selected account
        """
	self.account = account
        if self.account["institutionType"] == "BROKERAGE":
		y.destroy()
		inputFrame = createFrame(w, 1, 0, 2, W)
		btns = createButtons(inputFrame, brokeMenuItems, w, account, session, base_url, etrade, self.live, self.username, self.password, messageInterface=messageInterface)
        elif self.account["institutionType"] == "BANK":
		y.destroy()
                inputFrame = createFrame(w, 1, 0, 2, W)
                btns = createButtons(inputFrame, instMenuItems, w, session, base_url, etrade, self.live, self.username, self.password, messageInterface=messageInterface)
        else:
		y.destroy()
                inputFrame = createFrame(w, 1, 0, 2, W)
                btns = createButtons(inputFrame, goBack, w, session, base_url, etrade, self.live, self.username, self.password, messageInterface=messageInterface)
