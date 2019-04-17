import csv
from pprint import pprint

with open('sherp.csv') as sherp:
    rdr = csv.DictReader(sherp)
    outlist = []
    for r in rdr:
        row = {'publisher': r['Publisher']}
        row['price'] = r['US Dollars']
        row['lower'] = None
        row['higher'] = None
        row['per'] = None
        outlist.append(row)

lines = dict(enumerate(outlist))

forremoval = []
for i, l in lines.items():
    if l['price'] in ['', '-', '$[unknown]']:
        forremoval.append(i)
    elif l['price'].lower().startswith('p'):
        lines[i-1]['per'] = 'per'
        forremoval.append(i)

for i in forremoval:
    lines.pop(i)

with open('costs.csv', 'wt', newline='') as costs:
    fieldnames=['publisher', 'price', 'lower', 'higher', 'per']
    wtr = csv.DictWriter(costs, fieldnames=fieldnames)
    wtr.writeheader()
    for i, l in lines.items():
        if l['price'].startswith('('):
            l['price'] = l['price'][1:-1]
        if '-' in l['price']:
            low, high = l['price'].split('-')
            l['lower'], l['higher'] = int(low[1:]), int(high[1:])
            l['price'] = int((l['higher'] + l['lower'])/2)
        else:
            l['price'] = l['price'][1:]
        if l['publisher'].strip().startswith('-'):
            l['publisher'] = temp + ' ' + l['publisher']
        else:
            temp = l['publisher']
        wtr.writerow(l)
