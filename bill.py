#!/usr/bin/python3

#bill.py
#matt and peter, becoming billionaires

#first arg is the python rule file for playing the stock market game
#second (optional) argument is the number of days to simulate

import csv
import sys

if len(sys.argv) == 1:
    print ('must provide a python file name as the first argument')
    print ('this file will be treated as the rules file')
    sys.exit(0)

try:
    rule = __import__((sys.argv[1])[0:-3])
except ImportError:
    print ('couldn\'t import the rules file:')
    print (sys.argv[1])
    sys.exit(0)

#max number of days the trial will run
#-1 signals no max
limit = -1
if len(sys.argv) > 2:
    try:
        limit = int(sys.argv[2])
    except:
        print ('second command line argument must be an int')
        sys.exit(0)

count = 0
history = []
#TODO: unhardcode the file name
cr = csv.reader(open("data/nasdaq.csv", "r"))

#initial value of stock, initial value of capital
stock = 10000
cash = 10000

#just leave this at zero, because it won't
#as rules for a decision until there is some history
order = 0

for row in cr:
    if count == limit:
        break
    history.append(float(row[4]))
    if len(history) > 10:
        today = len(history) - 1

        old = stock + cash

        #the change in the market
        change = ((history[today] - history[today - 1]) / history[today - 1])
        stock = stock + (stock * change)
        
        if ((cash + stock) >= old):
            print ('day ' + str(count) + ': ' + str(stock + cash) + ', +' + str(stock + cash - old))
        else:
            print ('day ' + str(count) + ': ' + str(stock + cash) + ', ' + str(stock + cash - old))

        order = rule.main(history, stock, cash)
        if (order < 0 and 0 - order > stock):
            print ('can\'t sell more stock than you have')
            print ('sell order: ' + str(order) + ' in stock')
            print ('you have  : ' + str(stock) + ' in stock')
            sys.exit(1)
        if (order > 0 and order > cash):
            print ('can\'t spend more money than you have')
            print ('buy order : ' + str(order) + ' in cash')
            print ('you have  : ' + str(cash)  + ' in cash')
            sys.exit(1)

        stock = stock + order
        cash = cash - order
    count = count + 1
