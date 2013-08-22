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
import pandas

import qstkutil.tsutil as tsu

if len(sys.argv) < 3 and len(sys.argv) > 1:
	print "Use such format to run analisys.py <portfolioResultFileName> <benchmarkSymbol>"
	sys.exit(0)

# Get the data from the data store
storename = "Yahoo" # get data from our daily prices source
# Available field names: open, close, high, low, close, actual_close, volume
closefield = "close"
volumefield = "volume"

benchmarkSymbol = '$SPX'
valuesFile = 'values.csv'

if (len(sys.argv) > 1):
	valuesFile = sys.argv[1]
	benchmarkSymbol = sys.argv[2]

startday = dt.datetime(2011,1,10)
endday = dt.datetime(2011,12,21)

startPortfolioAmount = 1000000


# Read oreders
portfolioValue = array(np.loadtxt(valuesFile,dtype='str',delimiter=',',
	comments='#',skiprows=0))

values = portfolioValue[:,3]
day = portfolioValue[:,2]
month = portfolioValue[:,1]
year = portfolioValue[:,0]

#print values
dailyrets = []
timestamps = []
for i in range(1,len(values)):
	dailyrets.append((float(values[i])/float(values[i - 1])) - 1)
	timestamps.append(dt.datetime(int(year[i]),int(month[i]),int(day[i])))

#get spy
symbols=list()
symbols.append(benchmarkSymbol)

timeofday=dt.timedelta(hours=16)
timestampsSPY = du.getNYSEdays(startday,endday,timeofday)
dataobj = da.DataAccess('Yahoo')
print __name__ + " reading data"
# Reading the Data
closeSPY = dataobj.get_data(timestampsSPY, symbols, closefield)
closeTMP = dataobj.get_data(timestamps, symbols, closefield)
	
# Completing the Data - Removing the NaN values from the Matrix
closeSPY = (closeSPY.fillna(method='ffill')).fillna(method='backfill')
pricedat = closeSPY.values
dailyretsSPY = (pricedat[1:,:]/pricedat[0:-1,:]) - 1

plt.clf()
plt.cla()
newtimestampsSPY = closeSPY.index
newtimestamps = closeTMP.index
normdat = pricedat/pricedat[0,:]
normdatNew = values/values[0,:]
tsu.returnize0(normdat)
plt.plot(newtimestampsSPY,dailyretsSPY)
#plt.plot(newtimestampsSPY,dailyrets)
plt.axhline(y=0,color='r')
plt.ylabel('Adjusted Close')
plt.xlabel('Date')
savefig('adjustedclose.pdf',format='pdf')