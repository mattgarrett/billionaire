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

#TODO: check for data file and leaderboard file
#TODO: unhardcode the file name
stockData = csv.reader(open("data/nasdaq.csv", "r"))

#initial value of stock, initial value of capital
stock = 10000
cash = 10000

#just leave this at zero, because it won't
#as rules for a decision until there is some history
order = 0

for row in stockData:
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
    if len(leaderboard) == 11:
        os.remove("data/leaderboard/" + leaderboard[10][2])
        call(["git", "rm", "-fq", "data/leaderboard/" + leaderboard[10][2]])
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
