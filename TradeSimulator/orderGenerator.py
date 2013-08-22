'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on March, 5, 2012

@author: Sourabh Bajaj
@contact: sourabhbajaj90@gmail.com
@summary: Event Profiler Tutorial
'''


import pandas 
from qstkutil import DataAccess as da
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
from datetime import timedelta
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep
import csv

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""

# Get the data from the data store
storename = "Yahoo" # get data from our daily prices source
# Available field names: open, close, high, low, close, actual_close, volume
closefield = "actual_close"
volumefield = "volume"
window = 10

def findEvents(symbols, startday, endday, marketSymbol,verbose=False):

	# Reading the Data for the list of Symbols.	
	timeofday=dt.timedelta(hours=16)
	timestamps = du.getNYSEdays(startday,endday,timeofday)
	dataobj = da.DataAccess('Yahoo')
	if verbose:
            print __name__ + " reading data"
	# Reading the Data
	close = dataobj.get_data(timestamps, symbols, closefield)
	
	# Completing the Data - Removing the NaN values from the Matrix
	close = (close.fillna(method='ffill')).fillna(method='backfill')

	
	# Calculating Daily Returns for the Market
	# tsu.returnize0(close.values)
	# SPYValues=close[marketSymbol]

	# Calculating the Returns of the Stock Relative to the Market 
	# So if a Stock went down 5$
	np_eventmat = copy.deepcopy(close)
	for sym in symbols:
		for time in timestamps:
			np_eventmat[sym][time]=np.NAN

	if verbose:
            print __name__ + " finding events"

	# Generating the Event Matrix
	# Event described is : The stock falls under 5$ 

	print "Write values to file"
	with open('orders1.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for symbol in symbols:

			for i in range(1,len(close[symbol])):
				if close[symbol][i-1] >= 7 and close[symbol][i] < 7 : # When stock drops under 5$ there is an event
					tradeDaysArray = close[symbol].index
					dateIn = tradeDaysArray[i]
					if (len(tradeDaysArray) >= (i + 5)):
						dateOut = tradeDaysArray[i + 5]
					else:
						dateOut = tradeDaysArray[len(tradeDaysArray)]
					tmp = list()
					tmp.append(dateIn.year)
					tmp.append(dateIn.month)
					tmp.append(dateIn.day)
					tmp.append(symbol)
					tmp.append('Buy')
					tmp.append('100')
					spamwriter.writerow(tmp)
					tmp = list()
					tmp.append(dateOut.year)
					tmp.append(dateOut.month)
					tmp.append(dateOut.day)
					tmp.append(symbol)
					tmp.append('Sell')
					tmp.append('100')
					spamwriter.writerow(tmp)
					np_eventmat[symbol][i]=1
			
	return np_eventmat


#################################################
################ MAIN CODE ######################
#################################################


dataobj = da.DataAccess('Yahoo');
symbols = dataobj.get_symbols_from_list("sp5002012");
symbols.append('SPY');

#symbols =['BFRE','ATCS','RSERF','GDNEF','LAST','ATTUF','JBFCF','CYVA','SPF','XPO','EHECF','TEMO','AOLS','CSNT','REMI','GLRP','AIFLY','BEE','DJRT','CHSTF','AICAF']
startday = dt.datetime(2008,1,1)
endday = dt.datetime(2009,12,31)
eventMatrix = findEvents(symbols,startday,endday,marketSymbol='SPY',verbose=True)

eventProfiler = ep.EventProfiler(eventMatrix,startday,endday,lookback_days=20,lookforward_days=20,verbose=True)

eventProfiler.study(filename="Quiz.pdf",plotErrorBars=True,plotMarketNeutral=True,plotEvents=False,marketSymbol='SPY')


