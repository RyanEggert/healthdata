# varlook.py #
import os
import pandas as pd
import dataio as dio
import re


class DataSet(object):
    """docstring for dataset"""
    def __init__(self, picklefilename):
        super(DataSet, self).__init__()
        self.originpickle = picklefilename
        self.df = dio.importdata(picklefilename)
        self.name = picklefilename[:5].rstrip('_')

    def __str__(self):
        return 'dataset object ' + self.name
    # save dataframe as pickle

    def varlookup(self):
        pass


class Variable(object):
    """docstring for Variable"""
    def __init__(self, datasetname):
        super(Variable, self).__init__()
        self.set = datasetname

    def getDocs(self):
        """Looks in the appropriate text file to find this variable's documentation
        """
        with open(self.set+'.txt') as txtfile:

        #get full name

        #get values


        pass



def main():
    H155 = DataSet('h155_processed.pkl')
    print H155.name

if __name__ == '__main__':
    main()





    # def savedata(dataframe, picklefilename):
    #     """Saves a dataframe as a pickle in the pickles folder. Specify a name
    #     (including '.pkl')."""
    #     curdir = os.getcwd()
    #     pickleloc = curdir + '/Data/pickles/' + picklefilename
    #     dataframe.to_pickle(pickleloc)
