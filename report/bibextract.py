#!/usr/bin/env python3

import os
import csv

## list of files from Shannon with WoS data
files = ['OA 2013-2017.csv',
         'OA 2018 WoS.csv',
         'OA other 2013-2017.csv',
         'OA other gold 2018 WoS.csv']

fieldsOfInterest = ['Accession Number', 'DOI', 'Article Title', 'Authors',
                    'Source', 'Research Area', 'Publication Date',
                    'Times Cited']

def getPubs():
    pubs = []
    dois = set([])
    for f in files:
        with open(os.path.join('../data', f), 'rt',
                  encoding='windows-1251') as bibdata:
            rdr = csv.DictReader(bibdata)
            for row in rdr:
                if row['DOI'] == None or row['DOI'] == '':
                    # this removes the summaries at the bottom of CSV files
                    continue
                if row['DOI'] not in dois:
                    pubs.append({ k: row[k] for k in fieldsOfInterest })
                    dois.add(row['DOI'])

    return pubs
