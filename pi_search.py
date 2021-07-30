# by Daniel Turchiano 2021-07-30 2:54 p.m.

import sys

# Open Pi Digits
dic = open("pi1B_decimals.txt")
data = dic.read()
print(data.index(sys.argv[1]))
		