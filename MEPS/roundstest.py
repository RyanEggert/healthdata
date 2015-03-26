from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt

h155 = DataSet('h155.pkl')
df = h155.df

print df[['DUPERSID', 'RTHLTH31', 'RTHLTH42', 'RTHLTH53']]
