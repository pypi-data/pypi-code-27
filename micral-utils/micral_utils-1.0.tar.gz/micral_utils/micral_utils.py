
import numpy as np

def printDict(d, printType=False, nbtab=0):
    if isinstance(d,dict):
        for k, v in d.items():
            data = "\t"*nbtab+str(k) + " "
            if printType:
                data += str(type(v)).split('\'')[1] + " "
            if isinstance(v,np.ndarray):
                data += "shape="+str(v.shape)
            elif not isinstance(v,dict):
                data += str(v)
            print(data)
            printDict(v, printType, nbtab+1)

def removeEmptyDict(d):
    if not isinstance(d,dict):
        return d
    cleaned_dict = dict()
    for k,v in d.items():
        r = removeEmptyDict(v)
        if r is not None:
            cleaned_dict[k] = r
    if len(cleaned_dict)==0:
        return None
    else:
        return cleaned_dict
