import matplotlib.pyplot as plt
import matplotlib.cm as cm
from numpy import linspace, unique, array, median
from numpy import transpose as nptranspose
from scipy.stats import pearsonr

# from meps.think.stats2 import Corr as pearsonr


def iscat(var):
    """Returns True if variable is categorical. Uses
    statsmodels syntax.
    """
    categorical = False
    if var[0:2] == 'C(':
        categorical = True
    return categorical


def varin(var):
    """If a categorical variable, returns just the variable name
    (i.e. removes the "C(...)").
    """
    retvar = var
    if iscat(var):
        retvar = var[2:-1]
    return retvar


def logyrange(data):
    """Looks across all the datasets in data (a list of lists), and returns a
    minimum and a maximum for use in scaling a logarithmic axis."""

    flatdata = [point for dset in data for point in dset]
    datasumm = unique(flatdata).tolist()

    if datasumm[0] == 0:
        alldata_min = datasumm[1]
    elif datasumm[0] < 0:
        thisval = datasumm[0]
        ind = 0
        while thisval <= 0:     # Requires that data have positive part
            ind += 1
            thisval = datasumm[ind]
        alldata_min = datasumm[ind]

    alldata_max = max(datasumm)  # See whether this will be alright.
    return alldata_min, alldata_max


def categplot(df, exv, dev, log=False, catlabels=False, condition=False, dfcond=False, dfncond=False):
    categories = sorted(df[exv].unique())
    catdata = []
    for cat in categories:
        if condition:
            # Select all of one category (w/condition)
            this_sectc = dfcond[dfcond[exv] == cat]
            # Select the dependent variable
            this_depc = this_sectc[dev]
            # Store this_depc in a list and append to master list of lists
            this_cdata = this_depc.values
            catdata.append(this_cdata)
            # Select all of one category
            this_sectnc = dfncond[dfncond[exv] == cat]
            # Select the dependent variable
            this_depnc = this_sectnc[dev]
            # Store this_depnc in a list and append to master list of lists
            this_ncdata = this_depnc.values
            catdata.append(this_ncdata)
        else:
            # Select all of one category
            this_sect = df[df[exv] == cat]
            # Select the dependent variable
            this_dep = this_sect[dev]
            # Store this_dep in a list and append to master list of lists
            this_data = this_dep.values
            catdata.append(this_data)

    # Create a figure instance
    fig = plt.figure(1, figsize=(9, 6))
    # Create an axes instance
    ax = fig.add_subplot(111)
    # Create the boxplot

    bp = ax.boxplot(catdata, 0, '', 1, [25 - 15, 75 + 15])
    if condition:
        if catlabels:
            condcats = [str(x) + '_c' for x in condcats]
            ncondcats = [str(x) + '_nc' for x in condcats]
        else:
            condcats = [str(x) + '_c' for x in categories]
            ncondcats = [str(x) + '_nc' for x in categories]

        comblists = ncondcats + condcats
        comblists[::2] = ncondcats
        comblists[1::2] = condcats
        xlabels = comblists
    else:
        xlabels = categories

    if log:
        ax.set_yscale('log')
        ax.set_ylim(logyrange(catdata))
    ax.set_xticklabels(xlabels)
    ax.set_xlabel('Categories of %s' % exv)
    ax.set_ylabel(dev)
    if condition:
        nameplot(ax, fig, dev,
                 exv, condition=condition)
    else:
        nameplot(ax, fig, dev,
                 exv)
    print 'Median Data for %s, %s:' % (exv, dev)
    print xlabels
    print [median(x) for x in catdata]


def nameplot(ax, fig, dev, exv, condition=False, categorical=False):
    # Save the figure
    if condition:
        ax.set_title('%s & %s by condition %s' %
                     (dev, exv, condition))
        fig.savefig('./graphs/vargraphs/%s_%s_%s.png' %
                    (dev, exv, condition), bbox_inches='tight')
        fig.clf()
    else:
        ax.set_title('%s & %s' % (dev, exv))
        fig.savefig('./graphs/vargraphs/%s_%s.png' %
                    (dev, exv), bbox_inches='tight')
        fig.clf()


def vargraph(dataframe, explanatoryvariable, dependentvariable, categorical=False, catlabels=False, condition=False, log=False):
    """
    dataframe: Cleaned (Errors are NaN) DataFrame containing at least
    explanatoryvariable and dependentvariable.
    explanatoryvariable: Name of explanatory (x) variable
    dependentvariable: Name of dependent (y) variable
    categorical: Optional boolean. True if explanatoryvariable is categorical.
    condition: Optional string. Name of condition variable for comparison.
    log: Optional boolean. True for logarithmic y scale.
    """
    df = dataframe[[explanatoryvariable, dependentvariable]].dropna()

    if condition:
        dfc = dataframe[dataframe[condition] == 1]
        dfcond = dfc[[explanatoryvariable, dependentvariable]].dropna()
        dfnc = dataframe[dataframe[condition] == 2]
        dfncond = dfnc[[explanatoryvariable, dependentvariable]].dropna()

    if categorical:
        if condition:
            categplot(df, explanatoryvariable, dependentvariable, log=log,
                      condition=condition, catlabels=catlabels, dfcond=dfcond, dfncond=dfncond)
        else:
            categplot(
                df, explanatoryvariable, dependentvariable, catlabels=catlabels, log=log)

    else:
        # Continuous Variable
        if condition:
            x_cond = dfcond[explanatoryvariable].values
            x_ncond = dfncond[explanatoryvariable].values
            y_cond = dfcond[dependentvariable].values
            y_ncond = dfncond[dependentvariable].values
            x = [x_ncond, x_cond]
            y = [y_ncond, y_cond]
            print array(x_cond).shape, array(y_cond).shape
            print array(x_ncond).shape, array(y_ncond).shape
            corr_ncond = pearsonr(array(x_ncond), array(y_ncond))
            corr_cond = pearsonr(array(x_cond), array(y_cond))
            labels = ['Yes, %s (r = %.4f, p = %.4f, sz = %d)' % (
                condition, corr_cond[0], corr_cond[1], len(x_cond)),
                'No, %s (r = %.4f, p = %.4f, sz = %d)' % (
                condition, corr_ncond[0], corr_ncond[1], len(x_ncond))]
        else:
            x = [df[explanatoryvariable].values]
            y = [df[dependentvariable].values]
            print nptranspose(array(x)).shape, nptranspose(array(y)).shape
            corr = pearsonr(nptranspose(array(x)), nptranspose(array(y)))
            labels = ['r = %.4f, p = %d, sz = %d' % (corr[0], corr[1], len(x))]

        # Make scatterplot
        # Create a figure instance
        fig = plt.figure(1, figsize=(9, 6))
        # Create an axes instance
        ax = fig.add_subplot(111)
        # Generate colors
        colors = cm.rainbow(linspace(0, 1, len(x)))
        # Create the scatterplot
        for i, xsets in enumerate(x):
            print 'wat'
            ax.scatter(
                xsets, y[i], marker='o', alpha=0.5, lw=0, color=colors[i])
        if log:
            ax.set_yscale('log')
            ax.set_ylim(logyrange(y))
        ax.legend(labels)
        ax.set_xlabel(explanatoryvariable)
        ax.set_ylabel(dependentvariable)

        if condition:
            nameplot(ax, fig, dependentvariable,
                     explanatoryvariable, condition=condition)
        else:
            nameplot(ax, fig, dependentvariable,
                     explanatoryvariable)


def main():
    H155 = DataSet('h155.pkl')
    df = cleanallerrs(H155.df)
    df = df[df['CHOLDX'] == 1]
    vargraph(df, 'ARTHDX', 'TOTEXP12', categorical=True, catlabels=getattr(H155, 'IPNGTD12').responses,
             log=True, condition=False)

if __name__ == '__main__':
    from meps.data import DataSet
    from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs
    main()
