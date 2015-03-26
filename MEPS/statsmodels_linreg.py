import pandas as pd
import statsmodels.formula.api as smf
from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt



dependent = 'TOTEXP12'
#independents = ['BMINDX53', 'AGE12X', 'C(HIDEG)']
independents = ['C(NOASPR53)', 'C(CHNEVER)', 'OHRTAGED', 'CHDAGED', 'ADHECR42', 'ADSPRF42', 'ADILWW42' ] #, 'C(RTHLTH31)', 'AGE12X','DENTCK53', 'ADLIST42' 
#'C(CHOLCK53)'


#R2 went down from .64 to .51 when added 'ADEZUN42'... what?
#C(OHRTAGED) increases R2 to 

#note: collinearity between AGE and HIDEG
# explanatoryvariables = 'EMPHAGED'

h155 = DataSet('h155.pkl')
df = h155.df
df = cleanallerrs(df)

#df['CHNEVER'] = df['CHOLCK53'] >= 3 


hichol = df[df.CHOLDX == 1]

formula = dependent +  ' ~ ' + independents[0]

for i in range(len(independents)-1):
    formula = formula + ' + ' + independents[i+1]

print formula

model_all = smf.ols(formula, data=df)
model_hichol = smf.ols(formula, data=hichol)

results_all = model_all.fit()
results_hichol = model_hichol.fit()

#print results_all.rsquared
print results_hichol.summary()
