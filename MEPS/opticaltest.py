# opticaltest.py

from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs
from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from numpy import linspace as nplinspace


def summarydict(vars):
    outdict = {}
    for var in vars:
        outdict[var] = []
    return outdict

h155 = DataSet('h155.pkl')
df_u = h155.df

# Clean dataframe
df = cleanallerrs(df_u)

# Select those who do not report wearing glasses/contacts
no_eyewear = df[df['WRGLAS42'] == 2]

# Remove those who wear no eyewear AND reported no eyewear expense
discrep = no_eyewear[no_eyewear['VISEXP12'] > 0]

# Lets look at the reported eyewear expenses of those who don't wear eyewear
cost_glasses = discrep['VISEXP12']

print 'Avg cost: $%.2f' % cost_glasses.mean()
print 'St. Dev.: $%.2f' % (cost_glasses.std())
print 'Median: $%.2f' % (cost_glasses.median())
print 'Range of costs: $%.2f - $%.2f' % (cost_glasses.min(), cost_glasses.max())
print 'Number of people: %d' % (cost_glasses.shape)
print 'Number of NaNs: %d' % (cost_glasses.isnull().sum())


# for every person, compute makeup of funding sources
cost_makeup = ['VISEXP12', 'VISSLF12', 'VISMCR12', 'VISMCD12',
               'VISPRV12', 'VISVA12', 'VISTRI12', 'VISOFD12', 'VISSTL12',
               'VISWCP12', 'VISOPR12', 'VISOPU12', 'VISOSR12']
makeupvars = cost_makeup[1:]
cost_breakdown = discrep[cost_makeup]
counter = 0
aggr_bd = []
for person in cost_breakdown.iterrows():
    p = person[1]
    cost = p['VISEXP12']
    components = sum(p[x] for x in cost_makeup if x != 'VISEXP12')
    try:
        assert cost == components
    except AssertionError, e:
        print 'WARNING: Cost imbalance.'
    bd_dict = {}
    for makeupvar in makeupvars:
        bd_dict[makeupvar] = float(p[makeupvar]) / float(p['VISEXP12'])
    aggr_bd.append(bd_dict)


combined_dict = summarydict(makeupvars)
mean_dict = summarydict(makeupvars)
use_dict = summarydict(makeupvars)

labels = {}

for key in aggr_bd[1]:
    for person in aggr_bd:
        combined_dict[key].append(person[key])

for key in combined_dict:
    thisvar = combined_dict[key]
    mean_dict[key] = sum(thisvar) / float(len(thisvar))
    thisexists = [x for x in thisvar if x > 0]
    use_dict[key] = len(thisexists) / float(len(thisvar))
    labels[key] = getattr(h155, key).name

print use_dict
print
print labels

plt.Figure()
cdf = ts2.Cdf(cost_glasses)
tplt.Cdf(cdf, label="Expenses")
tplt.Config(title="Eyewear Expenses of People who don't use Eyewear",
            xlabel="Expenses [ $ ]", ylabel="Cumulative Probability")
tplt.Show()
colors = cm.jet(nplinspace(0, 1, len(use_dict)))
plt.pie([use_dict[key] for key in use_dict], shadow=True, colors=colors)
plt.axis('equal')
plt.legend([labels[key] for key in labels], shadow=True, prop={'size': 10})
plt.show()


# Vision impairment characterization

# VISION42

# EXP
# SLF
# MCR
# MCD
# PRV
# VA
# TRI
# OFD
# STL
# WCP
# OPR
# OPU
# OSR
