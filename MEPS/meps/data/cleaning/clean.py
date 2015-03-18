from numpy import NaN


def clean(dataframe, variable, clean):
    """Given a dataframe, variable, and a list of items to 'clean', returns
    the dataframe with all values of variable in clean revalued to NaN.
    """
    for scrub in clean:
        dataframe[dataframe[variable] == scrub][variable] = NaN
    return dataframe
