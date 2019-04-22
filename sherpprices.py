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
pricelist = {}
with open('sherp/costs.csv', 'rt') as costs:
    rdr = csv.DictReader(costs)
    for row in rdr:
        sherptitles.append(row['publisher'])
        pricelist[row['publisher']] = row

output = []
fieldnames = ['doi', 'apc', 'type', 'title']
with open('sherpapcs.csv', 'wt') as apcs:
    wtr = csv.DictWriter(apcs, fieldnames=fieldnames)
    wtr.writeheader()
    for r in wosdata:
        doi = quote(r['DOI'])
        try:
            resp = urllib.request.urlopen(apiurl.format(doi))
        except urllib.error.HTTPError:
            continue
        content = resp.read().decode('utf-8')
        data = json.loads(content)
        try:
            mp = process.extract(data['publisher'], sherptitles,
                                 scorer=fuzz.token_sort_ratio,
                                 limit=1)
            mj = process.extract(data['journal_name'], sherptitles,
                                 scorer=fuzz.token_sort_ratio,
                                 limit=1)
        except TypeError:
            print(doi, data['journal_name'], data['publisher'])
            continue
        matchon = []
        if mp[0][1] > 86:
            matchon.append('publisher')
        if mj[0][1] > 86:
            matchon.append('journal')
        if len(matchon) == 0:
            continue
        if data['oa_status'] != 'hybrid' or r['Publication Date'] != '2017':
            continue
        article = {'doi': doi}
        if 'publisher' in matchon:
            article['title'] = mp[0][0]
        if 'journal' in matchon:
            article['title'] = mj[0][0]
        article['apc'] = pricelist[article['title']]['price']
        article['type'] = data['oa_status']
        wtr.writerow(article)
        apcs.flush()

