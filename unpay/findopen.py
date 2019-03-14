import csv
import json
import urllib.request
from urllib.parse import quote

with open('data/2017-extract-chris.csv', 'rt',encoding='Windows-1252',newline='\n') as csvhdl:
    rdr = csv.DictReader(csvhdl)
    for r in rdr:
        doi = quote(r['DOI'])
        apiurl = 'https://api.unpaywall.org/v2/{0}?email=cpgrayca@uwaterloo.ca'.format(doi)
        resp = urllib.request.urlopen(apiurl)
        content = resp.read().decode('utf-8')
        data = json.loads(content)
        if data['is_oa']:
            #print(json.dumps(data, indent=2))
            print(data['is_oa'], data['oa_status'], data['publisher'], doi)
