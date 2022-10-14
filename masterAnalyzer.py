from __future__ import division
from yahoofinancials import YahooFinancials
import yfinance as yf
from timeout_decorator import timeout
from time import sleep
import timeout_decorator
from ast import literal_eval
from operator import itemgetter
from termcolor import colored
from os import listdir, chdir
sortByOptions = {"beta":0, "50DayAverage":1, "200DayAverage":2, "deviance":3, "float":4, "cVolume":5, "aVolume":6, "baRatio":7, "growth":8, "pbRatio":9, "mRatio":10, "rsi":11, "rVolume":12, "swing":13, "kst":15, "macd":16}
masterDataList = []
with open("stockData/allData.txt", "r") as f:
        allData = f.readlines()
totalProfit = literal_eval(allData[0])
partialProfit = literal_eval(allData[1])
chdir("stockData")
fileList = listdir()
fileList.remove("allData.txt")
fileList.remove(".DS_Store")
chdir("../")
fileList = sorted(fileList, reverse=False)
sortBy = str(input("Enter what you want to sort by seperated by commas and no spaces: "))
sortBy = sortBy.split(",")
for fileNumber in range(len(fileList)):
	print(str(fileNumber)+" : "+fileList[fileNumber])
try:
	startRange = int(input("Enter start date by number (lowest is 0): "))
except ValueError:
	startRange = 0
try:
	endRange = int(input("Enter end date by number (largest is "+str(len(fileList))+"): "))
except ValueError:
	endRange = len(fileList)
#print(fileList[startRange:endRange])
if (sortBy==["all"]):
	sortBy = ["beta", "deviance", "float", "baRatio", "pbRatio", "mRatio", "rsi", "rVolume", "swing", "kst", "macd"]
fileDataList = []
highTrend = []
lowTrend = []
middleTrend = []
for category in sortBy:
	highTrend.append(0)
	lowTrend.append(0)
	middleTrend.append(0)
e=0
for file in fileList[startRange:endRange]:
	print(file)
	with open("stockData/"+file, "r") as f:
		data = f.read()
	data = literal_eval(data)
	stockDataDict = {}
	for stockData in data:
		categoryList = []
		for category in sortBy:
			try:
				if (stockData[sortByOptions[category]]==""):
					stockData[sortByOptions[category]] = None
				categoryList.append(stockData[sortByOptions[category]])
			except IndexError:
				categoryList.append(None)
				pass
		stockDataDict.update({stockData[14]:categoryList})
	fileDataList.append(stockDataDict)
for dict in fileDataList:
	sortedList = []
	i=0
	month = str(fileList[e+startRange])[9:-8]
	day = str(fileList[e+startRange])[11:-6]
	year = str(fileList[e+startRange])[13:-4]
	print("\n\n\n\n"+month+"-"+day+"-"+year)
	#print("\n\n\n\n")
	for category in sortBy:
		try:
			sortedDict = sorted(dict.items(), key=lambda c: c[1][i], reverse=False)
			transList = []
			for stock in sortedDict:
				transList.append(stock[0])
			sortedList.append(transList)
			print("\n"+category.upper())
			sNumber = len(transList)
			z=0
			preMiddle = 0
			middle = 0
			postMiddle = 0
			for stock in transList:
				reprint = True
				for profitStock in totalProfit[e+startRange]:
					if (profitStock==stock):
						print(colored(stock, "green"), end=", ")
						reprint = False
						if (len(transList)>2):
							if (sNumber//3>z):
								preMiddle+=2
							elif ((sNumber//3)<=z and (sNumber//3)*2>=z):
								middle+=2
							elif ((sNumber//3)*2<z):
								postMiddle+=2
							break
				for profitStock in partialProfit[e+startRange]:
					if (profitStock==stock):
						print(colored(stock, "blue"), end=", ")
						reprint = False
						if (len(transList)>2):
							if (sNumber//3>z):
								preMiddle+=1
							elif ((sNumber//3)<=z and (sNumber//3)*2>=z):
								middle+=1
							elif ((sNumber//3)*2<z):
								postMiddle+=1
							break
				if (reprint):
					pass
					print(stock, end=", ")
				z+=1
			#print("\n"+str(len(totalProfit[e]))+"/"+str(len(transList)))
			if (preMiddle>postMiddle and preMiddle>middle):
				lowTrend[i]+=1
			elif (middle>preMiddle and middle>postMiddle):
				middleTrend[i]+=1
			elif (postMiddle>preMiddle and postMiddle>middle):
				highTrend[i]+=1
			print("\nLow: "+str(preMiddle)+"\nHigh: "+str(postMiddle)+"\nMiddle: "+str(middle))
		except TypeError:
			continue
		finally:
			i+=1
	masterDataList.append(sortedList)
	e+=1
y=0
for category in sortBy:
	if (highTrend[y]>lowTrend[y]+middleTrend[y]):
		print("\nTrend is growing stocks have higher "+category+" by "+str(highTrend[y]-middleTrend[y]-lowTrend[y]))
	elif (middleTrend[y]>highTrend[y]+lowTrend[y]):
		print("\nTrend: Growing stocks have medium "+category+" by "+str(middleTrend[y]-highTrend[y]-lowTrend[y]))
	elif (lowTrend[y]>highTrend[y]+middleTrend[y]):
		print("\nTrend is growing stocks have lower "+category+" by "+str(lowTrend[y]-middleTrend[y]-highTrend[y]))
	y+=1
