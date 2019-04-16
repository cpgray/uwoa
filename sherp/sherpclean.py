import csv

with open('sherp.csv') as sherp:
    rdr = csv.DictReader(sherp)
    with open('costs.csv', 'wt', newline='') as costs:
        wtr = csv.writer(costs)
        for r in rdr:
            if r['US Dollars'].startswith('('):
                price = r['US Dollars'][1:-1]
            else:
                price = r['US Dollars']
            if '-' in price and price != '-':
                price = price.split('-')
                price = (int(price[0][1:]) + int(price[1][1:]))/2
            elif price.startswith('$'):
                price = price[1:]
            if type(price) == type(1.0) or price.isdigit():
                if r['Publisher'].strip().startswith('-'):
                    wtr.writerow([temp + ' ' + r['Publisher'], price])
                else:
                    wtr.writerow([r['Publisher'], price])
                    temp = r['Publisher']
            else:
                print('error', r)
