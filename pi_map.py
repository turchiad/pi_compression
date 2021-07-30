# by Daniel Turchiano 2021-07-30 3:21 p.m.

import math
import sys

def digits(i):
	if i == 0:
		return 1
	elif i > 0:
		return (int)(math.log10(i)) + 1

# Open Pi Digits
dic = open("pi1B_decimals.txt")
data = dic.read()

# Read input
depth = int(sys.argv[1])

for i in range(10,100):
	search_value = i
	search_result = i
	for j in range(depth):
		search_result = data.index(str(search_result))
	direction = digits(search_value) - digits(search_result)
	if direction > 0:
		print(i,"-1",sep=',')
	elif direction == 0:
		print(i," 0",sep=',')
	else:
		print(i,"+1",sep=',')
