import csv

with open('sherp.csv') as sherp:
    rdr = csv.DictReader(sherp)
    with open('costs.csv', 'wt', newline='') as costs:
        wtr = csv.writer(costs)
        for r in rdr:
            if r['Publisher'].strip().startswith('-'):
                wtr.writerow([temp + ' ' + r['Publisher'], r['US Dollars']])
            else:
                wtr.writerow([r['Publisher'], r['US Dollars']])
                temp = r['Publisher']
