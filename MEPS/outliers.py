# outliers.py

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt
from meps.data.cleaning.cleanerrs import cleanerrs

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


def main():
    # Demonstration. Prints data regarding lowest 5 and highest 10 percent of
    # total healthcare expenditures.
    h155 = DataSet('h155.pkl')
    df = h155.df
    outliers = identifyoutliers(df, 'TOTEXP12', 5, 10)
    print 'low'
    print outliers['low']['size']
    print outliers['low']['range']
    print outliers['low']['percentile']
    print '\nhigh'
    print outliers['high']['size']
    print outliers['high']['range']
    print outliers['high']['percentile']

if __name__ == '__main__':
    main()
