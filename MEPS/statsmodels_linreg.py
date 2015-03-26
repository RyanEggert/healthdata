import pandas as pd
import statsmodels.formula.api as smf
from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt



dependent = 'TOTEXP12'
#independents = ['BMINDX53', 'AGE12X', 'C(HIDEG)']
independents = ['AGE12X', 'NOASPR53']


#note: collinearity between AGE and HIDEG
# explanatoryvariables = 'EMPHAGED'

h155 = DataSet('h155.pkl')
df = h155.df
df = cleanallerrs(df)

hichol = df[df.CHOLDX == 1]

formula = dependent +  ' ~ ' + independents[0]

for i in range(len(independents)-1):
    formula = formula + ' + ' + independents[i+1]

print formula

#model_all = smf.ols(formula, data=df)
model_hichol = smf.ols(formula, data=hichol)

#results_all = model_all.fit()
results_hichol = model_hichol.fit()

print  results_hichol.summary()
