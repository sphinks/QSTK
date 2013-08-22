'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on September, 12, 2011

@author: Tucker Balch
@contact: tucker@cc.gatech.edu
@summary: Example tutorial code.
'''

import qstkutil.qsdateutil as du
import qstkutil.tsutil as tsu
import qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
from pylab import *
import pandas

print pandas.__version__

#
# Prepare to read the data
#
symbols = ["RTS.SBER"]
#symbols = ["AAPL"]
startday = dt.datetime(2007,1,1)
endday = dt.datetime(2010,12,31)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

dataobj = da.DataAccess('Finam')
voldata = dataobj.get_data(timestamps, symbols, "volume",verbose=True)
close = dataobj.get_data(timestamps, symbols, "close",verbose=True)
actualclose = dataobj.get_data(timestamps, symbols, "actual_close",verbose=True)

print close.index
print close.values
