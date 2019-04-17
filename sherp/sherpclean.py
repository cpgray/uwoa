import csv
from pprint import pprint

with open('sherp.csv') as sherp:
    rdr = csv.DictReader(sherp)
    with open('costs.csv', 'wt', newline='') as costs:
        fieldnames=['publisher', 'price', 'lower', 'upper', 'per']
        wtr = csv.DictWriter(costs, fieldnames=fieldnames)
        wtr.writeheader()
        outl = {}
        for r in rdr:
            if r['US Dollars'].startswith('('):
                price = r['US Dollars'][1:-1]
            else:
                price = r['US Dollars']
            if '-' in price and price != '-':
                price = price.split('-')
                low = int(price[0][1:])
                high = int(price[1][1:])
                price = int((low + high)/2)
            elif price.startswith('$'):
                low = None
                high = None
                price = price[1:]
            if type(price) != type(1.0) and type(price) != type(1):
                if type(price) == type('abc') and price.lower().startswith('per'):
                    outl['per'] = 'per'
                    wtr.writerow(outl)
                elif price == '-' or price == '':
                    pass
                elif outl:
                    outl['per'] = None
                    if outl['publisher'] != '':
                        wtr.writerow(outl)
                if r['Publisher'].strip().startswith('-'):
                    values = [temp + ' ' + r['Publisher'], price, low, high]
                    outl = dict(zip(fieldnames[:-1], values))
                else:
                    values = [r['Publisher'], price, low, high]
                    outl = dict(zip(fieldnames[:-1], values))
                    temp = r['Publisher']
        else:
            outl['per'] = None
            wtr.writerow(outl)
