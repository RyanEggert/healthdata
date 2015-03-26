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
diagnoses = ['NOASPR53', 'CHNEVER', 'OHRTAGED', 'CHDAGED', 'ADHECR42', 'ADSPRF42', 'ADILWW42' ]


xvariable = 'AGE12X'
xdescr = 'Age'
yvariable = 'TOTEXP12'
ydescr = 'Total Yearly Healthcare Expenses'


# groups = [{'name': 'All', 'x': df[xvariable], 'y': df[yvariable], 'xname': xvariable,
#             'yname': yvariable, 'xlabel': xdescr, 'ylabel': ydescr}]
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

colors = cm.jet(np.linspace(0, 1, num_sets))
print colors

for data, c in zip(groups, colors):
    tplt.Scatter(data['x'], data['y'], color=c, label=data['name'])
tplt.Config(ylabel=groups[0]['ylabel'], xlabel=groups[0][
            'xlabel'], legend=True, loc='upper left')
plt.show()  # tplt.Show() moves overrides legend pos. for some reason.

# Correlations
for data in groups:
    thiscr = ts2.Corr(data['x'], data['y'])
    print 'The correlation between %s and %s for %s is %5f' % (data['xname'], data['yname'], data['name'], thiscr)
