# dataio.py

import pandas as pd
import os
import tables

# take data from csv to dataframe (first import) and pickle it


def firstimport(csvfilename):
    """Given the name of a csv file [string] in the DataIn folder, this opens
    the .csv as a Pandas dataframe."""
    curdir = os.getcwd()
    csvloc = curdir + '/Data/DataIn/' + csvfilename
    newDF = pd.read_csv(csvloc, delimiter=',')
    # We may consider indexing our dataframes by the DUPERSID column.
    pickleloc = curdir + '/Data/pickles/' + csvfilename[:-4] + '.pkl'
    newDF.to_pickle(pickleloc)

# open dataframe from pickle


def importdata(picklefilename):
    """Imports the given pickle file name from the pickles folder and returns
    it as a dataframe"""
    curdir = os.getcwd()
    pickleloc = curdir + '/Data/pickles/' + picklefilename
    openDF = pd.read_pickle(pickleloc)
    return openDF


# save dataframe as pickle
def savedata(dataframe, picklefilename):
    """Saves a dataframe as a pickle in the pickles folder. Specify a name
    (including '.pkl')."""
    curdir = os.getcwd()
    pickleloc = curdir + '/Data/pickles/' + picklefilename
    dataframe.to_pickle(pickleloc)


def main(csv):
    firstimport(csv)
    df2 = importdata('test.pkl')
    print df2
    savedata(df2, 'test2.pkl')


if __name__ == '__main__':
    main('test.csv')
