#!/usr/bin/env python3

import os
import csv

for f in os.listdir('../data'):
    with open(os.path.join('../data', f), 'rt',
              encoding='windows-1251') as bibdata:
        rdr = csv.DictReader(bibdata)
        print('-----',f,'-----')
        print(rdr.fieldnames)
