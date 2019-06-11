#!/usr/bin/env python3

import json
import csv

fieldnames = ['DOI', 'publisher', 'is-referenced-by-count', 'container-title',
              'subject']

def removeEOL(str):
    return str.replace('\n', ' ').replace('\r', ' ')

with open('xrefData.json', 'rt') as injson:
    with open('xrefData.csv', 'wt') as outfile:
        wtr = csv.DictWriter(outfile, fieldnames=fieldnames)
        wtr.writeheader()
        for i in injson.readlines():
            item = json.loads(i)
            item['publisher'] = removeEOL(item['publisher'])
            title = [ removeEOL(str) for str in item['container-title'] ]
            item['container-title'] = ';'.join(title)
            subj = item.get('subject')
            if subj == None:
                item['subject'] = ''
            else:
                subj = [ removeEOL(str) for str in subj ]
                item['subject'] = ';'.join(subj)
            wtr.writerow(item)

agencyfieldnames = ['DOI', 'agency id', 'agency label']
with open('xrefErrors.json', 'rt') as inagency:
    with open('xrefAgencies.csv', 'wt') as outagency:
        wtr = csv.DictWriter(outagency, fieldnames = agencyfieldnames)
        wtr.writeheader()
        for i in inagency.readlines():
            item = json.loads(i)
            item['agency id'] = item['agency']['id']
            item['agency label'] = item['agency']['label']
            item.pop('agency')
            wtr.writerow(item)
