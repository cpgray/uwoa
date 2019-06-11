#!/usr/bin/env python3

import os
import csv
import json
from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError
from pprint import pprint
from time import sleep

xrefURL = 'https://api.crossref.org/works/{0}?'
xrefURL += 'mailto=libxrefclient@library.uwaterloo.ca'

xrefFoI = ['DOI', 'publisher', 'is-referenced-by-count', 'container-title',
           'subject']

agencyURL = 'https://api.crossref.org/works/{0}/agency'

def rmfile(fpath):
    try:
        os.remove(fpath)
    except:
        pass

for fn in ['xref404.csv', 'xrefErrors.json', 'xrefData.json']:
    rmfile(fn)

with open('combined.csv', 'rt') as infile:
    rdr = csv.DictReader(infile)
    for l in rdr:
        doi = quote(l['DOI'])
        try:
            resp = urlopen(xrefURL.format(doi))
        except HTTPError as e:
            try:
                resp2 = urlopen(agencyURL.format(doi))
            except HTTPError as e2:
                with open('xref404.csv', 'at') as notfound:
                    notfound.write(doi + ',' + str(e2) + '\n')
                continue
            agencyJSON = resp2.read().decode('utf-8')
            agencyResp = json.loads(agencyJSON)
            data = agencyResp['message']
            with open('xrefErrors.json', 'at') as errout:
                errout.write(json.dumps(data) + '\n')
            continue
        xrefJSON = resp.read().decode('utf-8')
        xrefResp = json.loads(xrefJSON)
        if xrefResp['status'] == 'ok':
            xrefData = xrefResp['message']
            filtered = { k: xrefData.get(k) for k in xrefFoI }
            with open('xrefData.json', 'at') as outfile:
                outfile.write(json.dumps(filtered) + '\n')
        sleep(0.1)
