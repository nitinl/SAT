# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 22:41:43 2015

@author: Vaibhav
Gets the daily data for the stocks with MIN granularity in data folder in CSV format as text files.
The format for the name of the files is tickersymbol+'.txt' , e.g. for GOOG(Google) the intraday MIN data is in the path "data/GOOG.txt"
E.g. 
2015-09-10 09:30:11,110.0200,110.3100,109.9400,110.2500,1398100
(Local Time in Y-M-D H:M:S),close,high,low,open,volume

To convert the time in proper unix timestamp(UTC) format, first convert the time to unix-timestamp and then add 3600*9.5 if '.NS' is not present in ticker symbol.

Run twice daily after close of the market (NASDAQ(2:30-9:00 AM),NSE(5:00 PM-11:00PM))to update the files regularly.

"""

import urllib2
import time
import datetime

throwaway = datetime.datetime.strptime('20110101','%Y%m%d')
stocksToPull='AAPL','GOOG','TSLA','EBAY','SBIN.NS','AXISBANK.NS','ICICIBANK.NS','INFY.NS','WIPRO.NS','SUNPHARMA.NS','BHARTIART.NS','IDEA.NS','HINDUNILVR-EQ.NS','LT.NS','ONGC.NS'
def pullData(stock):
	try:
		print 'Currently pulling',stock
		print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
		urlToVisit='http://chartapi.finance.yahoo.com/instrument/1.1/'+stock+'/chartdata;type=quote;range=1d/csv'
		saveFileLine='../data/'+stock+'.txt'

		try:
			readExistingData=open(saveFileLine,'r').read()
			splitExisting=readExistingData.split('\n')
			mostRecentLine=splitExisting[-2]
			lastUnix=mostRecentLine.split(',')[0]
			lastUnix=int(time.mktime(datetime.datetime.strptime(lastUnix, "%Y-%m-%d %H:%M:%S").timetuple()))
			# The retrived value to be converted to utc unix used indian(local timezone) but the stock belongs to NASDAQ hence the time difference.
			if '.NS' not in stock:
				lastUnix=int(lastUnix)+3600*9.5
			else:
				pass
		except Exception, e:
			print str(e)
			time.sleep(1)
			lastUnix=0
		saveFile=open(saveFileLine,'a')
		sourceCode=urllib2.urlopen(urlToVisit).read()
		splitSource=sourceCode.split('\n')

		for eachLine in splitSource:
			if ':' not in eachLine:
				splitLine=eachLine.split(',')
				if len(splitLine)==6:
					if int(splitLine[0]) > lastUnix:
						# if '.NS' is not there the time is for New York , hence the difference
						if '.NS' not in stock:
							adjusted_timestamp=int(splitLine[0])-3600*9.5
						else:
							adjusted_timestamp=int(splitLine[0])
						lineToWrite=eachLine.replace(splitLine[0],str(datetime.datetime.fromtimestamp(adjusted_timestamp).strftime('%Y-%m-%d %H:%M:%S')))+'\n'
						saveFile.write(lineToWrite)
		saveFile.close()

		print 'Pulled',stock
		print 'Sleeping ...'
		print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
		time.sleep(10)

	except Exception, e:
		print 'main loop',str(e)

while True:
	for eachStock in stocksToPull:
		pullData(eachStock)
	time.sleep(500)

