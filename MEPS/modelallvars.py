# modelallvars.py
import statsmodels.formula.api as smf
import numpy as np
from meps.data import DataSet
from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs
import dill as pkl


def getkey(item):
    """Sort support function which selects dictionary key by which to sort.
    """
    return item['rsq']


def makebasemodel(dependent, independents):
    """Returns string representing base statsmodels formula.

    Args:
        dependent (str): DataFrame name of desired dependent variable.
        independents ([str]): List of DataFrame names of all independent
            model variables.
    Returns:
        str: statsmodels formula string.
    """
    formula = dependent + ' ~ ' + independents[0]
    for i in range(len(independents) - 1):
        formula = formula + ' + ' + independents[i + 1]
    return formula


def addcustomvars(df):
    """Adds these custom variables to the specified DataFrame. Note that these
    custom variables are meant to be calculated from the MEPS (2012)
    consolidated data file. Using a different data file will almost certainly
    result in errors.

    Args:
        df (DataFrame): DataFrame to impute/add custom variables from/to.

    Returns:
        DataFrame: Updated DataFrame
    """
    df['BADHLTH'] = df['RTHLTH31'] >= 4
    df['BADMENT'] = df['MNHLTH31'] >= 4
    df['EXPHLTH'] = 10 ** (df['RTHLTH31'] ** 2)
    df['PROBLEM'] = df['MDUNPR42'] == 1
    df['CHOLCKYR'] = df['CHOLCK53'] == 1
    df['FEWCHOLCK'] = df['CHOLCK53'] >= 5
    df['BPCHKYR'] = df['BPCHEK53'] == 1
    df['RICH'] = df['POVCAT12'] == 5
    df['DEPRESSED'] = df['PHQ242'] == 6
    df['GOODHC'] = df['ADHECR42'] >= 8
    df['BADHC'] = df['ADHECR42'] == 0
    df['NODECIDE'] = df['DECIDE42'] == 1
    df['RESPECT'] = df['RESPCT42'] == 4
    df['NOCARE'] = df['ADILWW42'] == 1
    df['NOEASYCARE'] = df['ADEGMC42'] == 1
    df['NOLISTEN'] = df['ADLIST42'] <= 2
    df['ENUFTIME'] = df['ADPRTM42'] >= 3
    df['HARDTOGET'] = df['DFTOUS42'] <= 2
    df['FEWDENTCHK'] = df['DENTCK53'] >= 3
    df['NOPHONE'] = df['PHNREG42'] <= 2
    df['NOAFTERHRS'] = df['AFTHOU42'] <= 2
    df['NOFLUSHT'] = df['FLUSHT53'] >= 5
    df['HEARTDIS'] = ((df['OHRTDX'] + df['CHDDX'])) >= 1
    df['FEWCHECK'] = df['CHECK53'] >= 2
    df['LOGTOTEXP'] = np.log10(df['TOTEXP12']).replace(
        [np.inf, -np.inf], np.nan)
    df['LOGTOTEXP'].dropna()
    return df

H155 = DataSet('h155.pkl')
df = addcustomvars(cleanallerrs(H155.df))


# print getattr(H155, 'CHOLDX').responses


dismissed = []  # Variable, coefficient, p-value removed from "good" list

# Set Custom Variables #


# Model Parameters #
dependent = 'LOGTOTEXP'
independents = ['C(ACTLIM31)', 'C(AIDHLP31)', 'AGE12X', 'C(ARTHDX)',
                'C(BADHLTH)', 'BMINDX53', 'C(CANCERDX)', 'C(COGLIM31)',
                'C(DIABDX)', 'C(INS12X)', 'C(WRGLAS42)']


basemodel = makebasemodel(dependent, independents)

allvars = df.columns.tolist()
# allvars = ['BUSNP12X']
# Set of variables to not run through the model
excludelist = set(['DUPERSID'])
varstocheck = [variable for variable in allvars if variable not in excludelist]
allmodels = []  # List to hold model results
errors = []
for i, var in enumerate(varstocheck):
    if i % 1 == 0:
        print 'Checking variable %d of %d.' % (i + 1, len(varstocheck))
    this_model = basemodel + '+' + var
    this_ols = smf.ols(this_model, data=df, missing='drop')
    this_result = this_ols.fit()
    try:
        this_data = {
            'pvalue': this_result.pvalues[var],
            'rsq': this_result.rsquared,
            'rsq_a': this_result.rsquared_adj,
            'rsq_diff': abs(this_result.rsquared - this_result.rsquared_adj),
            'coeff': this_result.params[var],
            'size': this_result.nobs,
            'var_name': var,
            'var_descr': getattr(H155, var, {
                'name': '\'No description avaliable.\''
            }).name[1: -1]
        }
    except:
        print 'ERROR'
        errors.append(var)
    else:
        allmodels.append(this_data)

outobj = {
    'successes': allmodels,
    'errors': errors
}
with open('modelallvars_res.pkl', 'wb+') as pcklfile:
    pkl.dump(outobj, pcklfile)

sorted_allmodels = sorted(allmodels, key=getkey, reverse=True)
print 'RESULTS'
print 'Successes:'
print sorted_allmodels
print
print '________________________________'
print 'Errors'
print errors
