import dataio as dio
import thinkstats2 as ts2
import thinkplot as tplt
import pandas as pd


def validateID(datasetname, variable):
    dset = dio.importdata(datasetname + '.pkl')
    try:
        pid_hist = ts2.Hist(dset[variable])
    except KeyError:
        print "%s WARNING!: VARIABLE %s NOT FOUND" % (datasetname, variable)
    else:
        items = pid_hist.Items()
        allfreqs = [x[1] for x in items]
        allfreqs.sort()
        if all(freq == 1 for freq in allfreqs):
            print "%s--%s: UNIQUENESS VALIDATED" % (datasetname, variable)
        else:
            print "%s--%s: UNIQUENESS FAILED" % (datasetname, variable)


def main():
    dsets = ['h152a', 'h152b', 'h152c', 'h152d', 'h152e', 'h152f',
             'h152g', 'h152h', 'h152if1', 'h152if2', 'h155', 'h156', 'h154', 'h150']

    for dset in dsets:
        validateID(dset, 'PID')
        validateID(dset, 'DUPERSID')

if __name__ == '__main__':
    main()
