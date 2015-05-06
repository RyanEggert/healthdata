# modelallvars.py
import statsmodels.formula.api as smf
import numpy as np
from meps.data import DataSet
from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs
import cPickle as pkl
import json
import csv
import gc


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
    # modified model vars
    df['BADHLTH'] = df['RTHLTH31'] >= 4

    # core healthcare quality/preventative care vars
    df['PROBLEM'] = df['MDUNPR42'] == 1
    df['CHOLCKYR'] = df['CHOLCK53'] == 1
    df['BPCHKYR'] = df['BPCHEK53'] == 1
    df['GOODHC'] = df['ADHECR42'] >= 8
    df['NODECIDE'] = df['DECIDE42'] == 1
    df['RESPECT'] = df['RESPCT42'] == 4
    df['ENUFTIME'] = df['ADPRTM42'] >= 3
    df['FEWDENTCHK'] = df['DENTCK53'] >= 3
    df['NOPHONE'] = df['PHNREG42'] <= 2
    df['NOAFTERHRS'] = df['AFTHOU42'] <= 2
    df['NOFLUSHT'] = df['FLUSHT53'] >= 5

    # additional healthcare quality/preventative care vars
    df['FEWCHECK'] = df['CHECK53'] >= 2  # PREVENTATIVE
    df['PSAYR'] = df['PSA53'] == 1
    df['PAPYR'] = df['PAPSMR53'] == 1
    df['BRSTYR'] = df['BRSTEX53'] == 1
    df['MAMMOYR'] = df['MAMOGR53'] == 1
    df['STOOLYR'] = df['BSTST53'] == 1
    df['COLONOSYR'] = df['CLNTST53'] == 1
    df['SIGMOIDYR'] = df['SGMTST53'] == 1
    df['SEATBELT'] = df['SEATBE53'] == 1

    df['HARDTOGET'] = df['DFTOUS42'] <= 2  # QUALITY
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

    df['LOGTOTEXP'] = np.log10(df['TOTEXP12']).replace(
        [np.inf, -np.inf], np.nan)
    df['LOGTOTEXP'].dropna()
    return df


def addcategcopy(df, varlist):
    categlist = []
    for varb in varlist:
        if len(df[varb].value_counts()) < 10:
            # Make categorical copy
            categlist.append('C(%s)' % varb)
    varlist.extend(categlist)
    return varlist


H155 = DataSet('h155.pkl')
df = addcustomvars(cleanallerrs(H155.df))
df = df[df.CHOLDX == 1]

# print getattr(H155, 'CHOLDX').responses


dismissed = []  # Variable, coefficient, p-value removed from "good" list

# Set Custom Variables #


# Model Parameters #
dependent = 'LOGTOTEXP'
independents = ['C(ACTLIM31)', 'C(AIDHLP31)', 'AGE12X', 'C(ARTHDX)',
                'C(BADHLTH)', 'BMINDX53', 'C(CANCERDX)', 'C(COGLIM31)',
                'C(DIABDX)', 'C(INS12X)', 'C(WRGLAS42)']


basemodel = makebasemodel(dependent, independents)

allvars = addcategcopy(df, df.columns.tolist())

# allvars = ['BUSNP12X']
# Set of variables to not run through the model
excludelist = set(['DUPERSID'])
varstocheck = [variable for variable in allvars if variable not in excludelist]
allmodels = []  # List to hold model results
errors = []
csvfile = open('modelallvars_res.csv', 'wb+')
fieldnames = ['pvalue', 'rsq', 'rsq_a', 'rsq_diff',
              'coeff', 'size', 'var_name', 'var_descr']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

writer.writeheader()


for i, var in enumerate(varstocheck):
    if i % 1 == 0:
        print 'Checking variable %d of %d. [%s]' % (i + 1, len(varstocheck), var)
    this_model = basemodel + '+' + var
    try:
        this_ols = smf.ols(this_model, data=df, missing='drop')
        this_result = this_ols.fit()
    except Exception as ee:
        print 'MODEL ERROR'
        print ee
        errors.append(var)
        continue
    modeloutvars = [
        catvar for catvar in this_result.pvalues.keys() if catvar.startswith(var)]
    for modeloutvar in modeloutvars:
        try:
            this_val_pvalue = this_result.pvalues[modeloutvar]
            this_val_rsq = this_result.rsquared
            this_val_rsq_a = this_result.rsquared_adj,
            this_val_rsq_diff = abs(
                this_result.rsquared - this_result.rsquared_adj)
            this_val_coeff = this_result.params[modeloutvar]
            this_val_size = this_result.nobs
            this_val_var_name = modeloutvar
            this_val_var_descr = getattr(
                H155, modeloutvar if modeloutvar[
                    1] != '(' else modeloutvar[2:-1],
                {'name': '\'No description avaliable.\''}).name[1: -1]
        except Exception as e:
            print 'ERROR ' + modeloutvar
            print e
            errors.append(modeloutvar)
        else:
            this_data = {
                'pvalue': this_val_pvalue,
                'rsq': this_val_rsq,
                'rsq_a': this_val_rsq_a,
                'rsq_diff': this_val_rsq_diff,
                'coeff': this_val_coeff,
                'size': this_val_size,
                'var_name': this_val_var_name,
                'var_descr': this_val_var_descr
            }
            writer.writerow(this_data)
            this_data = {}

csvfile.close()

# sorted_allmodels = sorted(allmodels, key=getkey, reverse=True)

outobj = {
    # 'successes': allmodels,
    # 'sort_successes': sorted_allmodels,
    'errors': errors,
}


pcklfile = open('modelallvars_res.pkl', 'wb')
pkl.dump(outobj, pcklfile)
pcklfile.close()

# save to file:
with open('modelallvars_res.json', 'wb') as f:
    json.dump(outobj, f)

print 'Errors'
print errors
