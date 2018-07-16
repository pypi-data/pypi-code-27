import pandas as pd
import os,time


def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts
def sort():

    from sys import argv
    myargs = getopts(argv)

    if '-i' in myargs:  # Example usage.
        textfile = os.path.abspath(myargs['-i'])
        split = textfile.split(os.path.sep)
        if split[0]=='C:' :
            split[0]='mnt'
            split[1]='mydata'
            join = os.path.join(*split)
            textfile = join
        if textfile[-1] is not '/':
            textfile = textfile + '/'
    else: textfile = '/mnt/mydata/kyuha/desktop/CP_Output/raw_images_1/'
    if '-o' in myargs:
        csvfile = myargs['-o']
    else: csvfile = '/mnt/mydata/kyuha/desktop/hi.csv'

    #cwd = os.path.abspath(os.path.dirname(__file__))
    #cwd = cwd.replace('sourcecode','')
    #cwd+textfile for normal script use in open func.
    #with open(textfile, 'r') as myfile:
    #    direc=myfile.read().strip()
    direc = textfile.strip()

    if direc[-1] is not '/':
        direc = direc + '/'

    from masksort import *
    masksort(direc)
    from UI_generator import *
    UI_generator(direc)
    ### below code means nothing, but needed for galaxy format ###
    d = {'dir':[direc]}
    df = pd.DataFrame(data=d)
    df.to_csv(csvfile,index=False, header=False)

    return('sort completed')
