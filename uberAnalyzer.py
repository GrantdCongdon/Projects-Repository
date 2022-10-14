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
from math import sqrt
def parseSorted(li):
	sList = []
	for stock in li:
		sList.append(stock[0])
	return sList
sortByOptions = {"beta":0, "deviance":3, "mRatio":10, "rsi":11, "rVolume":12, "swing":13, "kst":15, "macd":16}
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
startRange = 0
endRange = len(fileList)
sortBy = ["beta", "deviance", "mRatio", "rsi", "rVolume", "swing", "kst", "macd"]
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
betasList = []
devsList = []
mRatiosList = []
rsisList = []
rVolumesList = []
swingsList = []
kstsList = []
macdsList = []

nonbetasList = []
nondevsList = []
nonmRatiosList = []
nonrsisList = []
nonrVolumesList = []
nonswingsList = []
nonkstsList = []
nonmacdsList = []
for dict in fileDataList:
	sortedList = []
	i=0
	month = str(fileList[e+startRange])[9:-8]
	day = str(fileList[e+startRange])[11:-6]
	year = str(fileList[e+startRange])[13:-4]
	print("\n\n\n\n"+month+"-"+day+"-"+year)
	for category in sortBy:
		try:
			sortedDict = sorted(dict.items(), key=lambda c: c[1][i], reverse=False)
			transList = []
			for stock in sortedDict:
				transList.append(stock[0])
			sortedList.append(transList)
			print("\n"+category.upper())
			sNumber = len(transList)
			preMiddle = 0
			middle = 0
			postMiddle = 0
			for stock in transList:
				reprint = True
				for profitStock in totalProfit[e+startRange]:
					if (profitStock==stock):
						print(colored(stock, "green"), end=", ")
						reprint = False
						if (i==0 and sortedDict[0][1][i] is not None):
							betasList.append(sortedDict[0][1][i])
						elif (i==1 and sortedDict[0][1][i] is not None):
							devsList.append(sortedDict[0][1][i])
						elif (i==2 and sortedDict[0][1][i] is not None):
							mRatiosList.append(sortedDict[0][1][i])
						elif (i==3 and sortedDict[0][1][i] is not None):
							rsisList.append(sortedDict[0][1][i])
						elif (i==4 and sortedDict[0][1][i] is not None):
							rVolumesList.append(sortedDict[0][1][i])
						elif (i==5 and sortedDict[0][1][i] is not None):
							swingsList.append(sortedDict[0][1][i])
						elif (i==6 and sortedDict[0][1][i] is not None):
							kstsList.append(sortedDict[0][1][i])
						elif (i==7 and sortedDict[0][1][i] is not None):
							macdsList.append(sortedDict[0][1][i])
						else:
							continue
						break
				for profitStock in partialProfit[e+startRange]:
					if (profitStock==stock):
						print(colored(stock, "blue"), end=", ")
						reprint = False
						if (i==0 and sortedDict[0][1][i] is not None):
							betasList.append(sortedDict[0][1][i])
						elif (i==1 and sortedDict[0][1][i] is not None):
							devsList.append(sortedDict[0][1][i])
						elif (i==2 and sortedDict[0][1][i] is not None):
							mRatiosList.append(sortedDict[0][1][i])
						elif (i==3 and sortedDict[0][1][i] is not None):
							rsisList.append(sortedDict[0][1][i])
						elif (i==4 and sortedDict[0][1][i] is not None):
							rVolumesList.append(sortedDict[0][1][i])
						elif (i==5 and sortedDict[0][1][i] is not None):
							swingsList.append(sortedDict[0][1][i])
						elif (i==6 and sortedDict[0][1][i] is not None):
							kstsList.append(sortedDict[0][1][i])
						elif (i==7 and sortedDict[0][1][i] is not None):
							macdsList.append(sortedDict[0][1][i])
						else:
							continue
						break
				if (reprint):
					if (i==0 and sortedDict[0][1][i] is not None):
						nonbetasList.append(sortedDict[0][1][i])
					elif (i==1 and sortedDict[0][1][i] is not None):
						nondevsList.append(sortedDict[0][1][i])
					elif (i==2 and sortedDict[0][1][i] is not None):
						nonmRatiosList.append(sortedDict[0][1][i])
					elif (i==3 and sortedDict[0][1][i] is not None):
						nonrsisList.append(sortedDict[0][1][i])
					elif (i==4 and sortedDict[0][1][i] is not None):
						nonrVolumesList.append(sortedDict[0][1][i])
					elif (i==5 and sortedDict[0][1][i] is not None):
						nonswingsList.append(sortedDict[0][1][i])
					elif (i==6 and sortedDict[0][1][i] is not None):
						nonkstsList.append(sortedDict[0][1][i])
					elif (i==7 and sortedDict[0][1][i] is not None):
						nonmacdsList.append(sortedDict[0][1][i])
					print(stock, end=", ")
		except TypeError:
			continue
		finally:
			i+=1
	masterDataList.append(sortedList)
	e+=1
total = 0
standardDevs = {}
print("\nProfitable Beta")
positive=0
negative=0
pCounter=0
nCounter=0
for value in betasList:
	if (value>0):
		positive+=value
		pCounter+=1
	else:
		negative+=value*-1
		nCounter+=1
average = (sum(betasList))/(len(betasList))
pAverage = positive/pCounter
nAverage = negative/nCounter
print("Positive average: "+str(pAverage))
print("Negative average: "+str(nAverage))
for value in betasList:
	total+=(value-average)**2
bridge = total/len(betasList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))
for coreValue in betasList:
	for value in betasList:
		total+=(value-coreValue)**2
	bridge = total/len(betasList)
	sd = sqrt(bridge)
	standardDevs.update({coreValue:sd})
bridgeList = sorted(standardDevs.items(), key=itemgetter(1))
bridgeList2 = parseSorted(bridgeList)
#print("Values are cloest to "+str(bridgeList2[0]))
print(betasList)
total = 0
standardDevs = {}
print("\n\nProfitable Deviation")
average = sum(devsList)/len(devsList)
print("Average: "+str(average))
for value in devsList:
    total+=(value-average)**2
bridge = total/len(devsList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))
for coreValue in devsList:
    for value in devsList:
        total+=(value-coreValue)**2
    bridge = total/len(devsList)
    sd = sqrt(bridge)
    standardDevs.update({coreValue:sd})
bridgeList = sorted(standardDevs.items(), key=itemgetter(1))
bridgeList2 = parseSorted(bridgeList)
#print("Values are cloest to "+str(bridgeList2[0]))
print(devsList)
total = 0
standardDevs = []
print("\n\nProfitable mRatio")
average = sum(mRatiosList)/len(mRatiosList)
print("Average: "+str(average))
for value in mRatiosList:
    total+=(value-average)**2
bridge = total/len(mRatiosList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))
for coreValue in mRatiosList:
    for value in mRatiosList:
        total+=(value-coreValue)**2
    bridge = total/len(mRatiosList)
    sd = sqrt(bridge)
    standardDevs.append(sd)
#print("Values are cloest to "+str(standardDevs.index(max(standardDevs))))
print(mRatiosList)
total = 0
print("\n\nProfitable RSIs")
average = sum(rsisList)/len(rsisList)
print("Average: "+str(average))
for value in rsisList:
    total+=(value-average)**2
bridge = total/len(rsisList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))
for coreValue in rsisList:
    for value in rsisList:
        total+=(value-coreValue)**2
    bridge = total/len(rsisList)
    sd = sqrt(bridge)
    standardDevs.append(sd)
#print("Values are cloest to "+str(standardDevs.index(max(standardDevs))))
print(rsisList)
total = 0
print("\n\nProfitable rVolume")
average = sum(rVolumesList)/len(rVolumesList)
print("Average: "+str(average))
for value in rVolumesList:
    total+=(value-average)**2
bridge = total/len(rVolumesList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))
for coreValue in rVolumesList:
    for value in rVolumesList:
        total+=(value-coreValue)**2
    bridge = total/len(rVolumesList)
    sd = sqrt(bridge)
    standardDevs.append(sd)
#print("Values are cloest to "+str(standardDevs.index(max(standardDevs))))
print(rVolumesList)
total = 0
print("\n\nProfitable Swings")
average = sum(swingsList)/len(swingsList)
print("Average: "+str(average))
for value in swingsList:
    total+=(value-average)**2
bridge = total/len(swingsList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))
for coreValue in swingsList:
    for value in swingsList:
        total+=(value-coreValue)**2
    bridge = total/len(swingsList)
    sd = sqrt(bridge)
    standardDevs.append(sd)
#print("Values are cloest to "+str(standardDevs.index(max(standardDevs))))
print(swingsList)
total = 0
print("\n\nProfitable KST")
average = sum(kstsList)/len(kstsList)
print("Average: "+str(average))
for value in kstsList:
    total+=(value-average)**2
bridge = total/len(kstsList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))
for coreValue in kstsList:
    for value in kstsList:
        total+=(value-coreValue)**2
    bridge = total/len(kstsList)
    sd = sqrt(bridge)
    standardDevs.append(sd)
#print("Values are cloest to "+str(standardDevs.index(max(standardDevs))))
print(kstsList)
total = 0
print("\n\nProfitable MACDs")
average = sum(macdsList)/len(macdsList)
print("Average: "+str(average))
for value in macdsList:
    total+=(value-average)**2
bridge = total/len(macdsList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))
for coreValue in macdsList:
    for value in macdsList:
        total+=(value-coreValue)**2
    bridge = total/len(macdsList)
    sd = sqrt(bridge)
    standardDevs.append(sd)
#print("Values are cloest to "+str(standardDevs.index(max(standardDevs))))
print(macdsList)
#Nonprofit
total = 0
print("\nNonprofitable Beta")
positive=0
negative=0
pCounter=0
nCounter=0
for value in nonbetasList:
	if (value>0):
		positive+=value
		pCounter+=1
	else:
		negative+=value*-1
		nCounter+=1
average = (sum(nonbetasList))/(len(nonbetasList))
pAverage = positive/pCounter
nAverage = negative/nCounter
print("Positive average: "+str(pAverage))
print("Negative average: "+str(nAverage))
for value in nonbetasList:
    total+=(value-average)**2
bridge = total/len(nonbetasList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))

total = 0
print("\n\nNonprofitable Deviation")
average = sum(nondevsList)/len(nondevsList)
print("Average: "+str(average))
for value in nondevsList:
    total+=(value-average)**2
bridge = total/len(nondevsList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))

total = 0
print("\n\nNonprofitable mRatio")
average = sum(nonmRatiosList)/len(nonmRatiosList)
print("Average: "+str(average))
for value in nonmRatiosList:
    total+=(value-average)**2
bridge = total/len(nonmRatiosList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))

total = 0
print("\n\nNonprofitable RSIs")
average = sum(nonrsisList)/len(nonrsisList)
print("Average: "+str(average))
for value in nonrsisList:
    total+=(value-average)**2
bridge = total/len(nonrsisList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))

total = 0
print("\n\nNonprofitable rVolume")
average = sum(nonrVolumesList)/len(nonrVolumesList)
print("Average: "+str(average))
for value in nonrVolumesList:
    total+=(value-average)**2
bridge = total/len(nonrVolumesList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))

total = 0
print("\n\nNonprofitable Swings")
average = sum(nonswingsList)/len(nonswingsList)
print("Average: "+str(average))
for value in nonswingsList:
    total+=(value-average)**2
bridge = total/len(nonswingsList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))

total = 0
print("\n\nNonprofitable KST")
average = sum(nonkstsList)/len(nonkstsList)
print("Average: "+str(average))
for value in nonkstsList:
    total+=(value-average)**2
bridge = total/len(nonkstsList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))

total = 0
print("\n\nNonprofitable MACDs")
average = sum(nonmacdsList)/len(nonmacdsList)
print("Average: "+str(average))
for value in nonmacdsList:
    total+=(value-average)**2
bridge = total/len(nonmacdsList)
standardDev = sqrt(bridge)
print("Standard Deviation: "+str(standardDev))
