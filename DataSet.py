"""varlook.py"""
import os
import pandas as pd
import re
import dill as pickle
import sys
import time
import requests
from urllib import quote_plus
import json
from time import sleep

from config import auth
import dataio as dio


def DataSet(picklefilename, new=False):
    """Function masquerading as Class.
    If new = True, we create a new object. This involves retrieving information
    from the internet. If new = False, we look for a cached copy of the
    DataSet_ object
    """
    if not new:
        try:
            existname = 'dataset_store/%s_datasetobj.pkl' % picklefilename[
                :5].rstrip('_.')
            with open(existname, 'rb') as stf:
                existobj = pickle.load(stf)  # Open pickle
        except Exception, e:
            print "\"%s\" does not yet exist. Please create this file by instantiating this object once with new=True" % (existname)
            raise e
        else:
            return existobj     # Return unpickled object
    else:
        dset = DataSet_(picklefilename)
        return dset


class DataSet_(object):

    """Creates a DataSet object for a MEPS dataset and uses Dill
    to store the result for future use.
    """

    def __init__(self, picklefilename):
        super(DataSet_, self).__init__()
        self.originpickle = picklefilename
        # Just the original dataset name (e.g. "h155", "h152a", etc.)
        self.name = picklefilename[:5].rstrip('_.')
        # Create dataframe from saved pickle
        self.df = dio.importdata(picklefilename)
        # Dictionary of key=VARABBV, value= long variable name/description
        self.varnames = self.loadAllVariables()
        progresscounter = 0
        for key in self.varnames:
            # For every variable, instatiate a Variable object, accessible as a
            # DataSet method.
            setattr(self, key, Variable(self.name, key, self.varnames[key]))
            progresscounter += 1    # Increment counter
            if progresscounter % 2 == 0:
                sys.stdout.write("\rRetrieved %d out of %d variables of %s" % (
                    progresscounter, len(self.varnames), self.name))
                sys.stdout.flush()
            time.sleep(.3)  # Try not to flood the website with requests.

        sys.stdout.write("\rRetrieved %d out of %d variables of %s" % (
            len(self.varnames), len(self.varnames), self.name))
        sys.stdout.flush()
        print '\n'
        with open('dataset_store/%s_datasetobj.pkl' % self.name, 'wb+') as stf:
            pickle.dump(self, stf)

    def __str__(self):
        return 'Dataset object ' + self.name

    def loadAllVariables(self):
        """Get a list of all variables from text file"""
        with open('codebook_info/%s.txt' % self.name) as txtfile:
            text = txtfile.readlines()
        variablenames = {}
        for index, line in enumerate(text):
            if all(x == ' ' for x in line[:6]):
                # These are variables and their full names
                # Splits each line ONCE at the first '='
                splitnames = line.split('=', 1)
                variablenames[splitnames[0].lstrip().rstrip()] = splitnames[
                    1].lstrip().rstrip()
            elif line[:5] == 'VALUE':
                valstart = index
                break
        return variablenames


class Variable(object):

    """Creates a Variable object which contains information relating to a
    specific MEPS variable. A number of Variable objects are attributes
    of a DataSet object.
    """

    def __init__(self, datasetname, varabbv, varlongname):
        super(Variable, self).__init__()
        # The name of the dataset to which this variable belongs
        self.dataset = datasetname
        # The short name of this variable. Also the name of this variable's
        # attribute in its dataset
        self.abbv = varabbv
        self.name = varlongname     # The full name of this variable
        self.responses = []    # All responses to this variable.
        self.specials = []  # Error codes--the responses beginning with '-'
        # List of tuplets of form (response, unweighted number of response).
        self.response_counts = []
        # For a key=response (from self.responses), returns unweighted number
        # of responses as reported in the codebook. Similar to
        # self.response_counts, but dictionary syntax allows selection of a
        # specific variable.
        self.response_count = {}

        # Fetches data from MEPS html codebook. This also gives values to the
        # above empty attributes.
        self.retrieveFirstDocumentation()

    def retrieveFirstDocumentation(self):
        """Looks online and retrieves variable results from the codebook."""

        apikey = auth["importio"]["api_key"]
        apikey = quote_plus(apikey)
        # import.io POST API link
        plink = "https://api.import.io/store/data/978638d3-02fd-4772-8086-29f27a5d26b7/_query?_user=47a68269-99d8-42b9-9c7f-e281683c6531&_apikey=%s" % apikey

        headers = {'content-type': 'application/json'}  # POST headers
        lookup = {"input": {"webpage/url": "http://meps.ahrq.gov/mepsweb/data_stats/download_data_files_codebook.jsp?PUFId=%s&varName=%s" %
                            (self.dataset.upper(), self.abbv.upper())}}  # MEPS link to parse
        moveon = False
        errcounter = 0
        while moveon is False:
            try:
                req = requests.post(
                    plink, data=json.dumps(lookup), headers=headers)
            except e:
                print 'Retry Request... (%s, %s)' % (self.dataset.upper(), self.abbv.upper())
                sleep(1.5)
                errcounter += 1
                if errcounter > 5:
                    moveon = True
            else:
                moveon = True

        try:
            # Store JSON response as python data structures.
            jsonret = req.json()
        except ValueError, e:
            print '\nERROR: WEB SERVER TIMEOUT'
            print req
            raise e
        else:
            results = jsonret['results']
            if results == []:
                print "INVALID VARIABLE"
            else:
                self.responses = [x['values'] for x in results]
                self.response_counts = zip(
                    self.responses, [x['unweighted'] for x in results])
                for response_set in self.response_counts:
                    self.response_count[response_set[0]] = response_set[1]
                    if response_set[0] == '-':
                        self.specials.append(val)


def regeneratefullcache():
    dsets = ['h150', 'h152a', 'h152b', 'h152c', 'h152d', 'h152e', 'h152f', 'h152g',
             'h152h', 'h154', 'h155', 'h156']  # Ignore appendices h152if1 & h152if2
    for dset in dsets:
        print 'Generating cache for %s...' % dset.upper()
        newobj = DataSet(dset + '.pkl', True)


def main():
    # Opens the h152 DataSet object from its cached pickle.
    dset = DataSet('h155.pkl')
    print len(dset.varnames)


if __name__ == '__main__':
    # main()
    regeneratefullcache()
