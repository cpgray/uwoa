#!/usr/bin/env python3

import csv
import json
from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError
from collections import defaultdict

unpayurl = 'https://api.unpaywall.org/v2/{0}?email=cpgrayca@uwaterloo.ca'

unpayFoI = ['is_oa', 'journal_is_oa', 'oa_status']

unpayValues = defaultdict(set)

with open('combined.csv', 'rt') as infile:
    rdr = csv.DictReader(infile)
    for row in rdr:
        doi = quote(row['DOI'])
        try:
            resp = urlopen(unpayurl.format(doi))
        except HTTPError as e:
            print(doi)
            print(str(e))
            continue
        unpayJSON = resp.read().decode('utf-8')
        unpayResp = json.loads(unpayJSON)
        for k in unpayFoI:
            unpayValues[k].add(unpayResp[k])
    for k in unpayFoI:
        print(k, unpayValues[k])
    

