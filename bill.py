#/usr/bin/python

#bill.py
#
#matt and peter, becoming billionaires

import csv
import sys

if len(sys.argv) == 1:
    print 'must provide a python file name as the first argument'
    print 'this file will be treated as the rules file'
    sys.exit(0)

try:
    print (sys.argv[1])
    rules = __import__((sys.argv[1])[0:-3])
except:
    print 'couldn\'t import the rules file: '
    print sys.argv[1]
    sys.exit(0)

#max number of days the trial will run
#0 signals no max
limit = -1
if len(sys.argv) > 2:
    try:
        limit = int(sys.argv[2])
    except:
        print 'second command line argument must be an int'
        sys.exit(0)

count = 0
history = []
cr = csv.reader(open("nasdaq.csv", "r"))

for row in cr:
    if count == limit:
        break
    history.append(row[4])
    rules.main(history)
    count = count + 1
