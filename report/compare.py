#!/usr/bin/env python3

import csv
from pprint import pprint

wosdois = set([])
with open('shannon-Aug2019-0.csv', 'rt') as infile:
    rdr = csv.DictReader(infile)
    for row in rdr:
        if row['DOI'] != '-' and row['DOI'] != 'n/a':
            wosdois.add(row['DOI'])

print(len(wosdois))

total = 0
count = 0
for f in ['shannon-Aug2019-1.csv', 'shannon-Aug2019-2.csv']:
    with open(f, 'rt') as infile:
        rdr = csv.DictReader(infile)
        for row in rdr:
            if row['DOI'] != '-' and row['DOI'] != 'n/a':
                count += 1
                if row['DOI'] in wosdois:
                    total += 1
print('Count of DOIs in SciVal data:            ', count)
print('Count of DOIs unique to SciVal data:     ', total)
print('Percentage of DOIs unique to SciVal data:', total/count*100)
