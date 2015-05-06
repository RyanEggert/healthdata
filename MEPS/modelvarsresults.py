# modelvarsresults.py

import dill as pkl

with open('modelallvars_res.pkl', 'rb') as pcklfile:
    res = pkl.load(pcklfile)

print res['errors']
