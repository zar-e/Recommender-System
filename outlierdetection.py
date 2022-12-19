# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 20:29:37 2022

@author: mypc
"""

import numpy as np
import pandas as pd
from scipy import stats
#takes x as entire df, thresh as threshold , cl as a dataframe with 1 column
#returns the df without any rows who have a z value above the threshold
#returns a outlier-free DF
def outexter(x,thresh,cl):
    if type(cl)==str:
        floated=x[cl].apply(np.float64)
        z = np.abs(stats.zscore(floated))
        x['z']=z
        x=(x[x['z']<thresh])
        x=x.drop('z',axis=1)
        
#if cl is list of strings then 
#run cleaning code above with each value of the string of the indexer of
#the column to be cleaned
    else:
        for i in cl:
            x=outexter(x,thresh,i)
    return x

def cleaning(x,cl):
    #returns the x dataframe without any NaN values in the column cl
    if type(cl)==str:
        notnans=x[cl].apply(pd.isna)==False
        x=x[notnans]
        cltype=x[cl].apply(type)[1]
        sametype=x[cl].apply(type)==cltype
        x=x[sametype]
        
#if cl is list of strings then 
#run cleaning code above with each value of the string of the indexer of
#the column to be cleaned
    elif (type(cl)==type([])):
        for i in cl:
            x=cleaning(x,i)
    return x