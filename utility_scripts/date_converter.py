# -*- coding: utf-8 -*-
"""
This program will convert all the dates for the stock quotes data from unix-timestamp(UTC) to the local time for the stock in a readable format.
ie. NSE stocks to local time of my computer(i.e India) & NASDAQ stocks to local time of New York

It will come in handy for converting new data files. I have included unix-timestamp to local time conversion in daily-data puller.

The file name is in openFile and the stock ticker symbols in stocksToPull.The file should have one and only one dangling new line in the end.
Currently only NSE and NASDAQ time and stocks are supported.

@author: Vaibhav
"""
import time
import datetime

stocksToPull='AAPL','GOOG','TSLA','EBAY','SBIN.NS','AXISBANK.NS','ICICIBANK.NS','INFY.NS','WIPRO.NS','SUNPHARMA.NS','BHARTIART.NS','IDEA.NS','HINDUNILVR-EQ.NS','LT.NS','ONGC.NS'

def date_convert(stock):
	try:
		print 'Currently converting ' + stock
		print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
		openFile='../data/'+stock+'.txt'
		
		try:
			readExistingData=open(openFile,'r').read()
			splitExisting=readExistingData.split('\n')[0:-1]
		except Exception, e:
			print str(e)
			time.sleep(1)

		openedFile=open(openFile,'w')

		for eachLine in splitExisting:
			unix_timestamp=eachLine.split(',')[0]
			# if '.NS' is not there the time is for New York , hence the difference
			if '.NS' not in stock:
				new_unix_timestamp=int(unix_timestamp)-3600*9.5
			else:
				new_unix_timestamp=int(unix_timestamp)
			eachLine=eachLine.replace(unix_timestamp,str(datetime.datetime.fromtimestamp(new_unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')))
			lineTowrite=eachLine+'\n'
			openedFile.write(str(lineTowrite))

		openedFile.close()

		print 'Changed file'
		
	except Exception, e:
		print 'main loop',str(e)

for eachstock in stocksToPull:
	date_convert(eachstock)
	time.sleep(5)