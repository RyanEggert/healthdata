# convertcatdata.py

from DataSet import DataSet
import thinkstats2 as ts2
import thinkplot as tplt
from matplotlib import pyplot as plt
import pandas as pd

h155 = DataSet('h155')
df = h155.df

catvar = df['ADEXPL42']

responses = h155.ADEXPL42.responses
print responses

print pd.get_dummies(catvar)
