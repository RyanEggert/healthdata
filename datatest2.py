# import dataio as dio
import thinkstats2 as ts2
import thinkplot as tplt
import DataSet
import pdb
from random import choice

H155 = DataSet.DataSet('h155.pkl')

df = H155.df
print df.shape

dfr = df[df['INSCOPE'] == ]
print dfr.shape

c1 = choice(H155.varnames.keys())
c2 = choice(H155.varnames.keys())

print c1, H155.varnames[c1]
print c2, H155.varnames[c2]
