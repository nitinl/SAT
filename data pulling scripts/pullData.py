import urllib2
import time
import datetime

# pulls historic stock price data from yahoo finance api
def pullData(stock, extension='.txt', timeRange='1y'):
    try:
        print 'Currently pulling', stock
        print str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        
        saveFileName = stock+extension
        try:
            readExistingData = open(saveFileName, 'r').read()
            splitExisting = readExistingData.split('\n')
            mostRecentLine = splitExisting[-2]
            lastUnix = mostRecentLine.split(',')[0]
        except Exception, e:
            print str(e)
            time.sleep(1)
            lastUnix = 0
        
        urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range='+timeRange+'/csv'
        sourceCode = urllib2.urlopen(urlToVisit).read()
        splitSource = sourceCode.split('\n')
        
        saveFile = open(saveFileName,'a')
        
        for eachLine in splitSource:
            if 'values' not in eachLine:
                splitLine = eachLine.split(',')
                if len(splitLine) == 6:
                    if int (splitLine[0]) > int(lastUnix):
                        lineToWrite = eachLine + '\n'
                        saveFile.write(lineToWrite)
        
        saveFile.close()
        
        print 'Pulled',stock
        
    except Exception, e:
        print 'main loop', str(e)
        
# example usage:
pullData('INFY.NS', '.txt')
#  http://finance.yahoo.com/d/quotes.csv?s=AAPL+GOOG+MSFT