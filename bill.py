#/usr/bin/python

#bill.py
#
#matt and peter, becoming billionaires

import csv

#max number of days the trial will run
#0 signals no max
limit = 100

count = 0
history = []
cr = csv.reader(open("nasdaq.csv", "r"))

for row in cr:
    count = count + 1
    if count == limit:
        break
    history.append(row[4])
    print history
