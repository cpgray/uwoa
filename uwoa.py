#! /usr/bin/env python3
import csv
import os
import json
import urllib.request
from collections import Counter
from urllib.parse import quote
from pprint import pprint as ppr

apiurl = 'https://api.unpaywall.org/v2/{0}?email=cpgrayca@uwaterloo.ca'

wosdata = []
with open('data/wos1.csv', 'rt') as wos1:
    rdr = csv.DictReader(wos1)
    for row in rdr:
        wosdata.append(row)

with open('data/wos2.csv', 'rt') as wos2:
    rdr = csv.DictReader(wos2)
    fieldnames = rdr.fieldnames
    for row in rdr:
        wosdata.append(row)
        
#for row in wosdata:
#    print(row['Source'], row['DOI'])

pricelist = []
for f in os.listdir('apc'):
    with open('apc/'+f, 'rt', encoding='Latin-1') as fdata:
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

output = []
for r in wosdata:
    #match = False
    for price in pricelist:
        if r['Publication Date'] != '2017':
            continue
        p = price['Title'].lower()
        s = r['Source'].lower()
        if p == s:
            doi = quote(r['DOI'])
            try:
                resp = urllib.request.urlopen(apiurl.format(doi))
            except:
                continue
            content = resp.read().decode('utf-8')
            data = json.loads(content)
            #match = True
            if data['oa_status'] in ['closed', 'green']:
                continue
            article = {'doi': r['DOI'], 'apc':price['USD']}
            article['type'] = data['oa_status']
            article['title'] = price['Title']
            output.append(article)
            #ppr(article)
            continue

fieldnames = ['doi', 'apc', 'type', 'title'] 
with open('costs.csv', 'wt') as cost:
    wtr = csv.DictWriter(cost, fieldnames=fieldnames)
    wtr.writeheader()
    for i in output:
        wtr.writerow(i)

#fieldnames = ['File', 'Title', 'USD']
#with open('pricelist.csv', 'wt') as pl:
#    wtr = csv.DictWriter(pl, fieldnames=fieldnames)
#    wtr.writeheader()
#    for r in pricelist:
#        wtr.writerow(r)

#matched = []
#unmatched = []
#for row in wosdata:
#    match = False
#    for price in pricelist:
#        p = price['Title'].lower()
#        s = row['Source'].lower()
#        if p == s:
#            matched.append(row['Source'])
#            match = True
#    else:
#        if not match:
#            unmatched.append(row['Source']) 

#print(unmatched)
#print(len(unmatched))
#c = Counter(matched)
#for k, v in c.most_common():
#    print('{}\t{}'.format(v, k))
#print(sum(c.values()))
