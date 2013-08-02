#/usr/bin/python

#bill.py
#
#matt and peter, becoming billionaires

import csv
import sys
import rules.py

#max number of days the trial will run
#0 signals no max
limit = -1
if len(sys.argv) > 1:
    try:
        limit = int(sys.argv[1])
    except:
        print 'command line argument must be an int'
        sys.exit(0)

count = 0
history = []
cr = csv.reader(open("nasdaq.csv", "r"))

for row in cr:
    if count == limit:
        break
    history.append(row[4])
    rules(history)
    count = count + 1
