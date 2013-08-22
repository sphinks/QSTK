
import urllib
import string

def quotes(df, mf, yf, dt, mt, yt, simb, period):
    f = urllib.urlopen('http://195.128.78.52/GAZP_080201_100208.csv?d=d&market=1&em=' +
        str(simb)+'&df='+str(df)+'&mf='+str(mf)+'&yf='+str(yf)+'&dt='+str(dt)+'&mt='
        +str(mt)+'&yt='+str(yt)+'&p='+str(period)
        +'&f=GAZP_080201_100208&e=.csv&cn=GAZP&dtf=4&tmf=4&MSOR=0&sep=1&sep2=1&datf=5&at=1')

    header= f.readline()
    symbol_data=list()
    symbol_data.append (f.readline())
    while (len(symbol_data[-1]) > 0):
        symbol_data.append(f.readline())
    
    symbol_data.pop(-1) #The last element is going to be the string of length zero. We don't want to write that to file.
    #now writing data to file
    file_r= open ("1.csv", 'w')
    
    #Writing the header
    file_r.write (header)
    
    while (len(symbol_data) > 0):
        file_r.write (symbol_data.pop(0))
     
    file_r.close();

    #quot = f.read()
    #f.close()
    #return string.split(quot, '\n')[1:-1]
    return 0

qq = quotes(1, 0, 2010, 30, 0, 2010, 16842, 8)
#for q in qq:
#    print q[:-1]