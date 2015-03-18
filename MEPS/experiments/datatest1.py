# import dataio as dio
import thinkstats2 as ts2
import thinkplot as tplt
import DataSet
import pdb

H155 = DataSet.DataSet('h155.pkl')

df = H155.df
errorlist = []
totalvars = len(H155.varnames)
for index, var in enumerate(H155.varnames):

    print '\nPlotting %s, variable %d out of %d.' % (var, index+1, totalvars)
    thisplot = df[df[var] > 0][var]
    try:
        thishist = ts2.Cdf(thisplot)
        tplt.Cdf(thishist)
        tplt.Config(title=var, ylabel='Probability', xlabel='Response')
    except Exception, e:
        print 'ERROR CREATING %s' % var
        errorlist.append((var, e))
    else:
        tplt.SaveFormat('graphs/cdftests2/%s' % var, 'png')
        tplt.Clf()

# Exclude error codes
# Title the graphs
# place counter in for loop
print errorlist
with open('graphs/cdftests2/errorlog.txt', 'wb+') as wrfile:
    for err in errorlist:
        wrfile.write("%s\n" % err)
