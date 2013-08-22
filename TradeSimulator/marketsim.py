'''
Created on Dec 13, 2012

@author: Ivan Zerin
@contact: sphinks at newmail.ru
'''

import sys
import datetime as dt
import time as t
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from qstkutil import DataAccess as da
import qstkutil.qsdateutil as du
import csv

if len(sys.argv) < 4 and len(sys.argv) > 1:
	print "Use such format to run marketsim.py <startAmount> <orderFileName> <portfolioResultFileName>"
	sys.exit(0)

startPortfolioAmount = 1000000
ordersFile = 'orders.csv'
valuesFile = 'values.csv'

if (len(sys.argv) > 1):
	startPortfolioAmount = float(sys.argv[1])
	ordersFile = sys.argv[2]
	valuesFile = sys.argv[3]

# Get the data from the data store
storename = "Yahoo" # get data from our daily prices source
# Available field names: open, close, high, low, close, actual_close, volume
closefield = "close"
volumefield = "volume"

# Read oreders
print "Read oreders from " + ordersFile
orders = array(np.loadtxt(ordersFile,dtype='str',delimiter=',',
	comments='#',skiprows=0))
symbols=list()
dates=list()
for order in orders:
	if not order[3] in symbols:
		symbols.append(order[3])
	dates.append(dt.datetime(int(order[0]),int(order[1]),int(order[2])))
print "A list of the symbols we read in: "
print symbols

startday = min(dates)
endday = max(dates)

print "Trade dates: "
print startday
print endday

timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)
dataobj = da.DataAccess('Yahoo')
print __name__ + " reading data"
# Reading the Data
close = dataobj.get_data(timestamps, symbols, closefield)
	
# Completing the Data - Removing the NaN values from the Matrix
close = (close.fillna(method='ffill')).fillna(method='backfill')
#Simulate trade
eqity = {}
portfolio = {}
for symbol in symbols:
	portfolio[symbol] = 0
for time in timestamps:
	for order in orders:
		if time.year == int(order[0]) and time.month == int(order[1]) and time.day == int(order[2]):
			if order[4] == "Buy":
				startPortfolioAmount = startPortfolioAmount - close[order[3]][time]*int(order[5])
				portfolio[order[3]] += int(order[5])
			if order[4] == "Sell":
				startPortfolioAmount = startPortfolioAmount + close[order[3]][time]*int(order[5])
				portfolio[order[3]] -= int(order[5])
	eqity[time] = startPortfolioAmount
	keys = list(portfolio.keys())
	for key in keys:
		if portfolio[key] != 0:
			eqity[time] += portfolio[key]*close[key][time]
keys = sorted(list(eqity.keys()))

print "Write values to " + valuesFile
with open(valuesFile, 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for key in keys:
    	tmp = list()
    	tmp.append(key.year)
    	tmp.append(key.month)
    	tmp.append(key.day)
    	tmp.append(eqity[key])
    	spamwriter.writerow(tmp)