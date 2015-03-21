# opticaltest.py

from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs
from meps.data import DataSet
import meps.think.stats2 as ts2
import meps.think.plot as tplt
import matplotlib.pyplot as plt


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

# cdf = ts2.Cdf(cost_glasses)
# tplt.Cdf(cdf, label="Expenses")
# tplt.Config(title="Eyewear Expenses of People who don't use Eyewear",
#             xlabel="Expenses [ $ ]", ylabel="Cumulative Probability")
# tplt.Show()

# for every person, compute makeup of funding sources
cost_makeup = ['VISEXP12', 'VISSLF12', 'VISMCR12', 'VISMCD12',
               'VISPRV12', 'VISVA12', 'VISTRI12', 'VISOFD12', 'VISSTL12',
               'VISWCP12', 'VISOPR12', 'VISOPU12', 'VISOSR12']

cost_breakdown = discrep[cost_makeup]
counter = 0
for person in cost_breakdown.iterrows():
    p = person[1]
    cost = p['VISEXP12']
    components = sum(p[x] for x in cost_makeup if x != 'VISEXP12')
    try:
        assert cost == components
    except AssertionError, e:
        print 'WARNING: Cost imbalance.'


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
