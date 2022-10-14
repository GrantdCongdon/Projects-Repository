from ftplib import FTP
stockList = []
session = FTP("ftp.nasdaqtrader.com")
session.login()
session.cwd("Symboldirectory")
with open("nasdaqlisted.txt", "wb") as fp:
	session.retrbinary("RETR nasdaqlisted.txt", fp.write)
session.quit()
with open("nasdaqlisted.txt", "r") as f:
	nasdaq = f.readlines()
for line in nasdaq[1:-1]:
	data = line.split("|")
	etf = data[-1].strip()
	category = data[1]
	if (etf=="N" and (("common stock" in category) or ("Common Stock" in category)) and ("arrant" not in category)):
		stockList.append(data[0])
#print(stockList)
