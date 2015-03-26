import pandas as pd
import statsmodels.formula.api as smf
from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt



dependent = 'TOTEXP12'
#independents = ['BMINDX53', 'AGE12X', 'C(HIDEG)']
independents = ['C(NOASPR53)', 'C(CHOLCK53)', 'OHRTAGED', 'CHDAGED', 'C(ADHECR42)', 'C(ADSPRF42)', 'C(ADILWW42)', 'C(DECIDE42)'] #, 'C(RTHLTH31)', 'AGE12X','DENTCK53', 'ADLIST42', 'C(RESPCT42)' 
#'C(CHOLCK53)'

#including 'C(LANGPR42)' made R2 1, everything nan...what?

#RESPCT42: Does provider ask about and show respect for medical, traditional, and alternative treatments that the person is happy with 
#DECIDE42: Does provider ask the person to help make decisions between a choice of treatments (DECIDE42)
#ADILWW42: SAQ 12 Mos: Got Care When Needed Ill/Inj
#ADHECR42: SAQ 12 Mos: Rating of Health care
#ADSPRF42: SAQ 12Mos: How Esy Getting Spec Referral IF needed to see a specialist


#R2 went down from .64 to .51 when added 'ADEZUN42'
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
#print results_hichol.rsquared
print results_hichol.summary()