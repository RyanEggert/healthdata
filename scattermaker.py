# scattermaker.py
import thinkstats2 as ts2
import thinkplot as tplt
from DataSet import DataSet
import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from VarSearch import search_vars

H155 = DataSet('h155.pkl')
df = H155.df

diagnoses = search_vars('diagnosis', H155.varnames)

xvariable = 'HRWG31X'
xdescr = 'Hourly Wage'
yvariable = 'TOTEXP12'
ydescr = 'Total Yearly Healthcare Expenses'


groups = []
for diagnosis in diagnoses:
    afflicted = df[
        (df[diagnosis] == 1) & (df[xvariable] > 0) & (df[yvariable] > 0)]
    xvar = afflicted[xvariable]
    yvar = afflicted[yvariable]
    assert len(xvar) == len(yvar)
    data = {'name': diagnosis, 'x': xvar, 'y': yvar, 'xname': xvariable,
            'yname': yvariable, 'xlabel': xdescr, 'ylabel': ydescr}
    groups.append(data)

num_sets = len(groups)

colors = cm.rainbow(np.linspace(0, 1, num_sets))

for data, c in zip(groups, colors):
    tplt.Scatter(data['x'], data['y'], color=c, label=data['name'])
tplt.Config(ylabel=groups[0]['ylabel'], xlabel=groups[0][
            'xlabel'], yscale='log', xscale='log', legend=True, loc=6)
plt.show()  # tplt.Show() moves overrides legend pos. for some reason.

# Correlations
for data in groups:
    thiscr = ts2.Corr(data['x'], data['y'])
    print 'The correlation between %s and %s for %s is %5f' % (data['xname'], data['yname'], data['name'], thiscr)
