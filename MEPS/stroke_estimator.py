from matplotlib import pyplot as plt
import numpy as np
from numpy.random import choice

from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt


def showhist(series):
    """Given a pandas data series, plots histogram.
    """
    tplt.Hist(ts2.Hist(series), label='histogram')


def cleanseries(series):
    """Given a pandas data series, removes MEPS error codes.
    """
    return series[series >= 0]


def runmeanexperiment(indata):
    # Generate new sample
    newsample = choice(indata, len(indata), replace=True)
    return newsample.mean()


def runmedianexperiment(indata):
    # Generate new sample
    newsample = choice(indata, len(indata), replace=True)
    return np.median(newsample)


def meanestimator(variable, dataframe):
    """For a normally distributed variable from a dataframe,
    estimates the population mean"""
    print 'Sample Mean Estimation'
    dse = dataframe[variable]
    clser = cleanseries(dse)    # Clean dataseries of error codes
    smean = clser.mean()  # Compute sample mean of variable
    # showhist(clser)
    print smean
    expres = []
    for i in xrange(50000):
        expres.append(runmeanexperiment(clser))
    # Plot Variable CDF
    tplt.Figure()
    varcdf = ts2.Cdf(clser)
    tplt.Cdf(varcdf)
    tplt.Config(title="%s CDF" % variable)
    # Plot Expermental Median CDF
    tplt.Figure()
    expscdf = ts2.Cdf(expres)
    tplt.Cdf(expscdf)
    tplt.Config(title="%s Experimental Mean CDF" % variable)
    print '90 pct. Confidence Interval: ' + str(expscdf.ConfidenceInterval())
    print 'Standard Error: %.4f' % ts2.Std(expres)
    # Plot normal probability plot
    tplt.Figure()
    ts2.NormalProbabilityPlot(expres)
    tplt.Config(
        title="Normal Probability Plot of %s Mean Estimation" % variable)


def medianestimator(variable, dataframe):
    """For a normally distributed variable from a dataframe,
    estimates the population median"""
    print 'Sample Median Estimation'
    dse = dataframe[variable]
    clser = cleanseries(dse)    # Clean dataseries of error codes
    smedian = clser.median()  # Compute sample median of variable
    # showhist(clser)
    print smedian
    expres = []
    for i in xrange(50000):
        expres.append(runmedianexperiment(clser))
    # Plot Variable CDF
    tplt.Figure()
    varcdf = ts2.Cdf(clser)
    tplt.Cdf(varcdf)
    tplt.Config(title="%s CDF" % variable)
    # Plot Expermental Median CDF
    tplt.Figure()
    expscdf = ts2.Cdf(expres)
    tplt.Cdf(expscdf)
    tplt.Config(title="%s Experimental Median CDF" % variable)
    print '90 pct. Confidence Interval: ' + str(expscdf.ConfidenceInterval())
    print 'Standard Error: %.4f' % ts2.Std(expres)
    # Plot normal probability plot
    tplt.Figure()
    ts2.NormalProbabilityPlot(expres)
    tplt.Config(
        title="Normal Probability Plot of %s Median Estimation" % variable)


def main():
    h155 = DataSet('h155.pkl')
    df = h155.df
    meanestimator('STRKAGED', df)
    medianestimator('STRKAGED', df)
    plt.show(block=True)

if __name__ == '__main__':
    main()
