#!/usr/bin/env python3

import os
import csv
import json
from urllib.request import urlopen
from urllib.parse import quote
from pprint import pprint
from time import sleep

## list of files from Shannon with WoS data
files = ['OA 2013-2017.csv',
         'OA 2018 WoS.csv',
         'OA other 2013-2017.csv',
         'OA other gold 2018 WoS.csv']

fieldsOfInterest = ['Accession Number', 'DOI', 'Article Title', 'Authors',
                    'Source', 'Research Area', 'Publication Date',
                    'Times Cited']

xrefURL = 'https://api.crossref.org/works/{0}?'
xrefURL += 'mailto=libxrefclient@library.uwaterloo.ca'

xrefFoI = ['publisher', 'is-referenced-by-count', 'container-title', 'subject']

## Create new renamed files in utf-8 encoding with summaries removed
newFiles = []
for i, f in enumerate(files):
    newFn = 'wos' + str(i) + '.csv'
    newFiles.append( (newFn, f) )
    fn = os.path.join('../data', f)
    with open(fn, 'rt', encoding='windows-1251') as infile:
        with open(newFn, 'wt') as outfile:
            for l in infile.readlines():
                if ',,,,,,,,' in l:
                    # stop after separator between data and summary reached
                    break
                else:
                    outfile.write(l)

## record manifest of new files and their origin files
with open('fileOrigins.csv', 'wt') as manifest:
    manifest.write('Old,New\n')
    for a, b in newFiles:
        manifest.write('"{0}",{1}\n'.format(b, a))

## combine/filter: reduce fields, deduplicate, remove items without DOIs
newRows = {}
for n, o in newFiles:
    with open(n, 'rt') as infile:
        rdr = csv.DictReader(infile)
        for row in rdr:
            doi = row['DOI']
            if doi == 'n/a':
                continue
            newRow = { k:row[k] for k in fieldsOfInterest }
            if doi in newRows.keys():
                newRows[doi]['Filename'].append(o)
            else:
                newRow['Filename'] = [o]
                newRows[doi] = newRow

## create new output file with all data combined and filtered
with open('combined.csv', 'wt') as outfile:
    wtr = csv.DictWriter(outfile,
                         fieldnames = fieldsOfInterest + ['Filename'])
    wtr.writeheader()
    for k in newRows.keys():
        # change the list of filenames into a comma delimited string
        newRows[k]['Filename'] = ','.join(newRows[k]['Filename'])
        wtr.writerow(newRows[k])

with open('combined.csv', 'rt') as infile:
    rdr = csv.DictReader(infile)
    for l in rdr:
        doi = quote(l['DOI'])
        resp = urlopen(xrefURL.format(doi))
        xrefJSON = resp.read().decode('utf-8')
        xrefResp = json.loads(xrefJSON)
        if xrefResp['status'] == 'ok':
            xrefData = xrefResp['message']
            filtered = { k: xrefData.get(k) for k in xrefFoI }
            print(json.dumps(filtered, indent=2))
        sleep(5)
