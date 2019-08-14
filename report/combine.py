#!/usr/bin/env python3

import os
import csv

fieldsOfInterest = ['DOI', 'Article Title', 'Authors', 'Source',
                    'Research Area', 'Publication Date', 'Times Cited',
                    'Institutions']
ScopusFoI = ['DOI', 'Title', 'Authors', 'Scopus Source title',
             'All Science Journal Classification (ASJC) Field Name', 'Year',
             'Citations', 'Institutions']
Scopus2WoS = {'DOI': 'DOI',
              'Title': 'Article Title',
              'Authors': 'Authors',
              'Scopus Source title': 'Source',
              'All Science Journal Classification (ASJC) Field Name':
              'Research Area',
              'Year': 'Publication Date',
              'Citations': 'Times Cited',
              'Institutions': 'Institutions'}

## combine/filter: reduce fields, deduplicate, remove items without DOIs
newFiles = []
with open('fileOrigins-Aug2019.csv', 'rt') as infiles:
    rdr = csv.DictReader(infiles)
    for row in rdr:
        newFiles.append( (row['New'], row['Old']) )

newRows = {}    
for n, o in newFiles:
    with open(n, 'rt') as infile:
        rdr = csv.DictReader(infile)
        for row in rdr:
            if row.get('Document Type') != 'Article' and row.get('Publication-type') != 'Article':
                continue
            doi = row['DOI']
            if doi == 'n/a' or doi == '-':
                continue
            if 'Institutions' not in rdr.fieldnames or row['Institutions'] != 'University of Waterloo':
                row['Institutions'] = None
            if 'Title' in row.keys():
                for k in ScopusFoI:
                    row[Scopus2WoS[k]] = row.pop(k)
            newRow = { k:row[k] for k in fieldsOfInterest }
            if doi in newRows.keys():
                newRows[doi]['Filename'].append(o)
                if row['Institutions'] == 'University of Waterloo':
                    newRows[doi]['Institutions'] = 'University of Waterloo'
            else:
                newRow['Filename'] = [o]
                newRows[doi] = newRow

## create new output file with all data combined and filtered
with open('combined-2019.csv', 'wt') as outfile:
    wtr = csv.DictWriter(outfile,
                         fieldnames = fieldsOfInterest + ['Filename'])
    wtr.writeheader()
    for k in newRows.keys():
        # change the list of filenames into a comma delimited string
        newRows[k]['Filename'] = ','.join(newRows[k]['Filename'])
        wtr.writerow(newRows[k])
