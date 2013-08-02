#!/usr/bin/python3

#generates a bull market csv

import csv
import random

cw = csv.writer(open("bull.csv", "w"))

delta = 10

for x in range(30, 10000):
    val = random.uniform(x - delta, x + delta)
    cw.writerow(['bull', x, x, x, val, 0, val])
