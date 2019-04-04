import csv
import json
import urllib.request
from urllib.parse import quote
from collections import defaultdict

errorlog = open('unpay/error.txt', 'wt')

publishers = defaultdict(list)

# wosout.fieldnames =
# ['Accession Number', 'DOI', 'Pubmed ID', 'Article Title', 'Link', 'Authors',
# 'Source', 'Research Area', 'Volume', 'Issue', 'Pages', 'Publication Date',
# 'Times Cited', 'Journal Expected Citations', 'Category Expected Citations',
# 'Journal Normalized Citation Impact', 'Category Normalized Citation Impact',
# 'Percentile in Subject Area', 'Journal Impact Factor']

with open('data/OA 2013-2017.csv', 'rt', newline='\n') as wosout:
    rdr = csv.DictReader(wosout)
    #count=0
    for r in rdr:
        #count += 1
        
        doi = quote(r['DOI'])
        apiurl = 'https://api.unpaywall.org/v2/{0}?email=cpgrayca@uwaterloo.ca'
        try:
            resp = urllib.request.urlopen(apiurl.format(doi))
        except Exception as e:
            errorlog.write(doi+'\n')
            errorlog.write(repr(e)+'\n')
            continue
        content = resp.read().decode('utf-8')
        data = json.loads(content)

        ##  Show highest level data only ##
        #rejectedKeys = ['best_oa_location', 'oa_locations', 'z_authors']
        #filteredKeys = [ k for k in data.keys() if k not in rejectedKeys ]
        #filtered = { k: data[k] for k in filteredKeys }
        #print(json.dumps(filtered, indent=2))
        
        selectFields = ['genre', 'is_oa', 'journal_is_in_doaj',
                        'journal_is_oa', 'journal_issns', 'journal_name',
                        'oa_status', 'publisher']
        dataOfInterest = { k: data[k] for k in selectFields }
        #print(json.dumps(dataOfInterest, indent=2))

        publishers[data['publisher']].append(data['doi'])

        #if count > 20:
        #    break

errorlog.close()

for k, v in publishers.items():
    print(k, len(v))
