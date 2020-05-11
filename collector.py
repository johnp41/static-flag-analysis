import os
import  re 
from operator import add
import numpy as np
import csv
"""
    collects the features from milepost output files
    output: list of features
"""
def collect():
    files = os.listdir()
    ag_list = []
    for f in files :
        print(f)
        with open(f,'rt') as fille :            
            text = fille.read()
            p = re.compile(r'ft[0-9][0-9]?=([0-9]*.?[0-9]+)')
            lis= p.findall(text)
            lis = [float(x) for x in lis]
            ag_list.append(lis)
    res = np.sum(ag_list,0)
    res = [round(x) for x in res]
    """
        delete to match cobayn.csv
    """
    del res[17]
    ##deuterj
    del res[23]
    ##trith
    del res[30]
    #keep only 53
    res=res[:53]
    os.chdir("../../")
    ## final feature-array
    return res

