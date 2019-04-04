#! /usr/bin/env python3
import csv
import os

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
        
#for row in wosdata:
#    print(row['Source'], row['DOI'])

pricelist = []
for f in os.listdir('apc'):
    with open('apc/'+f, 'rt', encoding='windows-1252') as fdata:
        rdr = csv.DictReader(fdata)
        print(f, rdr.fieldnames)
        if 'Title' in rdr.fieldnames and 'USD' in rdr.fieldnames:
            for row in rdr:
                if row['Title'] != '':
                    pricelist.append({'File': f, 'Title': row['Title'],
                                      'USD': row['USD']})
        elif 'Title' in rdr.fieldnames and 'APC USD ' in rdr.fieldnames:
            for row in rdr:
                pricelist.append({'File': f, 'Title': row['Title'],
                                  'USD': row['APC USD ']})
        elif 'Title' in rdr.fieldnames and 'CHF' in rdr.fieldnames:
            for row in rdr:
                pricelist.append({'File': f, 'Title': row['Title'],
                                  'USD': row['CHF']})
        else:
            print(f)
            for row in rdr:
                if row['Currency'] == 'EUR':
                    USD = str(int(round(float(row['Price'])*1.12)))
                elif row['Currency'] == 'USD':
                    USD = row['Price']
                else:
                    print('????', row['Currency'], '????')
                pricelist.append({'File': f, 'Title': row['Journal title'],
                                  'USD': USD})

fieldnames = ['File', 'Title', 'USD']
with open('pricelist.csv', 'wt') as pl:
    wtr = csv.DictWriter(pl, fieldnames=fieldnames)
    wtr.writeheader()
    for r in pricelist:
        wtr.writerow(r)
