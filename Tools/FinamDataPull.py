'''
Short program to scrape historical price/volume data from Google Fianance.
into local CSV files that can be read and used by QSTK.

(c) 2013 by Ivan Zerin
'''

import urllib2
import urllib
import datetime
import sys
import os


def get_data(data_path, ls_symbols):

    #Create path if it doesn't exist
    if not (os.access(data_path, os.F_OK)):
        os.makedirs(data_path)

    #utils.clean_paths(data_path)   

    _now =datetime.datetime.now();
    miss_ctr=0; #Counts how many symbols we could get
    for symbol in ls_symbols:
        symbol_name = symbol
        if symbol[0] == '$':
            symbol = '^' + symbol[1:]

        symbol_data=list()
        #print "Getting " + str (symbol_name)
        symbol_code = get_symbol_code(symbol)
        
        try:
            #http://195.128.78.52/RTS.SBERP_130107_130107.csv?market=3&em=364&code=RTS.SBERP&df=7&mf=0&yf=2013&dt=7&mt=0&yt=2013&p=8&f=RTS.SBERP_130107_130107&e=.csv&cn=RTS.SBERP&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=3&sep2=1&datf=2&at=1
            url_get = urllib.urlopen('http://195.128.78.52/' + symbol + '.csv?d=d&market=3&em=' + symbol_code +
            '&df='+str(1)+'&mf='+str(0)+'&yf='+str(2007)+'&dt='+str(_now.day)+'&mt='
            +str(_now.month-1)+'&yt='+str(_now.year)+'&p='+str(8)
            +'&f=' + symbol + '&e=.csv&cn=GAZP&dtf=5&tmf=4&MSOR=0&sep=1&sep2=1&datf=5&at=1')

            header = url_get.readline()
            symbol_data.append (url_get.readline())
            while (len(symbol_data[-1]) > 0):
                symbol_data.append(url_get.readline())
            
            symbol_data.pop(-1) #The last element is going to be the string of length zero. We don't want to write that to file.
            #now writing data to file
            f= open (data_path + symbol_name + ".csv", 'w')
            
            #Writing the header
            f.write (header)
            
            while (len(symbol_data) > 0):
                f.write (symbol_data.pop(0))
             
            f.close();    
                        
        except urllib2.HTTPError:
            miss_ctr= miss_ctr+1
            print "Unable to fetch data for stock: " + str (symbol_name)
        except urllib2.URLError:
            print "URL Error for stock: " + str (symbol_name)
            
    print "All done. Got " + str (len(ls_symbols) - miss_ctr) + " stocks. Could not get " + str (miss_ctr) + " stocks."   

def get_symbol_code(symbol_name):
    d_symbols = {'RTS.SBER':'363'}
    print "Ask for symbol " + symbol_name + ":" + d_symbols[symbol_name]
    return d_symbols[symbol_name]

def read_symbols(s_symbols_file):
    ls_symbols=[]
    file = open(s_symbols_file, 'r')
    for f in file.readlines():
        j = f[:-1]
        ls_symbols.append(j)
    file.close()
    
    return ls_symbols  

def main():
    path = "../QSData/Finam/"
    #path = './'
    ls_symbols = read_symbols('symbols.txt')
    get_data(path, ls_symbols)

if __name__ == '__main__':
    main()