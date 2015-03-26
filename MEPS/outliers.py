# outliers.py
from operator import itemgetter

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt
from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs

import sklearn


def identifyoutliers(dataframe, variablename, lowrange=10, highrange=10):
    """Given a dataframe and a variable name, return a dictionary
    of low and high outliers identified by by DUPERSID.
    "lowrange" and "highrange" specify percent ranges of outliers. (e.g.
    lowrange=5 will return the lowest 5% of data in the low outliers set.)
    """
    # Create Series & remove error codes
    cleandf = cleanerrs(dataframe, variablename).dropna(subset=[variablename])
    ds = cleandf[variablename]
    # Find value of lowrange-th percentile
    lowperc = ds.quantile(lowrange / 100.)
    highperc = ds.quantile((100. - highrange) / 100.)

    # Identify all points in 0-lowrange percentiles.
    lowdf = cleandf[cleandf[variablename] <= lowperc]
    highdf = cleandf[cleandf[variablename] >= highperc]

    # Get list of DUPERSIDs from each dataframe
    lowID = lowdf['DUPERSID'].values.tolist()
    highID = highdf['DUPERSID'].values.tolist()

    # Size of ranges
    lowquan = len(lowID)
    highquan = len(highID)

    return {
        'low': {
            'df': lowdf,
            'ids': lowID,
            'range': [ds.min(), lowperc],
            'size': lowquan,
            'percentile': lowrange
        },
        'high': {
            'df': highdf,
            'ids': highID,
            'range': [highperc, ds.max()],
            'size': highquan,
            'percentile': highrange
        }
    }


def samplemean(dataframe, variable):
    """Computes and returns the mean of the variable from the full dataframe.
    """
    return dataframe[variable].mean()


def findsimilarities(dataframe, checkvars, orig_dataframe):
    """Takes a dataframe (from identifyoutliers()) of outliers and a list of
    variables to be checked.
    """
    cleanframe = cleanallerrs(dataframe)
    clean_orig = cleanallerrs(orig_dataframe)
    reslist = []
    for var in checkvars:
        this_series = cleanframe[var]
        this_std = this_series.std()
        this_mean = this_series.mean()
        this_stdv = this_std / this_mean
        this_qr = this_series.quantile(.8) / this_series.mean() - \
            this_series.quantile(.2) / this_series.mean()
        this_min = this_series.min()
        this_max = this_series.max()
        this_median = this_series.median()
        this_closetomedian = len(
            this_series[(this_series < this_median * 1.1) & (this_series > this_median * 0.9)])
        this_meandif = this_mean - samplemean(clean_orig, var)
        this_absmeandif = abs(this_meandif)
        this_normabsmeandif = this_absmeandif / this_mean
        # Number of NaNs:
        this_nan = this_series.isnull().sum()
        this_len = len(this_series)
        this_nonnan = this_len - this_nan

        this_info = {
            'name': var,
            'mean': this_mean,
            'std': this_std,
            'normstd': this_stdv,
            'percrange': this_qr,
            'min': this_min,
            'max': this_max,
            'median': this_median,
            'medianrange': this_closetomedian,
            'meandif': this_meandif,
            'absmeandif': this_absmeandif,
            'normabsmeandif': this_normabsmeandif,
            'NaNs': this_nan,
            'nonNaNs': this_nonnan,
            'size': this_len

        }
        reslist.append(this_info)

    # sort reslist
    outlist = sorted(reslist, key=itemgetter('normabsmeandif'), reverse=True)
    return outlist


def analyzeoutliers(dataframe, variablename, checkvars):
    outliers = identifyoutliers(dataframe, variablename)
    # Make list of low and high outlier dataframes
    outlierlabels = ['low', 'high']
    lhdf = [outliers['low']['df'], outliers['high']['df']]
    results = {}
    for outliertype in outlierlabels:
        outlierset = outliers[outliertype]['df']
        ranked = findsimilarities(outlierset, checkvars, dataframe)
        results[outliertype] = ranked
    return results, outliers


def main():
    # Demonstration. Prints data regarding lowest 5 and highest 10 percent of
    # total healthcare expenditures.
    h155 = DataSet('h155.pkl')
    df = h155.df
    # outliers = identifyoutliers(df, 'TOTEXP12', 5, 10)
    # print 'low'
    # print outliers['low']['size']
    # print outliers['low']['range']
    # print outliers['low']['percentile']
    # print '\nhigh'
    # print outliers['high']['size']
    # print outliers['high']['range']
    # print outliers['high']['percentile']
    checkvars = ['ADDRBP42', 'ADEXPL42', 'ADEZUN42', 'ADFHLP42', 'ADHECR42', 'ADILWW42', 'ADINST42', 'ADLIST42', 'ADPRTM42', 'ADRESP42', 'ADRTWW42', 'ADSPRF42', 'ADTLHW42', 'CLNTST53', 'BPCHEK53', 'BRSTEX53', 'BSTST53', 'CHOLCK53', 'DENTCK53', 'BPCHEK53', 'BRSTEX53', 'EATHLT42', 'DSA1C53', 'DSCB1153', 'DSCGRP53', 'DSCH1153', 'DSCH1253', 'DSCH1353', 'DSCHNV53', 'DSCINT53', 'DSCNPC53',
                 'DSCONF53', 'DSCPCP53', 'DSCPHN53', 'DSDIA53', 'DSDIET53', 'DSEB1153', 'DSEY1153', 'DSEY1253', 'DSEY1353', 'DSEYNV53', 'DSFB1153', 'DSFL1153', 'DSFL1253', 'DSFL1353', 'DSFLNV53', 'DSFT1153', 'DSFT1253', 'DSFT1353', 'DSFTNV53', 'DSINSU53', 'DSMED53', 'DSVB1153', 'FLUSHT53', 'FOODST12', 'MAMOGR53', 'PAPSMR53', 'SGMTRE53', 'SGMTST53', 'BPMONT53', 'NOFAT53', 'EXRCIS53', 'ASPRIN53', 'PSA53', 'ADDPRS42', 'ADHECR42', 'ADSMOK42', 'AGE12X', 'AIDHLP31', 'AIDHLP53', 'AMCHIR12', 'OBCHIR12', 'AMNURS12', 'OBNURS12', 'AMOPTO12', 'OBOPTO12', 'AMASST12', 'OBASST12', 'AMTHER12', 'OBTHER12', 'OBTOTV12', 'OBDRV12', 'OBOTHV12', 'COGLIM31', 'COGLIM53', 'BLIND42', 'BMINDX53', 'DEAF42', 'EMPST31', 'EMPST42', 'EMPST53', 'EVRETIRE', 'FNGRDF31', 'FNGRDF53', 'HEARAD42', 'HSELIM31', 'HSELIM53', 'HYSTER53', 'MARRY12X', 'MILDIF31', 'MILDIF53', 'NOASPR53', 'NOFAT53', 'RCHDIF31', 'RCHDIF53', 'READNW42', 'RECPEP42', 'SEX', 'STNDIF31', 'STNDIF53', 'STOMCH53', 'STPDIF31', 'STPDIF53', 'TTLP12X', 'UNABLE31', 'UNABLE53', 'VISION42', 'WLK3MO31', 'WLK3MO53', 'WLKDIF31', 'WLKDIF53', 'WLKLIM31', 'WLKLIM53', 'WRGLAS42', 'WRKLIM31', 'WRKLIM53', 'REGION12', 'RACETHX', 'RACEV1X', 'HIDEG', 'POVLEV12', 'RTHLTH31', 'RTHLTH42', 'RTHLTH53', 'MNHLTH31', 'MNHLTH42', 'MNHLTH53', 'PREGNT31', 'PREGNT42', 'PREGNT53', 'JTPAIN31', 'JTPAIN53', 'BENDIF31', 'BENDIF53', 'ASACUT53', 'IADLHP31', 'IADLHP42', 'IADLHP53', 'ACTLIM31', 'ACTLIM53', 'LSTETH53', 'PHYEXE53', 'ADINSA42', 'ADINSB42', 'ADRISK42', 'ADOVER42', 'EMPST31', 'EMPST42', 'EMPST53', 'CHECK53']

    # checkvars = h155.varnames
    results, outliers = analyzeoutliers(df, 'ERTOT12', checkvars)
    print 'High Outlier (>%d) Similarities:' % (outliers['high']['range'][1])
    for i in range(20):
        res = results['high'][i]
        print '%d. %s: Difference of means: %s, %.3f%% different (median: %d)' % (i + 1, res['name'], res['meandif'], 100 * float(res['meandif']) / float(res['mean']), res['median'])

    print 'Low Outlier (<%d) Similarities:' % (outliers['low']['range'][1])
    for i in range(20):
        res = results['low'][i]
        print '%d. %s: Difference of means: %s, %.3f%% different (median: %d)' % (i + 1, res['name'], res['meandif'], 100 * float(res['meandif']) / float(res['mean']), res['median'])

if __name__ == '__main__':
    main()
