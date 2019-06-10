#!/usr/bin/env python3

import os
import csv

fieldsOfInterest = ['DOI', 'Article Title', 'Authors', 'Source',
                    'Research Area', 'Publication Date', 'Times Cited']
ScopusFoI = ['DOI', 'Title', 'Authors', 'Source title', 'Index Keywords',
             'Year', 'Cited by']
Scopus2WoS = {'DOI': 'DOI',
              'Title': 'Article Title',
              'Authors': 'Authors',
              'Source title': 'Source',
              'Index Keywords': 'Research Area',
              'Year': 'Publication Date',
              'Cited by': 'Times Cited'}

## combine/filter: reduce fields, deduplicate, remove items without DOIs
newFiles = []
with open('fileOrigins.csv', 'rt') as infiles:
    rdr = csv.DictReader(infiles)
    for row in rdr:
        newFiles.append( (row['New'], row['Old']) )

newRows = {}    
for n, o in newFiles:
    with open(n, 'rt') as infile:
        rdr = csv.DictReader(infile)
        for row in rdr:
            doi = row['DOI']
            if doi == 'n/a':
                continue
            if 'Title' in row.keys():
                for k in ScopusFoI:
                    row[Scopus2WoS[k]] = row.pop(k)
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
