import pandas as pd
import statsmodels.formula.api as smf
from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt
from vargraph import iscat, varin, vargraph
import numpy as np



dependent = 'LOGTOTEXP'
#dependent = 'LOGTOTEXP'

    #WHOLE POPULATION
#independents = ['OHRTAGED', 'CHDAGED', 'C(ADHECR42)', 'C(ADSPRF42)', 'C(ADILWW42)', 'C(DECIDE42)']
    #HIGH CHOLESTEROL
#independents = ['C(BADHLTH)', 'C(INS12X)', 'C(ARTHDX)','C(AIDHLP31)', 'C(COGLIM31)', 'C(ACTLIM31)', 'C(DIABDX)', 
#'C(CANCERDX)', 'C(WRGLAS42)', 'AGE12X', 'BMINDX53']  #'C(FEWCHECK)', 'C(GOODHC)', 

independents = ['C(ACTLIM31)', 'C(AIDHLP31)','AGE12X','C(ARTHDX)', 'C(BADHLTH)','BMINDX53','C(CANCERDX)', 'C(COGLIM31)',  'C(DIABDX)', 'C(INS12X)',
'C(WRGLAS42)']  #'C(FEWCHECK)', 'C(GOODHC)', 

#check53 can handle all values!!! awesome!


prov_mod = ['C(PHYEXE53)','C(CHOLCKYR)', 'C(BPCHKYR)','C(RESPECT)','C(NODECIDE)', 'C(GOODHC)', 'C(PROBLEM)',
'C(ENUFTIME)', 'C(FEWDENTCHK)', 'C(NOPHONE)', 'C(NOAFTERHRS)', 'C(NOFLUSHT)']
#prov_mod = ['C(NOLISTEN)', 'C(ENUFTIME)', 'C(HARDTOGET)', 'C(FEWDENTCHK)', 'C(OFFHOU42)', 'C(NOPHONE)', 'C(NOAFTERHRS)', 'C(NOFAT53)', 'C(NOFLUSHT)', 'C(PROBLEMDNT)']
#all_prov_mod = prov_mod + ['C(NOFAT53)', 'C(EXRCIS53)', 'C(ASPRIN53)', 'C(PSAYR)', 'C(HYSTER53)', 'C(PAPYR)']



h155 = DataSet('h155.pkl')
df = h155.df
df = cleanallerrs(df)

#modified model vars
df['BADHLTH'] = df['RTHLTH31'] >= 4

#core healthcare quality/preventative care vars
df['PROBLEM'] = df['MDUNPR42'] == 1
df['CHOLCKYR'] = df['CHOLCK53'] == 1
df['BPCHKYR'] = df['BPCHEK53'] == 1
df['GOODHC'] = df['ADHECR42'] >=8
df['NODECIDE'] = df['DECIDE42'] == 1
df['RESPECT'] = df['RESPCT42'] == 4
df['ENUFTIME'] = df['ADPRTM42'] >= 3
df['FEWDENTCHK'] = df['DENTCK53'] >= 3
df['NOPHONE'] = df['PHNREG42'] <= 2
df['NOAFTERHRS'] = df['AFTHOU42'] <= 2
df['NOFLUSHT'] = df['FLUSHT53'] >= 5

#additional healthcare quality/preventative care vars
df['FEWCHECK'] = df['CHECK53'] >= 2     #PREVENTATIVE
df['PSAYR'] = df['PSA53'] == 1
df['PAPYR'] = df['PAPSMR53'] == 1
df['BRSTYR'] = df['BRSTEX53'] == 1
df['MAMMOYR'] = df['MAMOGR53'] == 1
df['STOOLYR'] = df['BSTST53'] == 1
df['COLONOSYR'] = df['CLNTST53'] == 1
df['SIGMOIDYR'] = df['SGMTST53'] == 1
df['SEATBELT'] = df['SEATBE53'] == 1

df['HARDTOGET'] = df['DFTOUS42'] <= 2   #QUALITY
df['PROBLEMDNT'] = df['DNUNPR42'] == 1
df['NOLISTEN'] = df['ADLIST42'] <= 2
df['LITTLECARE'] = df['ADILWW42'] <= 2
df['FEWAPPT'] = df['ADRTWW42'] <= 2
df['NOTEASY'] = df['ADEGMC42'] <= 2
df['NOEXPLAIN'] = df['ADEXPL42'] <= 2
df['NODRRESPCT'] = df['ADRESP42'] <= 2
df['NOINSTRUC'] = df['ADINST42'] == 2
df['NOUNDERST'] = df['ADEZUN42'] <= 2
df['NODRDESC'] = df['ADTLHW42'] <= 2
df['NOFORMHELP'] = df['ADFHLP42'] <= 2
df['NOEZREF'] = df['ADSPRF42'] <= 2
df['NOASKTREAT'] = df['TREATM42'] <= 2
df['NOEXPLOPT'] = df['EXPLOP42'] <= 2






df['LOGTOTEXP'] = np.log10(df['TOTEXP12']).replace([np.inf, -np.inf], np.nan)
df['LOGTOTEXP'].dropna()




hichol = df[df.CHOLDX == 1]

plotvars = independents + prov_mod

for var in plotvars:
    print (varin(var), dependent, iscat(var))
    if(iscat(var)):
        by_var = hichol.groupby(var[2:-1])
        print(by_var.size())
    if varin(var) == 'ADAPPT42':
        vargraph(hichol, varin(var), dependent, categorical=True, condition=False, log=True)
    else:
        vargraph(hichol, varin(var), dependent, categorical=iscat(var), condition=False, log=False)        




formula = dependent +  ' ~ ' + independents[0]

for i in range(len(independents)-1):
    formula = formula + ' + ' + independents[i+1]

print formula



model_hichol = smf.ols(formula, data=hichol)
results_hichol = model_hichol.fit()
print results_hichol.summary()

for var in prov_mod:
    by_var = hichol.groupby(var[2:-1])
    print(by_var.size())
    formula_mod = formula + '+' + var
    model_mod = smf.ols(formula_mod, data=hichol)
    results_hichol_mod = model_mod.fit()
    print formula_mod + '\n\n' + str(results_hichol_mod.summary())
