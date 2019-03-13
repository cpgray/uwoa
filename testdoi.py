import csv
from urllib.parse import quote
from habanero import Crossref

cr = Crossref()

licenses = set([])
assertions = set([])

with open('2017-extract-chris.csv', 'rt',encoding='Windows-1252',newline='\n') as csvhdl:
    rdr = csv.DictReader(csvhdl)
    for r in rdr:
        doi = quote(r['DOI'])
        data = cr.works(ids=doi)
        msg = data['message']
        for lic in msg['license']:
            
        if 'assertion' in msg.keys():
            for a in msg['assertion']:
                if a['name'] == 'copyright':
                    print(a['value'])

