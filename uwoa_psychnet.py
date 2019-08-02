#! /usr/bin/env python3
import csv
import os
import json
from urllib.request import urlopen
from urllib.parse import quote
from pprint import pprint

apiurl = 'https://api.unpaywall.org/v2/{0}?email=cpgrayca@uwaterloo.ca'
fsOfInterest = ['DocumentType', 'PublicationName', 'Publisher',
                'PublicationYear', 'ISSN', 'ISBN', 'DOI']
unpayFsoI = ['doi', 'genre', 'is_oa', 'journal_is_oa', 'journal_issns',
             'journal_name', 'oa_status']

psynetdata = []
with open('data/psychnet.csv', 'rt') as psynet:
    rdr = csv.DictReader(psynet)
    for row in rdr:
        psynetdata.append({ k:row[k] for k in fsOfInterest})

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
for r in psynetdata:
    doi = quote(r['DOI'][18:])
    try:
        resp = urlopen(apiurl.format(doi))
    except:
        continue
    content = resp.read().decode('utf-8')
    data = json.loads(content)
    if 'is_oa' in data.keys() and 'journal_name' in data.keys():
        if data['is_oa'] is not False:
            if data['oa_status'] == 'hybrid':
                for price in pricelist:
                    s = data['journal_name'].lower()
                    p = price['Title'].lower()
                    if p == s:
                        article = {'doi': doi, 'apc':price['USD']}
                        article['type'] = data['oa_status']
                        article['title'] = price['Title']
                        output.append(article)

fieldnames = ['doi', 'apc', 'type', 'title']
with open('pncosts.csv', 'wt') as cost:
    wtr = csv.DictWriter(cost, fieldnames=fieldnames)
    wtr.writeheader()
    for i in output:
        wtr.writerow(i)
            
    
