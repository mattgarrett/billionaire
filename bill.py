#!/usr/bin/python3

#bill.py
#matt and peter, becoming billionaires

#first arg is the python rule file for playing the stock market game
#second (optional) argument is the number of days to simulate

import csv
import os
import sys

from shutil import copyfile
from random import choice
from subprocess import call

if len(sys.argv) < 2:
    print ('must provide a python at least one file name')
    print ('as the first argument this file will be treated')
    print ('as the rules file')
    sys.exit(0)

rules = []
names = []

for i in range(1, len(sys.argv)):
    try:
        rules.append(__import__((sys.argv[i])[0:-3]))
        names.append(sys.argv[i])
    except ImportError:
        print ('couldn\'t import the rules file:')
        print (sys.argv[i])
        sys.exit(0)

#max number of days the trial will run
#-1 signals no max
limit = -1

count = 0
history = []

#TODO: check for data file and leaderboard file
#TODO: unhardcode the file name
stockData = csv.reader(open("data/nasdaq.csv", "r"))

#initial value of stock, initial value of capital
stock = [10000] * len(rules)
cash = [10000] * len(rules)

#just leave this at zero, because it won't
#as rules for a decision until there is some history
order = 0

def pad(string):
    while len(string) < 10:
        string = string + " "
    string = string[:10] + "  "
    return string

header = pad('                 ')
for name in names:
    header = header + pad(name)
print (header)
header = pad('                 ')
for name in names:
    header = header + pad('+++++++++++++++++++')
print (header)

line = ''
for row in stockData:
    if count == limit:
        break
    history.append(float(row[4]))

    today = len(history) - 1
    line = pad('Day: ' + str(today))

    for i in range(0, len(rules)):
        old = stock[i] + cash[i]

        #the change in the market
        change = ((history[today] - history[today - 1]) / history[today - 1])
        stock[i] = stock[i] + (stock[i] * change)
        
        """
        if ((cash[i] + stock[i]) >= old):
            print ('day ' + str(count) + ': ' + str(stock + cash) + ', +' + str(stock + cash - old))
        else:
            print ('day ' + str(count) + ': ' + str(stock + cash) + ', ' + str(stock + cash - old))
        """

        order = rules[i].main(history, stock[i], cash[i])
        if (order < 0 and 0 - order > stock[i]):
            print ('')
            print (names[i] + ':')
            print ('can\'t sell more stock than you have')
            print ('sell order: ' + str(order) + ' in stock')
            print ('you have  : ' + str(stock[i]) + ' in stock')
            sys.exit(1)
        if (order > 0 and order > cash[i]):
            print ('')
            print (names[i] + ':')
            print ('can\'t spend more money than you have')
            print ('buy order : ' + str(order) + ' in cash')
            print ('you have  : ' + str(cash[i])  + ' in cash')
            sys.exit(1)
        
        stock[i] = stock[i] + order
        cash[i] = cash[i] - order
        line = line + pad(str(stock[i] + cash[i]))

    count = count + 1
    print (line, end="\r")
print (line)

"""
leaderboard = []
leaderboardNames = []
words = []

#reads in the leaderboard for comparing results
leaderboardData = csv.reader(open("data/leaderboard/leaderboard.csv", "r"))
for row in leaderboardData:
    leaderboard.append((int(row[0]), row[1], row[2]))
    leaderboardNames.append(row[2][0:-3])

#reads in words for leaderboard names
wordsData = csv.reader(open("data/leaderboard/words.csv", "r"))
for row in wordsData:
    words.append(row[0])

words = list(filter(lambda word: word not in leaderboardNames, words))

name = choice(words)
leaderboard.append((round(stock + cash), sys.argv[1], name + ".py"))
leaderboard = sorted(leaderboard, reverse=True)

print ("\nLeaderboard:")
for item in leaderboard:
    print ("   " + str(item))

if len(leaderboard) < 11 or leaderboard[10][2] != name + ".py":
    copyfile(sys.argv[1], "data/leaderboard/" + name + ".py")
    call(["git", "add", "data/leaderboard/" + name + ".py"])
    print ("\nYou made it on the leaderboard as " + name + ".py!")
    print ("Saved your file at data/leaderboard/" + name + ".py")
    
    os.remove("data/leaderboard/leaderboard.csv")
    with open("data/leaderboard/leaderboard.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(0, min(len(leaderboard), 10)):
            writer.writerow(leaderboard[i])
    call(["git", "add", "data/leaderboard/leaderboard.csv"])
else:
    print ("You didn't make it on the leaderboard")
    print ("You must be pretty bad")
"""
