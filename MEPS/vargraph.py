import matplotlib.pyplot as plt
import matplotlib.cm as cm
from numpy import linspace, unique


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


def vargraph(dataframe, explanatoryvariable, dependentvariable, categorical=False, condition=False, log=False):
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
        # Find possible categories
        categories = sorted(df[explanatoryvariable].unique())
        catdata = []
        for cat in categories:
            if condition:
                # Select all of one category (w/condition)
                this_sectc = dfcond[dfcond[explanatoryvariable] == cat]
                # Select the dependent variable
                this_depc = this_sectc[dependentvariable]
                # Store this_depc in a list and append to master list of lists
                this_cdata = this_depc.values
                catdata.append(this_cdata)
                # Select all of one category
                this_sectnc = dfncond[dfncond[explanatoryvariable] == cat]
                # Select the dependent variable
                this_depnc = this_sectnc[dependentvariable]
                # Store this_depnc in a list and append to master list of lists
                this_ncdata = this_depnc.values
                catdata.append(this_ncdata)
            else:
                # Select all of one category
                this_sect = df[df[explanatoryvariable] == cat]
                # Select the dependent variable
                this_dep = this_sect[dependentvariable]
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
        ax.set_xlabel('Categories of %s' % explanatoryvariable)
        ax.set_ylabel(dependentvariable)

    else:
        if condition:
            x_cond = dfc[explanatoryvariable].values
            x_ncond = dfnc[explanatoryvariable].values
            y_cond = dfc[dependentvariable].values
            y_ncond = dfnc[dependentvariable].values
            x = [x_ncond, x_cond]
            y = [y_ncond, y_cond]
            labels = ['Yes, %s' % condition, 'No, %s' % condition]
        else:
            x = [df[explanatoryvariable].values]
            y = [df[dependentvariable].values]
            labels = ['']

        # Make scatterplot
        # Create a figure instance
        fig = plt.figure(1, figsize=(9, 6))
        # Create an axes instance
        ax = fig.add_subplot(111)
        # Generate colors
        colors = cm.rainbow(linspace(0, 1, len(x)))
        # Create the scatterplot
        for i, xsets in enumerate(x):
            ax.scatter(
                xsets, y[i], marker='o', alpha=0.5, lw=0, color=colors[i])
        if log:
            ax.set_yscale('log')
            ax.set_ylim(logyrange(y))
        ax.legend(labels)
        ax.set_xlabel(explanatoryvariable)
        ax.set_ylabel(dependentvariable)

    # Save the figure
    if condition:
        ax.set_title('%s & %s by condition %s' %
                     (dependentvariable, explanatoryvariable, condition))
        fig.savefig('./graphs/vargraphs/%s_%s_%s.png' %
                    (dependentvariable, explanatoryvariable, condition), bbox_inches='tight')
    else:
        ax.set_title('%s & %s' % (dependentvariable, explanatoryvariable))
        fig.savefig('./graphs/vargraphs/%s_%s.png' %
                    (dependentvariable, explanatoryvariable), bbox_inches='tight')


def main():
    H155 = DataSet('h155.pkl')
    df = cleanallerrs(H155.df)
    vargraph(df, 'RTHLTH31', 'TOTEXP12', categorical=True,
             log=True, condition='EMPHDX')

if __name__ == '__main__':
    from meps.data import DataSet
    from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs
    main()
