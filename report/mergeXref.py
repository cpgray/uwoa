#!/usr/bin/env python3

import csv
from pprint import pprint

bibFoI = ['DOI', 'Filename', 'Article Title', 'Authors', 'Source',
          'Research Area', 'Publication Date', 'Times Cited']
xrefFoI = ['DOI', 'publisher', 'is-referenced-by-count',
           'container-title', 'subject']
mergedFoI = ['DOI', 'Filename', 'Article Title', 'Authors', 'Source',
             'Research Area', 'Publication Date', 'Times Cited', 'publisher',
             'is-referenced-by-count', 'container-title', 'subject',
             'crossref-data']

dataWoSScopus = {}
with open('combined.csv', 'rt') as wsd:
    rdr= csv.DictReader(wsd)
    for r in rdr:
        dataWoSScopus[r['DOI']] = r
    
xrefData = {}
with open('xrefData.csv', 'rt') as xrd:
    rdr = csv.DictReader(xrd)
    for r in rdr:
        xrefData[r['DOI']] = r

xrefOther = {}
with open('xrefAgencies.csv', 'rt') as xro:
    rdr = csv.DictReader(xro)
    for r in rdr:
        xrefOther[r['DOI']] = r

with open('xrefMerged.csv', 'wt') as xmcsv:
    wtr = csv.DictWriter(xmcsv, fieldnames = mergedFoI)
    wtr.writeheader()
    for k in dataWoSScopus:
        if k in xrefData.keys():
            row = {**dataWoSScopus[k], **xrefData[k]}
            row['crossref-data'] = True
        elif k in xrefOther.keys():
            row = dataWoSScopus[k]
            for f in xrefFoI:
                if f != 'DOI':
                    row[f] = None
            row['crossref-data'] = False
        wtr.writerow(row)

