#! /usr/bin/env python3

import csv
from collections import defaultdict

with open('fileOrigins-Aug2019.csv', 'rt') as orgf:
    origins = {}
    rdr = csv.DictReader(orgf)
    for r in rdr:
        origins[r['Old']] = r['New']

with open('dups_in_scival.csv', 'rt') as dupf:
    dups = {}
    rdr = csv.DictReader(dupf)
    for r in rdr:
        for i in list(set(r['CSV files'].split(','))):
            if i.startswith('SciVal'):
                dups[r['DOI']] = origins[i]

records = defaultdict(list)
for f in ['shannon-Aug2019-1.csv', 'shannon-Aug2019-2.csv']:
    with open(f, 'rt') as inf:
        rdr = csv.DictReader(inf)
        fns = rdr.fieldnames
        for r in rdr:
            if r['DOI'] in dups.keys():
                records[r['DOI']].append(r)

with open('duprprt.csv', 'wt') as outf:
    wtr = csv.DictWriter(outf, fieldnames=fns, dialect="excel")
    wtr.writeheader()
    for k in records.keys():
        for rec in records[k]:
            wtr.writerow(rec)
