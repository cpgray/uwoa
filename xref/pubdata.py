import csv
from urllib.parse import quote
from habanero import Crossref

cr = Crossref()

licenses = set([])
assertions = set([])

with open('unpay',encoding='Windows-1252',newline='\n') as csvhdl:
    rdr = csv.DictReader(csvhdl)
    for r in rdr:
        doi = quote(r['DOI'])
        data = cr.works(ids=doi)
        msg = data['message']
        

