#!/usr/bin/env python3

import csv
import json
from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError

unpayurl = 'https://api.unpaywall.org/v2/{0}?email=cpgrayca@uwaterloo.ca'

xrefMergedFoI = ['DOI', 'Filename', 'Article Title', 'Authors', 'Institutions',
                 'Source', 'Research Area', 'Publication Date', 'Times Cited',
                 'publisher', 'is-referenced-by-count', 'container-title',
                 'subject', 'crossref-data']
unpayFoI = ['is_oa', 'journal_is_oa', 'oa_status']
mergedFoI = xrefMergedFoI + unpayFoI

with open('xrefMerged-2019.csv', 'rt') as infile:
    rdr = csv.DictReader(infile)
    with open('unpayAdded-2019.csv', 'wt') as outfile:
        wtr = csv.DictWriter(outfile, fieldnames=mergedFoI)
        wtr.writeheader()
        for row in rdr:
            doi = quote(row['DOI'])
            try:
                resp = urlopen(unpayurl.format(doi))
            except HTTPError as e:
                for k in unpayFoI:
                    row[k] = None
                wtr.writerow(row)
                continue
            except Exception as e:
                print('Not an HTTPError')
                print('DOI: ', doi)
                print(e)
                continue
            unpayJSON = resp.read().decode('utf-8')
            unpayResp = json.loads(unpayJSON)
            filtered = { key:unpayResp[key] for key in unpayFoI }
            wtr.writerow({**row, **filtered})

