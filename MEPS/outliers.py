# outliers.py

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt

import sklearn


def identifyoutliers(dataset, variablename, highrange=10, lowrange=10):
    """Given a dataframe and a variable name, return a dictionary
    of low and high outliers identified by by DUPERSID.
    "lowrange" and "highrange" specify percent ranges of outliers. (e.g.
    lowrange=5 will return the lowest 5% of data in the low outliers set.)
    """
    # Create Series & remove error codes
    ds = dataset[variablename][dataset[variablename] > 0]

    # Find value of lowrange-th percentile
    lowperc = ds.quantile(lowrange/100.)
    highperc = ds.quantile(highrange/100.)

    # Identify all points in 0-lowrange percentiles.


    pass


def makedataframe(dataset, outliers):
    """Given a dataframe and a list of outlier DUPERSIDs, returns a dataframe
    containing only rows associated with the DUPERSIDs in 'outliers'.
    """
    pass


def main():
    pass


if __name__ == '__main__':
    main()
