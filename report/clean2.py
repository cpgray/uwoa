#!/usr/bin/env python3

import os
from subprocess import Popen, PIPE

## list of files from Shannon
files = ['InCites 2013-2018 Waterloo affiliated pubs.csv',
         'SciVal 2017-2018 Waterloo affiliated pubs.csv',
         'SciVal 2013-2016 Waterloo affiliated pubs.csv']

## Create new renamed files in UTF-8 encoding with summaries removed
newFiles = []
for i, f in enumerate(files):
    newFn = 'shannon-Aug2019-' + str(i) + '.csv'
    newFiles.append( (newFn, f) )
    fn = os.path.join('../data', f)
    with open(fn, 'rt', encoding='Latin-1') as infile:
        p = Popen(['dos2unix'], stdout=PIPE, stderr=PIPE,
                  encoding='Latin-1', stdin=infile)
        with open(newFn, 'wt') as outfile:
            section = 'header'
            for l in p.stdout.readlines():
                if section == 'header':
                    if l.startswith('Title') or l.startswith('Accession'):
                        section = 'body'
                elif section == 'body':
                    if l.startswith(','):
                        section = 'tail'
                if section == 'body':
                    outfile.write(l)

## record manifest of new files and their origin files
with open('fileOrigins-Aug2019.csv', 'wt') as manifest:
    manifest.write('Old,New\n')
    for a, b in newFiles:
        manifest.write('"{0}",{1}\n'.format(b, a))
