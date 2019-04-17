#! /usr/bin/env python3
import csv
import os
import json
import urllib.request
from urllib.parse import quote
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pprint import pprint as ppr

apiurl = 'https://api.unpaywall.org/v2/{0}?email=cpgrayca@uwaterloo.ca'

wosdata = []
with open('data/wos1.csv', 'rt') as wos1:
    rdr = csv.DictReader(wos1)
    for row in rdr:
        wosdata.append(row)

with open('data/wos2.csv', 'rt') as wos2:
    rdr = csv.DictReader(wos2)
    fieldnames = rdr.fieldnames
    for row in rdr:
        wosdata.append(row)

sherptitles = []
pricelist = []
with open('sherp/costs.csv', 'rt') as costs:
    rdr = csv.DictReader(costs)
    for row in rdr:
        sherptitles.append(row['publisher'])
        pricelist.append(row)

output = []
for r in wosdata:
    doi = quote(r['DOI'])
    try:
        resp = urllib.request.urlopen(apiurl.format(doi))
    except urllib.error.HTTPError:
        continue
    data = resp.read().decode('utf-8')
    jsondata = json.loads(data)
    mp = process.extract(jsondata['publisher'], sherptitles,
                         scorer=fuzz.token_sort_ratio,
                         limit=1)
    if mp[0][1] > 86:
        print('pub', jsondata['publisher'], mp)
    mj = process.extract(jsondata['journal_name'], sherptitles,
                         scorer=fuzz.token_sort_ratio,
                         limit=1)
    if mj[0][1] > 86:
        print('jou', jsondata['publisher'], mp)
