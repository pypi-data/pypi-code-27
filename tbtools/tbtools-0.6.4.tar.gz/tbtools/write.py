'''Writing TxBLEND input/output files'''

import pandas as pd
import os
import calendar


def inflow(df, out_path, loc_string):
    '''
    Write the TxBLEND inflow input file
    
    Parameters
    ----------
    df : dataframe
        Dataframe of the inflow time series
        * must be continuous, hourly index that starts on 1/1 of
        first year and ends at 12/31 of last year
    out_path : string
        location where the file will be saved plus file name
    loc_string : string
        location string to indicate where the inflow is
        * must be 8 characters or less
        
    Example
    -------
    import tbtools as tbt
    
    tbt.write.inflow(df, 'desired/output/path', 'location')
    
    Returns
    -------
    None
    '''
    
    fout = open(out_path, 'w')
    
    yrs = range(df.index[0].year, df.index[-1].year + 1, 1)
    mnths = range(1, 13, 1)
    
    nd = []
    
    for y in yrs:
        for m in mnths:
            nd += [calendar.monthrange(y, m)[1]]
            
    c = 0
    
    for n in nd:
        line1 = '%4i,%2i,%2i' % (df.index[c].year,df.index[c].month,n)
        line2 = '%-9s%2i%2i' % (loc_string,df.index[c].month,1)
        line3 = '%-9s%2i%2i' % (loc_string,df.index[c].month,2)
        line4 = '%-9s%2i%2i' % (loc_string,df.index[c].month,3)

        for x in range(10):
            if df.ix[c+x][0] > 0:
                line2 += ('%6i' % df.ix[c+x])
            else:
                line2 += ('%6i' % 0)
        for x in range(10,20):
            if df.ix[c+x][0] > 0:
                line3 += ('%6i' % df.ix[c+x])
            else:
                line3 += ('%6i' % 0)
        for x in range(20,n):
            if df.ix[c+x][0] > 0:
                line4 += ('%6i' % df.ix[c+x])
            else:
                line4 += ('%6i' % 0)

        fout.write(line1+'\n'+line2+'\n'+line3+'\n'+line4+'\n')

        c+=n
        
    fout.close()
    

def gensal(df, out_path, loc_string):
    '''
    Write the TxBLEND boundary salinity concentration input file
    
    Parameters
    ----------
    df : dataframe
        Dataframe of the interpolated salinity values
        *must have a continuous, bihourly index
    out_path : string
        location where the file will be saved plus file name
    loc_string : string
        location string to indicate where the salinity data was colleged
        *e.g. 'OffGalves'
        
    Example
    -------
    import tbtools as tbt
    
    tbt.write.gensal(data, 'desired/output/path', 'OffGalves')
    
    Returns
    -------
    None
    '''
    fout = open(out_path,'w')
    for i in range(0,len(df),12):
        fout.write('%3i%3i%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6i %8s\n' % 
                  (df.index[i].month,df.index[i].day,
                   df.salinity[i],df.salinity[i+1],
                   df.salinity[i+2],df.salinity[i+3],
                   df.salinity[i+4],df.salinity[i+5],
                   df.salinity[i+6],df.salinity[i+7],
                   df.salinity[i+8],df.salinity[i+9],
                   df.salinity[i+10],df.salinity[i+11],
                   df.index[i].year,loc_string))
    fout.close()
    
def tide(df, out_path):
    '''
    Write the TxBLEND tide input file
    
    Parameters
    ----------
    df : dataframe
        Dataframe of the bihourly tide data
        *must have a continuous, bihourly index
    out_path : string
        location where the file will be saved plus file name
        
    Example
    -------
    import tbtools as tbt
    
    tbt.write.tide(data, 'desired/output/path')
    
    Returns
    -------
    None
    '''
    fout = open(out_path,'w')
    col = df.columns[0]
    for i in range(0,len(df),12):
        fout.write('%3i%3i%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f'
                   '%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6i %-8s\n' % 
                  (df.index[i].month,df.index[i].day,
                   df[col][i],df[col][i+1],
                   df[col][i+2],df[col][i+3],
                   df[col][i+4],df[col][i+5],
                   df[col][i+6],df[col][i+7],
                   df[col][i+8],df[col][i+9],
                   df[col][i+10],df[col][i+11],
                   df.index[i].year,col))
    fout.close()
    
    