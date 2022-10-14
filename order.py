import json
import logging
from logging.handlers import RotatingFileHandler
import configparser
import random
import re
from Tkinter import *
import accounts
import market
import datetime
import accounts
import quote as q
import datetime, holidays
from time import sleep
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from rauth import OAuth1Service
import pymail
# general variables
screenWidth=100
labelWidth=12
mainMenuItems = ["Preview Order", "Cancel Order", "Go Back"]
previewMenuItems = ["Select New Order", "Select From Previous Orders", "Order Menu"]
priceTypeItems = ["MARKET", "LIMIT"]
orderTermItems = ["GOOD_FOR_DAY", "IMMEDIATE_OR_CANCEL", "FILL_OR_KILL"]
orderActionItems = ["BUY", "SELL", "BUY_TO_COVER", "SELL_SHORT"]
brokeMenuItems = ["Get Account Balance", "Get Account Portfolio", "Manage Orders", "Account List"]
yesOrNo = ["Accept", "Return To Start"]
goBack = ["Cancel"]
orderList = []
prevOrderList = []
order = {"price_type": "",
	"order_term": "",
        "symbol": "",
       	"order_action": "",
        "limit_price":"",
        "quantity": ""}
yesOrNo = ["Accept", "Return To Start"]
accountId = 0
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
#browser
#config
configLive = configparser.ConfigParser()
configLive.read('live/config.ini')
configSandbox = configparser.ConfigParser()
configSandbox.read('sandbox/config.ini')
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
def createButtons(y, buttons, w, account, base_url, etrade, prev_orders, messageInterface=None, y2=None, width=24, stick=S):
        r=0
        c=0
        for b in buttons:
                def cmd(x=b):
                        click(x, y, w, messageInterface, account, base_url, etrade, prev_orders, y2)
                Button(y, text=b, width=width, command=cmd).grid(row=r, column=c,sticky=stick)
                c=c+1
                if (c>5):
                        c=0
                        r=r+1
def click(key, y, w, mI, account, base_url, etrade, prev_orders, y2):
	global accounts, marketSymbol, quantity, limitPrice, order, accountId, live, session, username, password
	for a in range(len(orderList)):
		if (key==orderList[a] and isinstance(key, (int, long))):
			# URL for the API endpoint
                       	url = base_url + "/v1/accounts/" + account["accountIdKey"] + "/orders/cancel.json"

                        # Add parameters and header information
			if (live):
                        	headers = {"Content-Type": "application/xml", "consumerKey": configLive["DEFAULT"]["CONSUMER_KEY"]}
			else:
				headers = {"Content-Type": "application/xml", "consumerKey": configSandbox["DEFAULT"]["CONSUMER_KEY"]}
                        # Add payload for POST Request
                        payload = """<CancelOrderRequest>
                                     	<orderId>{0}</orderId>
                                   	</CancelOrderRequest>
                                  """
                        payload = payload.format(orderList[int(a)])

                        # Add payload for PUT Request
                        response = session.put(url, header_auth=True, headers=headers, data=payload)
                        logger.debug("Request Header: %s", response.request.headers)
                        logger.debug("Request payload: %s", payload)

                        # Handle and parse response
                        if response is not None and response.status_code == 200:
                        	parsed = json.loads(response.text)
                            	logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
                            	data = response.json()
                            	if data is not None and "CancelOrderResponse" in data and "orderId" in data["CancelOrderResponse"]:
                                	ramble(w, mI, "\nOrder number #" + str(
                                    	data["CancelOrderResponse"]["orderId"]) + " successfully Cancelled.")
                            	else:
                                	# Handle errors
                                	logger.debug("Response Headers: %s", response.headers)
                                	logger.debug("Response Body: %s", response.text)
                                	data = response.json()
                                	if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                                    		output(w, mI, "Error: " + data["Error"]["message"])
                                	else:
                                    		output(w, mI, "Error: Cancel Order API service error")
                        else:
                        	# Handle errors
                            	logger.debug("Response Headers: %s", response.headers)
                            	logger.debug("Response Body: %s", response.text)
                            	data = response.json()
                            	if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                                	output(w, mI, "Error: " + data["Error"]["message"])
                            	else:
                                	output(w, mI, "Error: Cancel Order API service error")
			break
		elif (key==orderList[len(orderList)-1] and orderList is not None):
			y.destroy()
			orderObject = Order(session, account, base_url, accountId, live, username, password)
			orderObject.view_orders(w, mI, account, etrade, base_url)
			break
	for b in range(len(prevOrderList)):
                if (key==prevOrderList[b] and isinstance(key, (int, long))):
                    # URL for the API endpoint
                    url = base_url + "/v1/accounts/" + account["accountIdKey"] + "/orders/preview.json"
                    # Add parameters and header information
		    if (live):
                    	headers = {"Content-Type": "application/xml", "consumerKey": configLive["DEFAULT"]["CONSUMER_KEY"]}
		    else:
			headers = {"Content-Type": "application/xml", "consumerKey": configSandbox["DEFAULT"]["CONSUMER_KEY"]}
                    now = datetime.datetime.now()
                    # Add payload for POST Request
                    payload = """<PreviewOrderRequest>
                                   <orderType>{0}</orderType>
                                   <clientOrderId>{1}</clientOrderId>
                                   <Order>
                                       <allOrNone>false</allOrNone>
                                       <priceType>{2}</priceType>
                                       <orderTerm>{3}</orderTerm>
                                       <marketSession>REGULAR</marketSession>
                                       <stopPrice></stopPrice>
                                       <limitPrice>{4}</limitPrice>
                                       <Instrument>
                                           <Product>
                                               <callPut>CALL</callPut>
                                               <expiryDay>{9}</expiryDay>
                                               <expiryMonth>{10}</expiryMonth>
                                               <expiryYear>{11}</expiryYear>
                                               <strikePrice>{12}</strikePrice>
                                               <securityType>{5}</securityType>
                                               <symbol>{6}</symbol>
                                           </Product>
                                           <orderAction>{7}</orderAction>
                                           <quantityType>QUANTITY</quantityType>
                                           <quantity>{8}</quantity>
                                       </Instrument>
                                   </Order>
                               </PreviewOrderRequest>"""
		    options_select = int(key)
                    prev_orders[options_select - 1]["client_order_id"] = str(random.randint(1000000000,9999999999))
                    payload = payload.format(prev_orders[options_select - 1]["order_type"],
                                             prev_orders[options_select - 1]["client_order_id"],
                                             prev_orders[options_select - 1]["price_type"],
                                             prev_orders[options_select - 1]["order_term"],
                                             prev_orders[options_select - 1]["limitPrice"],
                                             prev_orders[options_select - 1]["security_type"],
                                             prev_orders[options_select - 1]["symbol"],
                                             prev_orders[options_select - 1]["order_action"],
                                             prev_orders[options_select - 1]["quantity"],
                                             now.day, now.month, now.year,
                                             prev_orders[options_select - 1]["limitPrice"])

                    # Make API call for POST request
                    response = session.post(url, header_auth=True, headers=headers, data=payload)
                    logger.debug("Request Header: %s", response.request.headers)
                    logger.debug("Request payload: %s", payload)

                    # Handle and parse response
                    if response is not None and response.status_code == 200:
                        parsed = json.loads(response.text)
                        logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
                        data = response.json()
                        output(w, mI, "\nPreview Order: ")
                        if data is not None and "PreviewOrderResponse" in data and "PreviewIds" in data["PreviewOrderResponse"]:
                            for previewids in data["PreviewOrderResponse"]["PreviewIds"]:
                                ramble(w, mI, "\nPreview ID: " + str(previewids["previewId"]))
                        else:
                            # Handle errors
                            data = response.json()
                            if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                                output(w, mI, "\nError: " + data["Error"]["message"])
                                logger.debug("Response Body: %s", response)
		    	    else:
                                output(w, mI, "\nError: Preview Order API service error")
                                logger.debug("Response Body: %s", response)

                        if data is not None and "PreviewOrderResponse" in data and "Order" in data[
                            "PreviewOrderResponse"]:
                            for orders in data["PreviewOrderResponse"]["Order"]:
                                prev_orders[options_select - 1]["limitPrice"] = orders["limitPrice"]

                                if orders is not None and "Instrument" in orders:
                                    for instruments in orders["Instrument"]:
                                        if instruments is not None and "orderAction" in instruments:
                                            ramble(w, mI, "\nAction: " + instruments["orderAction"])
                                        if instruments is not None and "quantity" in instruments:
                                            ramble(w, mI, "\nQuantity: " + str(instruments["quantity"]))
                                        if instruments is not None and "Product" in instruments \
                                                and "symbol" in instruments["Product"]:
                                            ramble(w, mI, "\nSymbol: " + instruments["Product"]["symbol"])
                                        if instruments is not None and "symbolDescription" in instruments:
                                            ramble(w, mI, "\nDescription: " + str(instruments["symbolDescription"]))

                            if orders is not None and "priceType" in orders and "limitPrice" in orders:
                                ramble(w, mI, "Price Type: " + orders["priceType"])
                                if orders["priceType"] == "MARKET":
                                    ramble(w, mI, "\nPrice: MKT")
                                else:
                                    ramble(w, mI, "Price: " + str(orders["limitPrice"]))
                            if orders is not None and "orderTerm" in orders:
                                ramble(w, mI, "\nDuration: " + orders["orderTerm"])
                            if orders is not None and "estimatedCommission" in orders:
				ramble(w, mI, "\nEstimated Commission: " + str(orders["estimatedCommission"]))
                            if orders is not None and "estimatedTotalAmount" in orders:
                                ramble(w, mI, "\nEstimated Total Cost: " + str(orders["estimatedTotalAmount"]))
                        else:
                            # Handle errors
                            data = response.json()
                            if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                                output(w, mI, "Error: " + data["Error"]["message"])
                                logger.debug("Response Body: %s", response)
                            else:
                                output(w, mI, "Error: Preview Order API service error")
                                logger.debug("Response Body: %s", response)
                    else:
                        # Handle errors
                        data = response.json()
                        if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                            output(w, mI, "Error: " + data["Error"]["message"])
                            logger.debug("Response Body: %s", response)
                        else:
                            output(w, mI, "Error: Preview Order API service error")
                            logger.debug("Response Body: %s", response)
                    y.destroy()
                    inputFrame = createFrame(w, 1, 0, 2, W)
                    btns = createButtons(inputFrame, mainMenuItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
                    break
                elif (key==prevOrderList[len(prevOrderList)-1] and prevOrderList is not None):
                        y.destroy()
                        orderObject = Order(session, account, base_url, accountId, live, username, password)
                        orderObject.preview_order_menu(prev_orders, w, account, base_url, etrade, mI, y)
                        break
	if (key==mainMenuItems[0]):
		y.destroy()
		orderObject = Order(session, account, base_url, accountId, live, username, password)
		orderObject.preview_order_menu(prev_orders, w, account, base_url, etrade, mI, y)
	elif (key==mainMenuItems[1]):
		y.destroy()
		orderObject = Order(session, account, base_url, accountId, live, username, password)
		orderObject.cancel_order(w, mI, account, base_url, etrade, prev_orders)
        elif (key==mainMenuItems[2]):
                y.destroy()
		btnFrame = createFrame(w, 1, 0, 2, W)
		btns = createButtons(btnFrame, brokeMenuItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
	if (key==brokeMenuItems[0]):
                accountss = accounts.Accounts(session, base_url, w, mI, etrade, live, username, password)
                accountss.balance(account, w, messageInterface)
        elif (key==brokeMenuItems[1]):
                accountss = accounts.Accounts(session, base_url, w, mI, etrade, live, username, password)
                accountss.portfolio(account, w, messageInterface)
        elif (key==brokeMenuItems[2]):
                y.destroy()
                order = Order(session, accounts, base_url, accountId, live, username, password)
                order.view_orders(w, mI, account, etrade, base_url)
        elif (key==brokeMenuItems[3]):
                y.destroy()
                numList = []
                accountss = accounts.Accounts(session, base_url, w, mI, etrade, live, username, password)
                accountss.account_list()
	elif (key==previewMenuItems[2]):
		y.destroy()
		orderObject = Order(session, account, base_url, accountId, live, username, password)
		orderObject.view_orders(w, mI, account, etrade, base_url)
	elif (key==previewMenuItems[1]):
		y.destroy()
		orderObject = Order(session, account, base_url, accountId, live, username, password)
		orderObject.previous_order(account, prev_orders, w, mI, base_url, etrade)
	elif (key==previewMenuItems[0]):
		y.destroy()
		orderObject = Order(session, account, base_url, accountId, live, username, password)
		orderObject.user_select_order(w, account, base_url, etrade, prev_orders, mI)
	elif (key==priceTypeItems[0]):
		y.destroy()
		order["price_type"] = key
		order["order_term"] = "GOOD_FOR_DAY"
		order["limit_price"] = None
		inputFrame = createFrame(w, 1, 0, 2, W)
		btns = createButtons(inputFrame, orderActionItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
	elif (key==priceTypeItems[1]):
		y.destroy()
		order["price_type"] = key
		inputFrame = createFrame(w, 1, 0, 2, W)
		btns = createButtons(inputFrame, orderTermItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
	elif (key==orderTermItems[0]):
                y.destroy()
                order["order_term"] = key
                inputFrame = createFrame(w, 1, 0, 2, W)
                btns = createButtons(inputFrame, orderActionItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
        elif (key==orderTermItems[1]):
                y.destroy()
                order["order_term"] = key
                inputFrame = createFrame(w, 1, 0, 2, W)
                btns = createButtons(inputFrame, orderActionItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
        elif (key==orderTermItems[2]):
                y.destroy()
                order["order_term"] = key
                inputFrame = createFrame(w, 1, 0, 2, W)
                btns = createButtons(inputFrame, orderActionItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
	elif (key==orderActionItems[0] and order["price_type"]=="LIMIT"):
                y.destroy()
                order["order_action"] = key
                entryFrame = createFrame(w, 1, 0, 2, W)
                limitPrice = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                limitPrice.grid(row=0, column=1, sticky=W)
                limitLabel = Label(entryFrame, width=labelWidth, height=1, text="Limit Price").grid(row=0, column=0, sticky=W)
                marketSymbol = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                marketSymbol.grid(row=1, column=1, sticky=W)
                symbolLabel = Label(entryFrame, width=labelWidth, height=1, text="Symbol").grid(row=1, column=0, sticky=W)
                quantity = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                quantity.grid(row=2, column=1, sticky=W)
                quantityLabel = Label(entryFrame, width=labelWidth, height=1, text="Quantity").grid(row=2, column=0, sticky=W)
                buttonFrame = createFrame(w, 2, 0, 2, W)
                btns = createButtons(buttonFrame, yesOrNo, w, account, base_url, etrade, prev_orders, messageInterface=mI, y2=entryFrame)
        elif (key==orderActionItems[1] and order["price_type"]=="LIMIT"):
                y.destroy()
                order["order_action"] = key
                entryFrame = createFrame(w, 1, 0, 2, W)
                limitPrice = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                limitPrice.grid(row=0, column=1, sticky=W)
                limitLabel = Label(entryFrame, width=labelWidth, height=1, text="Limit Price").grid(row=0, column=0, sticky=W)
                marketSymbol = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                marketSymbol.grid(row=1, column=1, sticky=W)
                symbolLabel = Label(entryFrame, width=labelWidth, height=1, text="Symbol").grid(row=1, column=0, sticky=W)
                quantity = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                quantity.grid(row=2, column=1, sticky=W)
                quantityLabel = Label(entryFrame, width=labelWidth, height=1, text="Quantity").grid(row=2, column=0, sticky=W)
                buttonFrame = createFrame(w, 2, 0, 2, W)
                btns = createButtons(buttonFrame, yesOrNo, w, account, base_url, etrade, prev_orders, messageInterface=mI, y2=entryFrame)
	elif (key==orderActionItems[2] and order["price_type"]=="LIMIT"):
                y.destroy()
                order["order_action"] = key
                entryFrame = createFrame(w, 1, 0, 2, W)
                limitPrice = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                limitPrice.grid(row=0, column=1, sticky=W)
                limitLabel = Label(entryFrame, width=labelWidth, height=1, text="Limit Price").grid(row=0, column=0, sticky=W)
                marketSymbol = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                marketSymbol.grid(row=1, column=1, sticky=W)
                symbolLabel = Label(entryFrame, width=labelWidth, height=1, text="Symbol").grid(row=1, column=0, sticky=W)
                quantity = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                quantity.grid(row=2, column=1, sticky=W)
                quantityLabel = Label(entryFrame, width=labelWidth, height=1, text="Quantity").grid(row=2, column=0, sticky=W)
                buttonFrame = createFrame(w, 2, 0, 2, W)
                btns = createButtons(buttonFrame, yesOrNo, w, account, base_url, etrade, prev_orders, messageInterface=mI, y2=entryFrame)
        elif (key==orderActionItems[3] and order["price_type"]=="LIMIT"):
                y.destroy()
                order["order_action"] = key
                entryFrame = createFrame(w, 1, 0, 2, W)
                limitPrice = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                limitPrice.grid(row=0, column=1, sticky=W)
                limitLabel = Label(entryFrame, width=labelWidth, height=1, text="Limit Price").grid(row=0, column=0, sticky=W)
                marketSymbol = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                marketSymbol.grid(row=1, column=1, sticky=W)
                symbolLabel = Label(entryFrame, width=labelWidth, height=1, text="Symbol").grid(row=1, column=0, sticky=W)
                quantity = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                quantity.grid(row=2, column=1, sticky=W)
                quantityLabel = Label(entryFrame, width=labelWidth, height=1, text="Quantity").grid(row=2, column=0, sticky=W)
                buttonFrame = createFrame(w, 2, 0, 2, W)
                btns = createButtons(buttonFrame, yesOrNo, w, account, base_url, etrade, prev_orders, messageInterface=mI, y2=entryFrame)
	elif (key==orderActionItems[0] and order["price_type"]=="MARKET"):
                y.destroy()
                order["order_action"] = key
                entryFrame = createFrame(w, 1, 0, 2, W)
                marketSymbol = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                marketSymbol.grid(row=0, column=1, sticky=W)
                symbolLabel = Label(entryFrame, width=labelWidth, height=1, text="Symbol").grid(row=0, column=0, sticky=W)
                quantity = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                quantity.grid(row=1, column=1, sticky=W)
                quantityLabel = Label(entryFrame, width=labelWidth, height=1, text="Quantity").grid(row=1, column=0, sticky=W)
                buttonFrame = createFrame(w, 2, 0, 2, W)
                btns = createButtons(buttonFrame, yesOrNo, w, account, base_url, etrade, prev_orders, messageInterface=mI, y2=entryFrame)
        elif (key==orderActionItems[1] and order["price_type"]=="MARKET"):
                y.destroy()
                order["order_action"] = key
                entryFrame = createFrame(w, 1, 0, 2, W)
                marketSymbol = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                marketSymbol.grid(row=0, column=1, sticky=W)
                symbolLabel = Label(entryFrame, width=labelWidth, height=1, text="Symbol").grid(row=0, column=0, sticky=W)
                quantity = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                quantity.grid(row=1, column=1, sticky=W)
                quantityLabel = Label(entryFrame, width=labelWidth, height=1, text="Quantity").grid(row=1, column=0, sticky=W)
                buttonFrame = createFrame(w, 2, 0, 2, W)
                btns = createButtons(buttonFrame, yesOrNo, w, account, base_url, etrade, prev_orders, messageInterface=mI, y2=entryFrame)
	elif (key==orderActionItems[3] and order["price_type"]=="MARKET"):
                y.destroy()
                order["order_action"] = key
                entryFrame = createFrame(w, 1, 0, 2, W)
                marketSymbol = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                marketSymbol.grid(row=0, column=1, sticky=W)
                symbolLabel = Label(entryFrame, width=labelWidth, height=1, text="Symbol").grid(row=0, column=0, sticky=W)
                quantity = Entry(entryFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
                quantity.grid(row=1, column=1, sticky=W)
                quantityLabel = Label(entryFrame, width=labelWidth, height=1, text="Quantity").grid(row=1, column=0, sticky=W)
                buttonFrame = createFrame(w, 2, 0, 2, W)
                btns = createButtons(buttonFrame, yesOrNo, w, account, base_url, etrade, prev_orders, messageInterface=mI, y2=entryFrame)
	elif (key==yesOrNo[0] and order["price_type"]=="LIMIT"):
                y.destroy()
                order["limit_price"] = limitPrice.get()
                order["symbol"] = marketSymbol.get()
                order["quantity"] = quantity.get()
                y2.destroy()
                orderObject = Order(session, account, base_url, accountId, live, username, password)
                orderObject.preview_order(w, mI, order)
                inputFrame = createFrame(w, 1, 0, 2, W)
                btns = createButtons(inputFrame, mainMenuItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
        elif (key==yesOrNo[0] and order["price_type"]=="MARKET"):
                y.destroy()
                order["symbol"] = marketSymbol.get()
                order["quantity"] = quantity.get()
                y2.destroy()
                orderObject = Order(session, account, base_url, accountId, live, username, password)
                orderObject.preview_order(w, mI, order)
                inputFrame = createFrame(w, 1, 0, 2, W)
                btns = createButtons(inputFrame, mainMenuItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
        elif (key==yesOrNo[1]):
                y.destroy()
                y2.destroy()
                orderObject = Order(session, account, base_url, accountId, live, username, password)
                orderObject.preview_order_menu(prev_orders, w, account, base_url, etrade, mI, y)
	else:
		ramble(w, mI, "Error")
class Order:

    def __init__(self, sessions, account, base_url, accountIdt, livee, usernamee, passwordd):
	global table, accountId, tBudget, live, session, username, password
	accountId = accountIdt
        session = sessions
        self.account = account
        self.base_url = base_url
	live = livee
	username = usernamee
	password = passwordd

    def preview_order(self, w, mI, order):
        """
        Call preview order API based on selecting from different given options

        :param self: Pass in authenticated session and information on selected account
        """

        # URL for the API endpoint
        url = self.base_url + "/v1/accounts/" + self.account["accountIdKey"] + "/orders/preview.json"

        # Add parameters and header information
	if (live):
        	headers = {"Content-Type": "application/xml", "consumerKey": configLive["DEFAULT"]["CONSUMER_KEY"]}
	else:
		headers = {"Content-Type": "application/xml", "consumerKey": configSandbox["DEFAULT"]["CONSUMER_KEY"]}
        # Add payload for POST Request
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
        payload = payload.format(order["client_order_id"], order["price_type"], order["order_term"],
                                 order["limit_price"], order["symbol"], order["order_action"], order["quantity"])

        # Make API call for POST request
        response = session.post(url, header_auth=True, headers=headers, data=payload)
        logger.debug("Request Header: %s", response.request.headers)
        logger.debug("Request payload: %s", payload)

        # Handle and parse response
        if response is not None and response.status_code == 200:
            parsed = json.loads(response.text)
            logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
            data = response.json()
            output(w, mI, "\nPreview Order:")

            if data is not None and "PreviewOrderResponse" in data and "PreviewIds" in data["PreviewOrderResponse"]:
                for previewids in data["PreviewOrderResponse"]["PreviewIds"]:
                    ramble(w, mI, "\nPreview ID: " + str(previewids["previewId"]))
            else:
                # Handle errors
                data = response.json()
                if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                    output(w, mI, "Error: " + data["Error"]["message"])
                else:
                    output(w, mI, "Error: Preview Order API service error")

            if data is not None and "PreviewOrderResponse" in data and "Order" in data["PreviewOrderResponse"]:
                for orders in data["PreviewOrderResponse"]["Order"]:
                    if orders is not None and "priceType" in orders and "limitPrice" in orders:
		    	order["limitPrice"] = orders["limitPrice"]

                    if orders is not None and "Instrument" in orders:
                        for instrument in orders["Instrument"]:
                            if instrument is not None and "orderAction" in instrument:
                                ramble(w, mI, "\nAction: " + instrument["orderAction"])
                            if instrument is not None and "quantity" in instrument:
                                ramble(w, mI, "\nQuantity: " + str(instrument["quantity"]))
                            if instrument is not None and "Product" in instrument \
                                    and "symbol" in instrument["Product"]:
                                ramble(w, mI, "\nSymbol: " + instrument["Product"]["symbol"])
                            if instrument is not None and "symbolDescription" in instrument:
                                ramble(w, mI, "\nDescription: " + str(instrument["symbolDescription"]))

                if orders is not None and "priceType" in orders and "limitPrice" in orders:
                    ramble(w, mI, "Price Type: " + orders["priceType"])
                    if orders["priceType"] == "MARKET":
                        ramble(w, mI, "\nPrice: MKT")
                    else:
                        ramble(w, mI, "\nPrice: " + str(orders["limitPrice"]))
                if orders is not None and "orderTerm" in orders:
                    ramble(w, mI, "\nDuration: " + orders["orderTerm"])
                if orders is not None and "estimatedCommission" in orders:
                    ramble(w, mI, "\nEstimated Commission: " + str(orders["estimatedCommission"]))
                if orders is not None and "estimatedTotalAmount" in orders:
                    ramble(w, mI, "\nEstimated Total Cost: " + str(orders["estimatedTotalAmount"]))
            else:
                # Handle errors
                data = response.json()
                if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                    output(w, mI, "Error: " + data["Error"]["message"])
                else:
                    ramble(w, mI, "Error: Preview Order API service error")
        else:
            # Handle errors
            data = response.json()
            if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                output(w, mI, "Error: " + data["Error"]["message"])
            else:
                output(w, mI, "Error: Preview Order API service error")
    def preview_order_menu(self, prev_orders, w, account, base_url, etrade, mI, y):
	global session
	y.destroy()
	inputFrame = createFrame(w, 1, 0, 2, W)
	btns = createButtons(inputFrame, previewMenuItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
    def previous_order(self, account, prev_orders, w, mI, base_url, etrade):
        global prevOrderList, session
	if (prevOrderList is not None):
		prevOrderList = []
	"""
        Calls preview order API based on a list of previous orders

        :param session: authenticated session
        :param account: information on selected account
        :param prev_orders: list of instruments from previous orders
        """

        if prev_orders is not None:
        	# Display previous instruments for user selection
        	output(w, mI, "")
                count = 1
                for order in prev_orders:
                    ramble(w, mI, str(count) + ")\tOrder Action: " + order["order_action"] + " | "
                          + "Security Type: " + str(order["security_type"]) + " | "
                          + "Term: " + str(order["order_term"]) + " | "
                          + "Quantity: " + str(order["quantity"]) + " | "
                          + "Symbol: " + order["symbol"] + " | "
                          + "Price Type: " + order["price_type"])
		    prevOrderList.append(count)
                    count = count + 1
		prevOrderList.append("Order Menu")
                ramble(w, mI, str(count) + ")\t" "Go Back")
		inputFrame = createFrame(w, 1, 0, 2, W)
		btns = createButtons(inputFrame, prevOrderList, w, account, base_url, etrade, prev_orders, messageInterface=mI, width=12)

    @staticmethod
    def print_orders(response, status, w, mI):
        """
        Formats and displays a list of orders

        :param response: response object of a list of orders
        :param status: order status related to the response object
        :return a list of previous orders
        """
        prev_orders = []
        if response is not None and "OrdersResponse" in response and "Order" in response["OrdersResponse"]:
            for order in response["OrdersResponse"]["Order"]:
                if order is not None and "OrderDetail" in order:
                    for details in order["OrderDetail"]:
                        if details is not None and "Instrument" in details:
                            for instrument in details["Instrument"]:
                                order_str = ""
                                order_obj = {"price_type": None,
                                             "order_term": None,
                                             "order_indicator": None,
                                             "order_type": None,
                                             "security_type": None,
                                             "symbol": None,
                                             "order_action": None,
                                             "quantity": None}
                                if order is not None and 'orderType' in order:
                                    order_obj["order_type"] = order["orderType"]

                                if order is not None and 'orderId' in order:
                                    order_str += "\nOrder "

                                if instrument is not None and 'Product' in instrument \
                                        and 'securityType' in instrument["Product"]:
                                    order_str += "\nType: " + instrument["Product"]["securityType"]
                                    order_obj["security_type"] = instrument["Product"]["securityType"]

                                if instrument is not None and 'orderAction' in instrument:
                                    order_str += "\nOrder Type: " + instrument["orderAction"]
                                    order_obj["order_action"] = instrument["orderAction"]

                                if instrument is not None and 'orderedQuantity' in instrument:
                                    order_str += "\nQuantity(Exec/Entered): " + str("{:,}".format(instrument["orderedQuantity"]))
                                    order_obj["quantity"] = instrument["orderedQuantity"]

                                if instrument is not None and 'Product' in instrument and 'symbol' in instrument["Product"]:
                                    order_str += "\nSymbol: " + instrument["Product"]["symbol"]
                                    order_obj["symbol"] = instrument["Product"]["symbol"]

                                if details is not None and 'priceType' in details:
                                    order_str += "\nPrice Type: " + details["priceType"]
                                    order_obj["price_type"] = details["priceType"]

                                if details is not None and 'orderTerm' in details:
                                    order_str += "\nTerm: " + details["orderTerm"]
                                    order_obj["order_term"] = details["orderTerm"]

                                if details is not None and 'limitPrice' in details:
                                    order_str += "\nPrice: " + str('${:,.2f}'.format(details["limitPrice"]))
                                    order_obj["limitPrice"] = details["limitPrice"]

                                if status == "Open" and details is not None and 'netBid' in details:
                                    order_str += "\nBid: " + details["netBid"]
                                    order_obj["bid"] = details["netBid"]

                                if status == "Open" and details is not None and 'netAsk' in details:
                                    order_str += "\nAsk: " + details["netAsk"]
                                    order_obj["ask"] = details["netAsk"]

                                if status == "Open" and details is not None and 'netPrice' in details:
                                    order_str += "\nLast Price: " + details["netPrice"]
                                    order_obj["netPrice"] = details["netPrice"]

                                if status == "indiv_fills" and instrument is not None and 'filledQuantity' in instrument:
                                    order_str += "\nQuantity Executed: " + str("{:,}".format(instrument["filledQuantity"]))
                                    order_obj["quantity"] = instrument["filledQuantity"]

                                if status != "open" and status != "expired" and status != "rejected" and instrument is not None \
                                        and "averageExecutionPrice" in instrument:
                                    order_str += "\nPrice Executed: " + str('${:,.2f}'.format(instrument["averageExecutionPrice"]))

                                if status != "expired" and status != "rejected" and details is not None and 'status' in details:
                                    order_str += "\nStatus: " + details["status"]

                                ramble(w, mI, order_str)
                                prev_orders.append(order_obj)
        return prev_orders

    @staticmethod
    def options_selection(options):
        """
        Formats and displays different options in a menu

        :param options: List of options to display
        :return the number user selected
        """
        while True:
            print("")
            for num, price_type in enumerate(options, start=1):
                print("{})\t{}".format(num, price_type))
            options_select = input("Please select an option: ")
            if options_select.isdigit() and 0 < int(options_select) < len(options) + 1:
                return options_select
            else:
                print("Unknown Option Selected!")

    def user_select_order(self, w, account, base_url, etrade, prev_orders, mI):
        global order, session
	"""
            Provides users options to select to preview orders
            :param self test
            :return user's order selections
            """
	order = {"price_type": "",
                 "order_term": "",
                 "symbol": "",
                 "order_action": "",
                 "limit_price":"",
                 "quantity": ""}
        output(w, mI, "Price Type")
	inputFrame = createFrame(w, 1, 0, 2, W)
	btns = createButtons(inputFrame, priceTypeItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
        order["client_order_id"] = random.randint(1000000000, 9999999999)

        return order

    def cancel_order(self, w, mI, account, base_url, etrade, prev_orders):
        global session
	"""
        Calls cancel order API to cancel an existing order
        :param self: Pass parameter with authenticated session and information on selected account
        """
        # Display a list of Open Orders
        # URL for the API endpoint
        url = self.base_url + "/v1/accounts/" + self.account["accountIdKey"] + "/orders.json"

        # Add parameters and header information
        params_open = {"status": "OPEN"}
	if (live):
        	headers = {"consumerkey": configLive["DEFAULT"]["CONSUMER_KEY"]}
	else:
		headers = {"consumerkey": configSandbox["DEFAULT"]["CONSUMER_KEY"]}

        # Make API call for GET request
        response_open = session.get(url, header_auth=True, params=params_open, headers=headers)

        logger.debug("Request Header: %s", response_open.request.headers)
        logger.debug("Response Body: %s", response_open.text)

        output(w, mI, "\nOpen Orders: ")
        # Handle and parse response
        if response_open.status_code == 204:
        	logger.debug(response_open)
                ramble(w, mI, "\nNone")
                inputFrame = createFrame(w, 1, 0, 2, W)
		btns = createButtons(inputFrame, goBack, account, base_url, etrade, prev_orders)
        elif (response_open.status_code == 200):
                parsed = json.loads(response_open.text)
                logger.debug(json.dumps(parsed, indent=4, sort_keys=True))
                data = response_open.json()

		orderList = []
                count = 1
            	if data is not None and "OrdersResponse" in data and "Order" in data["OrdersResponse"]:
                	for order in data["OrdersResponse"]["Order"]:
                        	if order is not None and "OrderDetail" in order:
                            		for details in order["OrderDetail"]:
                                		if details is not None and "Instrument" in details:
                                    			for instrument in details["Instrument"]:
                                        			order_str = ""
                                        			order_obj = {"price_type": None,
                                                     			"order_term": None,
                                                     			"order_indicator": None,
                                                     			"order_type": None,
                                                     			"security_type": None,
                                                     			"symbol": None,
                                                     			"order_action": None,
                                                     			"quantity": None}
                                        			if order is not None and 'orderType' in order:
                                            				order_obj["order_type"] = order["orderType"]

                                        			if order is not None and 'orderId' in order:
                                            				order_str += "Order "
                                        			if instrument is not None and 'Product' in instrument and 'securityType' in instrument["Product"]:
                                            				order_str += "Type: " + instrument["Product"]["securityType"] + " | "
                                            				order_obj["security_type"] = instrument["Product"]["securityType"]

                                        			if instrument is not None and 'orderAction' in instrument:
                                            				order_str += "Order Type: " + instrument["orderAction"] + " | "
                                            				order_obj["order_action"] = instrument["orderAction"]

                                        			if instrument is not None and 'orderedQuantity' in instrument:
                                            				order_str += "Quantity(Exec/Entered): " + str(
                                                			"{:,}".format(instrument["orderedQuantity"])) + " | "
                                            				order_obj["quantity"] = instrument["orderedQuantity"]

                                        			if instrument is not None and 'Product' in instrument and 'symbol' in instrument["Product"]:
                                            				order_str += "Symbol: " + instrument["Product"]["symbol"] + " | "
                                            				order_obj["symbol"] = instrument["Product"]["symbol"]

                                        			if details is not None and 'priceType' in details:
                                            				order_str += "Price Type: " + details["priceType"] + " | "
                                            				order_obj["price_type"] = details["priceType"]

                                        			if details is not None and 'orderTerm' in details:
                                            				order_str += "Term: " + details["orderTerm"] + " | "
                                            				order_obj["order_term"] = details["orderTerm"]

                                        			if details is not None and 'limitPrice' in details:
                                            				order_str += "Price: " + str(
                                                			'${:,.2f}'.format(details["limitPrice"])) + " | "
                                            				order_obj["limitPrice"] = details["limitPrice"]

                                        			if instrument is not None and 'filledQuantity' in instrument:
                                            				order_str += "Quantity Executed: " \
                                                         		+ str("{:,}".format(instrument["filledQuantity"])) + " | "
                                            				order_obj["quantity"] = instrument["filledQuantity"]

                                        			if instrument is not None and "averageExecutionPrice" in instrument:
                                            				order_str += "Price Executed: " + str(
                                                			'${:,.2f}'.format(instrument["averageExecutionPrice"])) + " | "

                                        			if details is not None and 'status' in details:
                                            				order_str += "Status: " + details["status"]

                        					ramble(w, mI, str(count) + ")\t" + order_str)
                        					count = 1 + count
                        					orderList.append(order["orderId"])

                	ramble(w, mI, str(count) + ")\t Order Options")
			orderList.append("Order Options")
			inputFrame = createFrame(w, 1, 0, 2, W)
			btns = createButtons(inputFrame, orderList, w, account, base_url, etrade, prev_orders, messageInterface=mI)
        	else:
        		# Handle errors
                	logger.debug("Response Body: %s", response_open.text)
                	if response_open is not None and response_open.headers['Content-Type'] == 'application/json' \
                		and "Error" in response_open.json() and "message" in response_open.json()["Error"] \
                        	and response_open.json()["Error"]["message"] is not None:
                        	output(w, mI, "Error: " + response_open.json()["Error"]["message"])
                	else:
                        	output(w, mI, "Error: Balance API service error")
        else:
        	# Handle errors
                logger.debug("Response Body: %s", response_open.text)
                if response_open is not None and response_open.headers['Content-Type'] == 'application/json' \
                        and "Error" in response_open.json() and "message" in response_open.json()["Error"] \
                        and response_open.json()["Error"]["message"] is not None:
                    output(w, mI, "Error: " + response_open.json()["Error"]["message"])
                else:
                    output(w, mI, "Error: Balance API service error")

    def view_orders(self, w, mI, account, etrade, base_url):
        global session, live
	"""
        Calls orders API to provide the details for the orders

        :param self: Pass in authenticated session and information on selected account
        """
        # URL for the API endpoint
        url = base_url + "/v1/accounts/" + account["accountIdKey"] + "/orders.json"

        # Add parameters and header information
	if (live):
        	headers = {"consumerkey": configLive["DEFAULT"]["CONSUMER_KEY"]}
	else:
		headers = {"consumerkey": configSandbox["DEFAULT"]["CONSUMER_KEY"]}
        params_open = {"status": "OPEN"}
        params_executed = {"status": "EXECUTED"}
        params_indiv_fills = {"status": "INDIVIDUAL_FILLS"}
        params_cancelled = {"status": "CANCELLED"}
        params_rejected = {"status": "REJECTED"}
        params_expired = {"status": "EXPIRED"}

        # Make API call for GET request
        response_open = session.get(url, header_auth=True, params=params_open, headers=headers)
        response_executed = session.get(url, header_auth=True, params=params_executed, headers=headers)
        response_indiv_fills = session.get(url, header_auth=True, params=params_indiv_fills, headers=headers)
        response_cancelled = session.get(url, header_auth=True, params=params_cancelled, headers=headers)
        response_rejected = session.get(url, header_auth=True, params=params_rejected, headers=headers)
        response_expired = session.get(url, header_auth=True, params=params_expired, headers=headers)

        prev_orders = []

        # Open orders
        logger.debug("Request Header: %s", response_open.request.headers)
        logger.debug("Response Body: %s", response_open.text)

        output(w, mI, "Orders:")
        # Handle and parse response
        if response_open.status_code == 204:
        	logger.debug(response_open)
                ramble(w, mI, "\nNone")
        elif response_open.status_code == 200:
                parsed = json.loads(response_open.text)
                logger.debug(json.dumps(parsed, indent=4, sort_keys=True))
                data = response_open.json()

                # Display list of open orders
                prev_orders.extend(self.print_orders(data, "\n\nOpen", w, mI))

        # Executed orders - not part of if
        logger.debug("Request Header: %s", response_executed.request.headers)
        logger.debug("Response Body: %s", response_executed.text)
        logger.debug(response_executed.text)

        ramble(w, mI, "\nExecuted Orders:")
        # Handle and parse response
        if response_executed.status_code == 204:
                logger.debug(response_executed)
                ramble(w, mI, "\nNone")
        elif response_executed.status_code == 200:
                parsed = json.loads(response_executed.text)
                logger.debug(json.dumps(parsed, indent=4, sort_keys=True))
                data = response_executed.json()

                # Display list of executed orders
                prev_orders.extend(self.print_orders(data, "\n\nExecuted", w, mI))

        logger.debug("Request Header: %s", response_rejected.request.headers)
        logger.debug("Response Body: %s", response_rejected.text)

        # Individual fills orders
        logger.debug("Request Header: %s", response_indiv_fills.request.headers)
        logger.debug("Response Body: %s", response_indiv_fills.text)

        ramble(w, mI, "\nIndividual Fills Orders:")
        # Handle and parse response
        if response_indiv_fills.status_code == 204:
                logger.debug("Response Body: %s", response_executed)
                ramble(w, mI, "\nNone")
        elif response_indiv_fills.status_code == 200:
                parsed = json.loads(response_indiv_fills.text)
                logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))
                data = response_indiv_fills.json()

                # Display list of individual fills orders
                prev_orders.extend(self.print_orders(data, "\n\nIndivisual Fills", w, mI))

        logger.debug("Request Header: %s", response_rejected.request.headers)
        logger.debug("Response Body: %s", response_rejected.text)

        # Cancelled orders
        logger.debug("Request Header: %s", response_cancelled.request.headers)
        logger.debug("Response Body: %s", response_cancelled.text)

        ramble(w, mI, "\nCancelled Orders:")
        # Handle and parse response
        if response_cancelled.status_code == 204:
                logger.debug(response_cancelled)
                ramble(w, mI, "\nNone")
        elif response_cancelled.status_code == 200:
                parsed = json.loads(response_cancelled.text)
                logger.debug(json.dumps(parsed, indent=4, sort_keys=True))
                data = response_cancelled.json()

                # Display list of open orders
                prev_orders.extend(self.print_orders(data, "\n\nCancelled", w, mI))

        # Rejected orders
        logger.debug("Request Header: %s", response_rejected.request.headers)
        logger.debug("Response Body: %s", response_rejected.text)

        ramble(w, mI, "\nRejected Orders:")
        # Handle and parse response
        if response_rejected.status_code == 204:
                logger.debug(response_executed)
                ramble(w, mI, "\nNone")
        elif response_rejected.status_code == 200:
                parsed = json.loads(response_executed.text)
                logger.debug(json.dumps(parsed, indent=4, sort_keys=True))
                data = response_executed.json()

                # Display list of open orders
                prev_orders.extend(self.print_orders(data, "\n\nRejected", w, mI))

        # Expired orders
        ramble(w, mI, "\nExpired Orders:")
        # Handle and parse response
        if response_expired.status_code == 204:
		logger.debug(response_executed)
                ramble(w, mI, "\nNone")
        elif response_expired.status_code == 200:
                parsed = json.loads(response_expired.text)
                logger.debug(json.dumps(parsed, indent=4, sort_keys=True))
                data = response_expired.json()

                # Display list of open orders
                prev_orders.extend(self.print_orders(data, "\n\nExpired", w, mI))
	inputFrame = createFrame(w, 1, 0, 2, W)
	btns = createButtons(inputFrame, mainMenuItems, w, account, base_url, etrade, prev_orders, messageInterface=mI)
