import pandas as pd
import statsmodels.formula.api as smf
from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt



dependent = 'TOTEXP12'
    #WHOLE POPULATION
#independents = ['OHRTAGED', 'CHDAGED', 'C(ADHECR42)', 'C(ADSPRF42)', 'C(ADILWW42)', 'C(DECIDE42)']
    #HIGH CHOLESTEROL
independents = ['C(BADHLTH)', 'C(INS12X)', 'IPNGTD12', 'C(ARTHDX)', 'ADAPPT42', 'AGE12X', 'BMINDX53', 'C(RICH)', 'C(COGLIM31)'] #, 'POVLEV12', 'C(RTHLTH31)', 'AGE12X','DENTCK53', 'ADLIST42', 'C(RESPCT42)' 'C(ADILWW42)', 'C(ADSPRF42)''BMINDX53', 'AGE12X', 
#AGE12X and ARTHDX are interchangeable! Switched them out, had same R^2 value.     
#None of the condition variables affect total cost aside from ARTHDX

#what do all the numbers mean?
#BMI relationship...what is it?
#perceived health -- what is it?
#age + bmi or total prescriptions?


#INSAT12X, INS12X
#, ,   'BMINDX53'



    #CORONARY HEART DISEASE
#independents = ['C(NOASPR53)', 'OHRTAGED','CHDAGED', 'C(ADHECR42)', 'C(ADSPRF42)', 'C(ADILWW42)', 'C(DECIDE42)']

#including 'C(LANGPR42)' made R2 1, everything nan...what?

#RESPCT42: Does provider ask about and show respect for medical, traditional, and alternative treatments that the person is happy with 
#DECIDE42: Does provider ask the person to help make decisions between a choice of treatments (DECIDE42)
#ADILWW42: SAQ 12 Mos: Got Care When Needed Ill/Inj
#ADHECR42: SAQ 12 Mos: Rating of Health care
#ADSPRF42: SAQ 12Mos: How Esy Getting Spec Referral IF needed to see a specialist


#R2 went down from .64 to .51 when added 'ADEZUN42'

#note: collinearity warning with two heart-disease variables OHRTAGED and CHDAGED?

h155 = DataSet('h155.pkl')
df = h155.df
df = cleanallerrs(df)

df['BADHLTH'] = df['RTHLTH31'] >= 4
df['EXPHLTH'] = 10**(df['RTHLTH31']**2)
df['PROBLEM'] = df['MDUNPR42'] == 1
df['CHOLCKYR'] = df['CHOLCK53'] == 1
df['BPCHKYR'] = df['BPCHEK53'] == 1
df['RICH'] = df['POVCAT12'] ==5

#group = df[(df.CHOLDX == 1) & (df.CHOLCK53 == 5)]
#print len(group['DUPERSID'].values)

hichol = df[df.CHOLDX == 1]
cheartd = df[df.CHDDX == 1]




formula = dependent +  ' ~ ' + independents[0]

for i in range(len(independents)-1):
    formula = formula + ' + ' + independents[i+1]

print formula

model_all = smf.ols(formula, data=df)
model_hichol = smf.ols(formula, data=hichol)
#model_cheartd = smf.ols(formula, data=cheartd)

results_all = model_all.fit()
results_hichol = model_hichol.fit()
#results_cheartd = model_cheartd.fit()

#print results_all.rsquared
#print results_hichol.rsquared
#print results_cheartd.summary()
print results_hichol.summary()