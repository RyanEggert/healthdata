import statsmodels.formula.api as smf
import numpy as np


def guessrelationship(dataframe, explanatoryvariable, dependentvariable):
    exv = explanatoryvariable
    dev = dependentvariable
    if exv[0:2] == 'C(':
        categorical = True
        dfexv = exv[2:-1]
    else:
        categorical = False
        dfexv = exv
    dataframe[dev + '_linear'] = dataframe[dev]  # No change
    dataframe[dev + '_squared'] = np.square(dataframe[dev])  # Squared
    dataframe[dev + '_sqrt'] = np.sqrt(dataframe[dev])  # Square root
    dataframe[dev + '_log'] = np.log(dataframe[dev])  # Log
    dataframe[dev + '_inverse'] = np.reciprocal(dataframe[dev])

    dataframe[dev + '_exp'] = np.exp(dataframe[dev])  # Exponential
    print dataframe[dev + '_exp'].value_counts()
    relations = ['linear', 'squared', 'sqrt', 'log', 'exp', 'inverse']
    rsqs = {}
    for relation in relations:
        if categorical:
            expvar = 'C(' + dfexv + ')'
        else:
            expvar = dfexv
        depvar = dev + '_' + relation
        formula = depvar + ' ~ ' + expvar
        model = smf.ols(formula, data=dataframe)
        results = model.fit()
        rsqs[relation] = (results.rsquared)
    return rsqs


def main():
    H155 = DataSet('h155.pkl')
    df = cleanallerrs(H155.df)
    print guessrelationship(df, 'BMINDX53', 'TOTEXP12')


if __name__ == '__main__':
    from meps.data import DataSet
    from meps.data.cleaning.cleanerrs import cleanallerrs
    main()
