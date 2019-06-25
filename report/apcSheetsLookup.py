#! /usr/bin/env python3

import csv
import os
from urllib.parse import quote
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pprint import pprint as ppr

fieldmap = {'publisher': 'Xref_pub',
            'is-referenced-by-count': 'Xref_timesCited',
            'container-title': 'Xref_jour',
            'subject': 'Xref_area',
            'crossref-data': 'in_Xref',
            'is_oa': 'Unpay_art_is_oa',
            'journal_is_oa': 'Unpay_jour_is_oa',
            'oa_status': 'Unpay_art_status'}
outKeys = ['DOI', 'URL', 'Article Title', 'Authors', 'Source', 'Research Area',
           'Publication Date', 'Times Cited', 'Xref_pub', 'Xref_timesCited',
           'Xref_jour', 'Xref_area', 'in_Xref', 'Unpay_art_is_oa',
           'Unpay_jour_is_oa', 'Unpay_art_status', 'Filename', 'apc cost',
           'cost source']

mainData = {}
with open('unpayAdded.csv', 'rt') as mainfile:
    rdr = csv.DictReader(mainfile)
    inFNs = rdr.fieldnames
    for k in inFNs:
        if k not in fieldmap.keys():
            fieldmap[k] = k
    for row in rdr:
        mainData[row['DOI']] = { fieldmap[k]: row[k] for k in row }

outFNs = [ fieldmap[k] for k in inFNs ]

pricelist = []
for f in os.listdir('../apc'):
    with open('../apc/'+f, 'rt', encoding='windows-1252') as fdata:
        rdr = csv.DictReader(fdata)
        #print(f, rdr.fieldnames)
        if 'Title' in rdr.fieldnames and 'USD' in rdr.fieldnames:
            for row in rdr:
                if row['Title'] != '':
                    pricelist.append({'File': f, 'Title': row['Title'],
                                      'USD': row['USD']})
        elif 'Title' in rdr.fieldnames and 'APC USD ' in rdr.fieldnames:
            for row in rdr:
                pricelist.append({'File': f, 'Title': row['Title'],
                                  'USD': row['APC USD ']})
        elif 'Title' in rdr.fieldnames and 'CHF' in rdr.fieldnames:
            for row in rdr:
                pricelist.append({'File': f, 'Title': row['Title'],
                                  'USD': row['CHF']})
        else:
            #print(f)
            for row in rdr:
                if row['Currency'] == 'EUR':
                    USD = str(int(round(float(row['Price'])*1.12)))
                elif row['Currency'] == 'USD':
                    USD = row['Price']
                else:
                    print('????', row['Currency'], '????')
                pricelist.append({'File': f, 'Title': row['Journal title'],
                                  'USD': USD})

sherptitles = []
sherpprices = {}
with open('../sherp/costs.csv', 'rt') as costs:
    rdr = csv.DictReader(costs)
    for row in rdr:
        sherptitles.append(row['publisher'])
        sherpprices[row['publisher']] = row
                
with open('report.csv', 'wt') as outfile:
    wtr = csv.DictWriter(outfile, fieldnames=outKeys)
    wtr.writeheader()
    for k in mainData.keys():
        r = {}
        for price in pricelist:
            p = price['Title'].lower()
            s = mainData[k]['Source'].lower()
            if p == s or p[4:] == s:
                r = mainData[k]
                r['apc cost'] = price['USD']
                r['cost source'] = price['File']
                break
        if r == {}:
            mp = process.extract(mainData[k]['Xref_pub'], sherptitles,
                                 scorer=fuzz.token_sort_ratio,
                                 limit=1)
            if mp[0][1] > 86:
                r = mainData[k]
                r['apc cost'] = sherpprices[mp[0][0]]['price']
                r['cost source'] = 'SHERPA/ROMEO'
            else:
                r = mainData[k]
                r['apc cost'] = 2100
                r['cost source'] = 'Default Value'
        doi = quote(r['DOI'])
        url = 'https://dx.doi.org/{0}'.format(doi)
        r['URL'] = '=HYPERLINK("{0}")'.format(url)
        wtr.writerow(r)

