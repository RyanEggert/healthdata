# cleanerrs.py

from numpy import NaN
from .clean import clean


def cleanerrs(dataframe, variable, exclude=False):
    """Given a dataframe and a variable, replaces every negative error code
    with NaN. You may optionally specify a list of values to exclude from
    this cleaning process.
    """
    errcodes = range(-13, 0)
    if not exclude:
        exclist = []
    else:
        exclist = exclude

    replcodes = list(set(errcodes) - set(exclist))
    for code in replcodes:
        dataframe = clean(dataframe, variable, code)
    return dataframe


def cleanallerrs(dataframe, exclude=False):
    """Replaces a range of negative numbers (MEPS error codes) with NaN.
    You may optionally specify a list of negative values to exclude from
    this cleaning process.
    """
    errcodes = range(-13, 0)
    if not exclude:
        exclist = []
    else:
        exclist = exclude

    replcodes = list(set(errcodes) - set(exclist))

    dataframe.replace(replcodes, NaN)

    return dataframe


# http://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/h155/h155doc.shtml
# Section 2.2 of the above link shows that MEPS' reserved codes range from -1
# to -13.
