import pandas as pd
import statsmodels.formula.api as smf
from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt
from vargraph import iscat, varin, vargraph
import numpy as np



dependent = 'TOTEXP12'
#dependent = 'LOGTOTEXP'

    #WHOLE POPULATION
#independents = ['OHRTAGED', 'CHDAGED', 'C(ADHECR42)', 'C(ADSPRF42)', 'C(ADILWW42)', 'C(DECIDE42)']
    #HIGH CHOLESTEROL
independents = ['C(BADHLTH)', 'C(INS12X)', 'IPNGTD12', 'C(ARTHDX)',
                'ADAPPT42', 'AGE12X', 'BMINDX53', 'C(RICH)', 'C(COGLIM31)']

#'C(PHYEXE53)','C(CHOLCKYR)', 'C(BPCHKYR)', 
#'C(RESPECT)', 
#'C(NODECIDE)', 'C(GOODHC)', 'C(PROBLEM)', 'C(NOCARE)', 'C(NOEASYCARE)',  

#, 'C(PHYEXE53)', 'C(DEPRESSED)', 'POVLEV12', 'C(RTHLTH31)', 'AGE12X','DENTCK53', 'ADLIST42', 'C(RESPCT42)' 'C(ADILWW42)', 'C(ADSPRF42)''BMINDX53', 'AGE12X', 
#AGE12X and ARTHDX are interchangeable! Switched them out, had same R^2 value.     
#None of the condition variables affect total cost aside from ARTHDX

#what do all the numbers mean?
#BMI relationship...what is it?
#perceived health -- what is it?
#age + bmi or total prescriptions?

#INSAT12X, INS12X
#, ,   'BMINDX53'






h155 = DataSet('h155.pkl')
df = h155.df
df = cleanallerrs(df)

df['BADHLTH'] = df['RTHLTH31'] >= 4
df['EXPHLTH'] = 10**(df['RTHLTH31']**2)
df['PROBLEM'] = df['MDUNPR42'] == 1
df['CHOLCKYR'] = df['CHOLCK53'] == 1
df['FEWCHOLCK'] = df['CHOLCK53'] >= 5
df['BPCHKYR'] = df['BPCHEK53'] == 1
df['RICH'] = df['POVCAT12'] ==5
df['DEPRESSED'] = df['PHQ242']==6
df['GOODHC'] = df['ADHECR42'] >=8
df['BADHC'] = df['ADHECR42'] ==0
df['NODECIDE'] = df['DECIDE42'] == 1
df['RESPECT'] = df['RESPCT42'] == 4
df['NOCARE'] = df['ADILWW42'] == 1
df['NOEASYCARE'] = df['ADEGMC42'] == 1


#df['LOGTOTEXP'] = log10(df['TOTEXP12'])

df['LOGTOTEXP'] = np.log(df['TOTEXP12']).replace([np.inf, -np.inf], np.nan)
df['LOGTOTEXP'].dropna()
#print df['LOGTOTEXP']


#group = df[(df.CHOLDX == 1) & (df.CHOLCK53 == 5)]
#print len(group['DUPERSID'].values)

hichol = df[df.CHOLDX == 1]
cheartd = df[df.CHDDX == 1]
highbp = df[df.HIBPDX == 1]

#plotvars = ['C(BADHLTH)', 'C(INS12X)', 'IPNGTD12', 'C(ARTHDX)', 'ADAPPT42', 
#            'AGE12X', 'BMINDX53', 'C(RICH)', 'C(COGLIM31)', 'RTHLTH31', 'C(NOFAT53)', 
#            'C(CHOLCK53)', 'C(EXRCIS53)', 'C(PHYEXE53)', 'C(PHQ242)', 'C(DEPRESSED)', 'C(ADOVER42)', 'POVLEV12']
plotvars = independents + ['C(PHYEXE53)','C(CHOLCKYR)', 'C(BPCHKYR)', 'C(RESPECT)', 'C(NODECIDE)', 'C(GOODHC)', 'C(PROBLEM)', 'C(NOCARE)', 'C(NOEASYCARE)']

for var in plotvars:
    print (varin(var), dependent, iscat(var))
    if varin(var) == 'ADAPPT42':
        vargraph(hichol, varin(var), dependent, categorical=True, condition=False, log=True)
    else:
        vargraph(hichol, varin(var), dependent, categorical=iscat(var), condition=False, log=True)        




formula = dependent +  ' ~ ' + independents[0]

for i in range(len(independents)-1):
    formula = formula + ' + ' + independents[i+1]

print formula

model_all = smf.ols(formula, data=df)
model_hichol = smf.ols(formula, data=hichol)
model_highbp = smf.ols(formula, data=highbp)
#model_cheartd = smf.ols(formula, data=cheartd)

results_all = model_all.fit()
results_hichol = model_hichol.fit()
results_highbp = model_highbp.fit()
#results_cheartd = model_cheartd.fit()

#print results_all.rsquared
#print results_hichol.rsquared
#print results_cheartd.summary()
print results_hichol.summary()