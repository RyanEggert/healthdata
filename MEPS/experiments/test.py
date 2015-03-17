# import bs4
# import requests

# with open('codebook_info/h152a.txt') as txtfile:
#     text = txtfile.readlines()
# variablenames = {}
# for index, line in enumerate(text):
#     if all(x == ' ' for x in line[:6]):
#         # These are variables and their full names
#         splitnames = line.split('=')
#         assert len(splitnames) == 2 # Throw an error if var. description has '='
#         variablenames[splitnames[0].lstrip().rstrip()] = splitnames[1].lstrip().rstrip()
#     elif line [:5] == 'VALUE':
#         valstart = index
#         break
# # print variablenames
# # print valstart
# # line = ''
# # lindex = valstart
# # line = text[lindex]
# # while lindex < len(text):   # While there's still more text file to read
# #     line = text[lindex]
# #     if line[:5] != 'VALUE':
# #         if line[:2] == '  ;':
# #             print 'end'
# #         # print '\t variable'
# #     else:
# #         print line
# #     lindex += 1
# # dset = 'h152a'
# # keys = variablenames.keys()[:1]
# # for key in keys:
# #     req = requests.get('http://meps.ahrq.gov/mepsweb/data_stats/download_data_files_codebook.jsp?PUFId=%s&varName=%s&prfricon=yes' % (dset.capitalize(), key))
# #     # print req.text
# #     html = bs4.BeautifulSoup(req.text)
# #     header =  html.body.tbody
# #     for child in header.children:
# #         print child

# # #


new = 'splitnames'
print not new


