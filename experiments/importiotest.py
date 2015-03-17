import requests
from urllib import quote_plus
import json


def varget(datasetname, varname):
    pass
    apikey = 'kQTjOqputO8bYhjMRTedVczQrkLDfep0GkK8fOn8uZge1yXEOxmga5NrJzGGUNpV5G7xUOnPFJ502dZGDCQl+w=='
    apikey = quote_plus(apikey)
    plink = "https://api.import.io/store/data/978638d3-02fd-4772-8086-29f27a5d26b7/_query?_user=47a68269-99d8-42b9-9c7f-e281683c6531&_apikey=%s" % apikey

    headers = {'content-type': 'application/json'}
    lookup = {"input": {"webpage/url": "http://meps.ahrq.gov/mepsweb/data_stats/download_data_files_codebook.jsp?PUFId=%s&varName=%s" %
                        (datasetname.upper(), varname.upper())}}
    req = requests.post(plink, data=json.dumps(lookup), headers=headers)
    jsonret = req.json()

    results = jsonret['results']
    if results == []:
        print "INVALID VARIABLE"
    # print results[1].keys()
    vals = [x['values'] for x in results]
    for val in vals:
        if val[0] == '-':
            print val


def main():
    varget('h155', 'IADL3M31')


if __name__ == '__main__':
    main()
