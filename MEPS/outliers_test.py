import pandas as pd
import statsmodels.formula.api as smf
from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt

h155 = DataSet('h155.pkl')
df = h155.df
df = cleanallerrs(df)

dependent = 'TOTEXP12'

conditions = ['ADHDADDX', 'ANGIDX', 'ARTHDX', 'ASTHDX', 'BPMLDX', 'CANCERDX', 'CHDDX', 'CHOLDX', 'DIABDX', 'EMPHDX', 'HIBPDX', 'MIDX', 'OHRTDX', 'STRKDX']

cdf = ts2.Cdf(df[dependent])
tplt.Cdf(cdf, label=dependent+' CDF')
tplt.Config(xscale='log')
tplt.Show()

pmf = ts2.Pmf(df[dependent])
tplt.Pmf(pmf, label=dependent + ' PMF')
tplt.Config(xscale='log')
tplt.Show()


for condition in conditions:
    df_cond = df[df[condition]==1]
    df_nocond = df[df[condition]==2]
    num_cond = len(df_cond['DUPERSID'].values)
    num_nocond = len(df_nocond['DUPERSID'].values)

    cdf_cond = ts2.Cdf(df_cond[dependent])
    cdf_nocond = ts2.Cdf(df_nocond[dependent])
    pmf_cond = ts2.Pmf(df_cond[dependent])
    pmf_nocond = ts2.Pmf(df_nocond[dependent])

    tplt.Cdf(cdf_cond, label=dependent + ' with ' + condition + ': ' + str(num_cond))
    tplt.Cdf(cdf_nocond, label=dependent + ', no ' + condition + ': ' + str(num_nocond))
    tplt.Config(xscale='log')
    tplt.Show()

    tplt.Pmf(pmf_cond, label=dependent + ' with ' + condition + ': ' + str(num_cond))
    tplt.Pmf(pmf_nocond, label=dependent + ', no ' + condition + ': ' + str(num_nocond))
    tplt.Config(xscale='log', yscale='log')
    tplt.Show()


#group = df[(df.CHOLDX == 1) & (df.CHOLCK53 == 5)]
#print len(group['DUPERSID'].values)
