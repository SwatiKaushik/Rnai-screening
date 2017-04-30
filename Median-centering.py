#perform median centering of RNAi data
import sys
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
import numpy as np
stats1 = importr('stats')

def mediancentering(filename):
    median = filename.stack().median()
    mcentering = filename[list(filename)].apply (lambda x: x-median)
    df1 = filename.transpose()
    ttest = stats.ttest_1samp(df1,0).pvalue
    p_adjust = stats1.p_adjust(FloatVector(ttest), method = 'fdr')
    mcentering['rowmean'] = mcentering.mean(axis=1)
    mcentering['pvalue'] = ttest
    mcentering['fdr'] = p_adjust
    return mcentering

def splitstring(x):
    prefix, postfix = x.split(".")
    outputfile = prefix + "_mediancentering.txt"
    return outputfile
    
def outputfile(dataframe, stringname):
    outfile = np.round(dataframe, decimals=7 )
    outfile.to_csv(stringname, sep='\t')
   

file1 = sys.argv[1]
    
df = pd.read_csv(file1,sep="\t", header =0,index_col=0)
mcentering = mediancentering(df)
stringname = splitstring(file1)
outputfile(mcentering, stringname)

