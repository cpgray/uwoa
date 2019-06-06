#!/usr/bin/env python3

import bibextract
import csv
from pprint import pprint

pubs = bibextract.getPubs()

pprint(pubs)

with open('pubsReport.csv', 'wt') as pubscsv:
    wtr = csv.DictWriter(pubscsv, fieldnames=bibextract.fieldsOfInterest)
    wtr.writeheader()
    for row in pubs:
        wtr.writerow(row)

