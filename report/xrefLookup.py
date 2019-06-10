#!/usr/bin/env python3

import csv
import json
from urllib.request import urlopen
from urllib.parse import quote
from pprint import pprint
from time import sleep

xrefURL = 'https://api.crossref.org/works/{0}?'
xrefURL += 'mailto=libxrefclient@library.uwaterloo.ca'

xrefFoI = ['publisher', 'is-referenced-by-count', 'container-title', 'subject']

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
