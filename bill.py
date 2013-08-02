#/usr/bin/python

#bill.py
#
#matt and peter, becoming billionaires

import csv

cr = csv.reader(open("nasdaq.csv", "r"))
for row in cr:
    print row
