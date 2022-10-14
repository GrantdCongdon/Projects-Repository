import random, configparser
from rauth import OAuth1Service
from retrying import retry
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
commission=6.99
configSandbox = configparser.ConfigParser()
configSandbox.read("sandbox/config.ini")
class Etrade():
	def __init__(self, live, accountId, username, password):
		self.live = live
		self.accountId = accountId
		self.username = username
		self.password = password
		self.base_url = configSandbox["DEFAULT"]["SANDBOX_BASE_URL"]
		self.etrade = OAuth1Service(name="etrade",
				consumer_key=configSandbox["DEFAULT"]["CONSUMER_KEY"],
				consumer_secrete=configSandbox["DEFAULT"]["CONSUMER_SECRET"],
				request_token_url="https://api.etrade.com/oauth/request_token",
				access_token_url="https://api.etrade.com/oauth/access_token",
				authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
				base_url="https://api.etrade.com")
	def trade(self, transaction, price, amount, symbol):
		order = {"price_type": "", "order_term": "", "symbol": "",
			"order_action": "", "limit_price":"", "quantity": ""}
		order["client_order_id"] = random.randint(1000000000, 9999999999)
		order["price_type"] = "LIMIT"
		order["order_term"] = "GOOD_FOR_DAY"
		order["symbol"] = symbol
		order["quantity"] = amount
		order["limit_price"] = price
		if (transaction=="buy"):
			order["order_action"] = "BUY"
			moneyChange = price*amount+commission
			print("Buying "+str(amount)+" "+symbol+" for "+str(price) + " each")
		else:
			order["order_action"] = "SELL"
			moneyChange = price*amount-commission
			print("Selling "+str(amount)+" "+symbol+" for "+str(price)+" each")
		session = signIn()
		account = selectAccount(session)
		orderStocks(session, account, order)
		return moneyChange
	def selectAccount(self, session):
		accountsUrl = self.base_url + "/v1/accounts/list.json"
		response = session.get(accountsUrl, header_auth=True)
		if (response is not None and response.status_code==200):
			data = response.json()
			accounts = data["AccountListReponse"]["Accounts]["Accounts"]
			accounts[:] = [d or d in accounts if d.get('accountStatus') != 'CLOSED']
			for account in accounts:
				if (account["accountId"]==self.accountId):
					return account
	def orderStocks(self, session, account, order):
		orderUrl = self.base_url + "/v1/accounts/" + account["accountIdKey"] +"/orders/preview.json"
		if (self.live):
			exit()
		else:
			headers = {"Content-Type": "application/xml", "consumerKey": configSandbox["DEFAULT"]["CONSUMER_KEY"]}
		payload = """<PreviewOrderRequest>
				<orderType>EQ</orderType>
				<clientOrderId>{0}</clientOrderId>
				<Order>
					<allOrNone>false</allOrNone>
					<priceType>{1}</priceType>
					<orderTerm>{2}</orderTerm>
					<marketSession>REGULAR</marketSession>
					<stopPrice></stopPrice>
					<limitPrice>{3}</limitPrice>
					<Instrument>
						<Product>
							<securityType>EQ</securityType>
							<symbol>{4}</symbol>
						</Product>
						<orderAction>{5}</orderAction>
						<quantityType>QUANTITY</quantityType>
						<quantity>{6}</quantity>
					</Instrument>
				</Order>
			</PreviewOrderRequest>"""
		payload = payload.format(order["client_order_id"], order["price_type"],
						order["order_term"], order["limit_price"],
						order["symbol"], order["order_action"],
						order["quantity"])
		response = session.post(orderUrl, header_auth=True, headers=headers, data=payload)
		if (response is not None and response.status_code==200):
			print(json.loads(response.txt))
	@retry(stop_max_attempt_number=3)
	def signIn(self):
		opts = Options()
		#opts.set_headless()
		requestToken, requestTokenSecrete = self.etrade.get_request_toekn(params={"oath_callback": "oob", "format": "json"})
                authorizeUrl = self.etrade.authorize_url.format(self.etrade.consumer_key, requestToken)
		browser = Firefox(options=opts)
		browser.get(authorize_url)
		usernameBox = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "USER")))
		passwordBox = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "PASSWORD")))
		logon = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.ID, "logon_button")))
		usernameBox.send_keys(self.username)
		passwordBox.send_keys(self.password)
		logon.click()
		acceptAgreement = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "submit")))
		sleep(0.5)
		acceptAgreement.click()
		WebDriverWait(browser, 10).until(ec.presense_of_element_located((By.TAG_NAME, "input")))
		code = codeBox.get_attribute('value')
		browser.close()
		session = self.etrade.get_auth_session(requestToken, requestTokenSecrete, params={"oauth_verifier": code})
		return session
