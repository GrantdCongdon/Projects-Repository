#!/usr/bin/env python
from __future__ import print_function
import webbrowser
import json
import logging
import configparser
import sys
import requests
from rauth import OAuth1Service
from logging.handlers import RotatingFileHandler
from accounts import Accounts
from market import Market
from Tkinter import *
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from time import sleep
import algotrade
from retrying import retry
# universal variables
menuItems = ["Sandbox Login", "Live Login", "Exit"]
textCodeItems = ["Accept", "Go Back"]
mainMenuItems = ["Get Market Quotes", "Begin Algotrading", "Manage Accounts", "Exit"]
screenWidth=100
labelWidth=12
live=False
# load configuration file
configLive = configparser.ConfigParser()
configLive.read('live/config.ini')
configSandbox = configparser.ConfigParser()
configSandbox.read('sandbox/config.ini')
# create tkinter window
w = Tk()
w.title("AlgoTrader")
# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("python_client.log", maxBytes=5*1024*1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)
#browser
opts = Options()
opts.set_headless()
@retry(stop_max_attempt_number=3)
def signIn(authorize_url, mI, usernameP, passwordP):
	output(mI, "Logging in...")
	browser = Firefox(options=opts)
	browser.get(authorize_url)
	etradeUsername = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "USER")))
	etradePassword = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "PASSWORD")))
	logon = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.ID, "logon_button")))
	etradeUsername.send_keys(usernameP)
	etradePassword.send_keys(passwordP)
	logon.click()
	acceptAgreement = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.NAME, "submit")))
	sleep(1)
	acceptAgreement.click()
	WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "api-footer")))
	codeBox = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.TAG_NAME, "input")))
	code = codeBox.get_attribute('value')
	browser.close()
	return code
# main function for handling options
def click(key, etrade, etrade2, y, mI, usr, passwd, y2):
	global textCode, request_token, request_token_secret, base_url, inputFrame, buttonFrame, session, w, live, username, password
	if (key==menuItems[0]):
		y.destroy()
		usr = str(username.get())
		passwd = str(password.get())
		y2.destroy()
		if (usr==""):
			usr = ""
		if (passwd==""):
			passwd=""
		base_url = configSandbox["DEFAULT"]["SANDBOX_BASE_URL"]
		# Step 1: Get OAuth 1 request token and secret
		request_token, request_token_secret = etrade.get_request_token(params={"oauth_callback": "oob", "format": "json"})
		# Step 2: Go through the authentication flow. Login to E*TRADE.
		# After you login, the page will provide a text code to enter.
		authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
		#webbrowser.open(authorize_url)
		text_code = signIn(authorize_url, mI, usr, passwd)
		session = etrade.get_auth_session(request_token, request_token_secret, params={"oauth_verifier": text_code})
		buttonFrame = main_menu(base_url, mI, etrade, etrade2, usr, passwd)
		live = False
		output(mI, "Login Successful")
	elif (key==menuItems[1]):
		y.destroy()
		usr = str(username.get())
		passwd = str(password.get())
		y2.destroy()
		if (usr==""):
                        usr = ""
                if (passwd==""):
                        passwd=""
		base_url = configLive["DEFAULT"]["PROD_BASE_URL"]
		# Step 1: Get OAuth 1 request token and secret
		request_token, request_token_secret = etrade2.get_request_token(params={"oauth_callback": "oob", "format": "json"})
		# Step 2: Go through the authentication flow. Login to E*TRADE.
		# After you login, the page will provide a text code to enter.
		authorize_url = etrade2.authorize_url.format(etrade2.consumer_key, request_token)
		#webbrowser.open(authorize_url)
		text_code = signIn(authorize_url, mI, usr, passwd)
		# Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
		session = etrade2.get_auth_session(request_token, request_token_secret, params={"oauth_verifier": text_code})
		buttonFrame = main_menu(base_url, mI, etrade, etrade2, usr, passwd)
		live = True
		output(mI, "Login Succcessful")
	elif (key==menuItems[2]):
		w.destroy()
		exit()
	elif (key==textCodeItems[0] and not live):
		text_code = textCode.get()
		textCode.destroy()
        	buttonFrame.destroy()
		# Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
        	session = etrade.get_auth_session(request_token, request_token_secret, params={"oauth_verifier": text_code})
		buttonFrame = main_menu(base_url, mI, etrade, etrade2, usr, passwd)
		output(mI, "Login Successful")
	elif (key==textCodeItems[0] and live):
		text_code = textCode.get()
		textCode.destroy()
		buttonFrame.destroy()
		session = etrade2.get_auth_session(request_token, request_token_secret, params={"oauth_verifier": text_code})
		buttonFrame = main_menu(base_url, mI, etrade, etrade2, usr, passwd)
		output(mI, "Login Succcessful")
	elif (key==textCodeItems[1]):
		inputFrame.destroy()
		buttonFrame.destroy()
		btns = createFrame(1, 0, 2, W)
        	createButtons(btns, menuItems, etrade, etrade2, usr, passwd, messageInterface=mI)
		output(mI, "")
	elif (key==mainMenuItems[0] and not live):
		buttonFrame.destroy()
		market = Market(session, base_url, w, mI, etrade, live, usr, passwd)
		market.quotes()
	elif (key==mainMenuItems[2] and not live):
		buttonFrame.destroy()
		accounts = Accounts(session, base_url, w, mI, etrade, live, usr, passwd)
		accounts.account_list()
	elif (key==mainMenuItems[1] and not live):
		buttonFrame.destroy()
		algoTradeMenu = Accounts(session, base_url, w, mI, etrade, live, usr, passwd)
		algoTradeMenu.algoMainMenu()
	elif (key==mainMenuItems[0] and live):
		buttonFrame.destroy()
		market = Market(session, base_url, w, mI, etrade2, live, usr, passwd)
		market.quotes()
	elif (key==mainMenuItems[2] and live):
		buttonFrame.destroy()
		accounts = Accounts(session, base_url, w, mI, etrade2, live, usr, passwd)
		accounts.account_list()
	elif (key==mainMenuItems[1] and live):
		buttonFrame.destroy()
		algotradeMenu = Accounts(session, base_url, w, mI, etrade2, live, usr, passwd)
		algoTradeMenu.algoMainMenu()
	elif (key==mainMenuItems[3]):
		w.destroy()
		exit()
	else:
		output(mI, "Error")
# function for creating tkinter frames
def createFrame(row, column, columnspan, stick):
    display = Frame(w)
    display.grid(row=row, column=column, columnspan=columnspan, sticky=stick)
    return display
# function for creating buttons
def createButtons(y, buttons, etrade, etrade2, username, password, messageInterface=None, width=18, stick=S, y2=None):
        r=0
        c=0
        for b in buttons:
                def cmd(x=b):
                        click(x, etrade, etrade2, y, messageInterface, username, password, y2=y2)
                Button(y, text=b, width=width, command=cmd).grid(row=r, column=c,sticky=stick)
                c=c+1
                if (c>5):
                        c=0
                        r=r+1
# function for creating a text interface
def createInterface(y, r, c, stick):
    interface = Text(y, width=screenWidth, height=32, bg="Black", fg="White", state="disabled", font=("Times",12))
    interface.grid(row=r, column=c, sticky=stick)
    return interface
# printing on the text interface
def output(y, message):
    y.config(state="normal")
    y.delete(1.0, END)
    y.insert(END, message)
    y.config(state="disabled")
    w.update()
    return 0
def oauth():
	global username, password
        etrade = OAuth1Service(
        name="etrade",
        consumer_key=configSandbox["DEFAULT"]["CONSUMER_KEY"],
        consumer_secret=configSandbox["DEFAULT"]["CONSUMER_SECRET"],
        request_token_url="https://api.etrade.com/oauth/request_token",
        access_token_url="https://api.etrade.com/oauth/access_token",
        authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        base_url="https://api.etrade.com")

	etrade2 = OAuth1Service(
	name="etrade",
        consumer_key=configLive["DEFAULT"]["CONSUMER_KEY"],
        consumer_secret=configLive["DEFAULT"]["CONSUMER_SECRET"],
        request_token_url="https://api.etrade.com/oauth/request_token",
        access_token_url="https://api.etrade.com/oauth/access_token",
        authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        base_url="https://api.etrade.com")

        firstMenu = createFrame(0, 0, 2, N)
        text = createInterface(firstMenu, 0, 0, N)
	loginFrame = createFrame(1, 0, 2, W)
	username = Entry(loginFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
	username.grid(row=0, column=1, sticky=W)
	usernameLabel = Label(loginFrame, width=labelWidth, height=1, text="Username: ").grid(row=0, column=0, sticky=W)
	password = Entry(loginFrame, width=screenWidth-labelWidth, background="black", fg="white", insertbackground="white")
	password.grid(row=1, column=1, sticky=W)
	passwordLabel = Label(loginFrame, width=labelWidth, height=1, text="Password: ").grid(row=1, column=0, sticky=W)
        btns = createFrame(2, 0, 2, W)
        createButtons(btns, menuItems, etrade, etrade2, username, password, messageInterface=text, y2=loginFrame)
	output(text, "Welcome to the E*trade algorithmic trader and account manager! Login with either a sandbox or live key by pressing sandbox login or live login")
	return etrade, etrade2
def main_menu(base_url, mI, etrade, etrade2, username, password):
        """
        Provides the different options for the sample application: Market Quotes, Account List

        :param session: authenticated session
        """
	buttonFrame = createFrame(1, 0, 2, W)
	btns = createButtons(buttonFrame, mainMenuItems, etrade, etrade2, username, password, messageInterface=mI)
	return buttonFrame

oauth()
w.mainloop()
