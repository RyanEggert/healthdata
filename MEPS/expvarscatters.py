# scattermaker.py
import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt

# from VarSearch import search_vars

H155 = DataSet('h155.pkl')
df = H155.df

# diagnoses = search_vars('diagnosis', H155.varnames)
xvars = ['NOASPR53', 'CHOLCK53', 'OHRTAGED',
         'CHDAGED', 'ADHECR42', 'ADSPRF42', 'ADILWW42']


yvariable = 'TOTEXP12'
ydescr = 'Total Yearly Healthcare Expenses'


for xvar in xvars:
    this_df = df[[xvar, yvariable]].dropna()
    x = this_df[xvar]
    y = this_df[yvariable]

    tplt.Scatter(x, y)
    tplt.Config(ylabel=yvariable, xlabel=xvar, alpha=.001)
    # tplt.Show() moves overrides legend pos. for some reason.
    plt.savefig('./graphs/scattertests/%s.png' % xvar)
    plt.clf()

# # Correlations
# for data in groups:
#     thiscr = ts2.Corr(data['x'], data['y'])
#     print 'The correlation between %s and %s for %s is %5f' % (data['xname'], data['yname'], data['name'], thiscr)
