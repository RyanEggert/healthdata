import dataio as dio

# imports all of the listed datasets from csv and saves to pickle.
dsets = ['h152a', 'h152b', 'h152c', 'h152d', 'h152e', 'h152f', 'h152g', 'h152h', 'h152if1', 'h152if2', 'h155', 'h156']

for dset in dsets:
    dio.firstimport(dset+'.csv')
    print 'imported ' + dset
