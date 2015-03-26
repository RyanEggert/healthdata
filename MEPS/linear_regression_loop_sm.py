import pandas as pd
import statsmodels.formula.api as smf

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt


def listfmla(variables):
    return ' + '.join(variables)


def getkey(item):
    return item[0]


dependentvariable = 'TOTEXP12'
# explanatoryvariables = 'EMPHAGED'

h155 = DataSet('h155.pkl')
df = h155.df

join = df
t = []
tprint = []
varlist = []
rsquareds = []
# explanvars = listfmla(explanatoryvariables)

for index, name in enumerate(join.columns):
    if index % 100 == 0:
        print '%s: Variable %d of %d.' % (name, index + 1, len(join.columns))

    try:
        joinclean = join[(join[name] > -1) & (join[dependentvariable] > -1)]
    except:
        print 'nope'
        continue
    try:
        if joinclean[name].var() < 1e-7:
            continue

        formula = dependentvariable + ' ~ ' + name
        model = smf.ols(formula, data=joinclean)
        if model.nobs < len(joinclean) / 2:
            continue

        results = model.fit()
    except (ValueError, TypeError):
        continue

    varlist.append(name)
    rsquareds.append(float(results.rsquared))
    t.append([results.rsquared, name, joinclean.shape])
    tprint.append(str((results.rsquared, name)))

t_sort = sorted(t, key=getkey, reverse=True)
# print rsquareds
# print all(type(x) is float for x in rsquareds)
# print type(rsquareds)
print max(rsquareds), min(rsquareds)
print t_sort
with open('datamining_%s_%s.txt' % (h155.name, dependentvariable), 'wb+') as textfile:
    textfile.writelines(str(t_sort))
