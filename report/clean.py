#!/usr/bin/env python3

import os

## list of files from Shannon
files = ['OA 2013-2017.csv',
         'OA 2018 WoS.csv',
         'OA other 2013-2017.csv',
         'OA other gold 2018 WoS.csv',
         'OA 2018 Scopus.csv']

## Create new renamed files in utf-8 encoding with summaries removed
newFiles = []
for i, f in enumerate(files):
    newFn = 'shannon' + str(i) + '.csv'
    newFiles.append( (newFn, f) )
    fn = os.path.join('../data', f)
    with open(fn, 'rt', encoding='windows-1251') as infile:
        with open(newFn, 'wt') as outfile:
            for l in infile.readlines():
                if ',,,,,,,,' in l:
                    # stop after separator between data and summary reached
                    break
                else:
                    outfile.write(l)

## record manifest of new files and their origin files
with open('fileOrigins.csv', 'wt') as manifest:
    manifest.write('Old,New\n')
    for a, b in newFiles:
        manifest.write('"{0}",{1}\n'.format(b, a))

