import dataio as dio


dsets = ['h152a', 'h152b', 'h152c', 'h152d', 'h152e', 'h152f', 'h152g', 'h152h', 'h152if1', 'h152if2']
dsets2 = ['h156']
for dset in dsets2:
    dio.firstimport(dset+'_processed.csv')
    print 'imported ' + dset
