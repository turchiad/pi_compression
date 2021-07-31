# by Daniel Turchiano 2021-07-30 6:24 p.m.

import math
import sys

class pi_pair:
	def __init__(self, num):
		# Check for invalid inputs
		try:
			x = int(num)
			if x < 0:
				print("pi_pair failed: negative number")
				sys.exit()
		except:
			print("pi_pair failed: not an int")
			sys.exit()
		# Assign values
		self.num = str(num)

	def __str__(self):
		return self.num

	def digits(self):
		return len(self.num)

# num_digits > 0
def gen_pi_pairs(num_digits):
	if num_digits <= 0:
		# Invalid inputs
		print("gen_pi_pairs() failed: num_digits must be a positive int")
		sys.exit()
	elif num_digits == 1:
		# Base condition
		return [pi_pair(str(x)) for x in range(10)]
	else:
		# Append 0-9 to each member of last call and add to new_list
		new_list = []
		for i in [str(x) for x in gen_pi_pairs(num_digits-1)]:
			for j in range(10):
				new_list.append(i + str(j))
		# Convert to pi_pairs
		return [pi_pair(x) for x in new_list]

# returns the index of init_value recursively searched `depth` times in `pi_digits`
def recur_index(pi_digits, init_value, depth):
	n = init_value
	for i in range(depth):
		try:
			n = str(pi_digits.index(n))
		except:
			print("recur_index() failed:",n,"not found in pi")
			sys.exit()
	return pi_pair(n) 

# Open Pi Digits
f = open("pi1B_decimals.txt")
pi_digits = f.read()

# Order of magnitude of the values ('1' -> 0,1,2...; '2' -> 00,01,02... etc.)
oom = int(sys.argv[1])
# Depth of the digit searching
depth = int(sys.argv[2])

# Generate inputs/outputs
inputs = gen_pi_pairs(oom)
outputs = [recur_index(pi_digits, str(x), depth) for x in inputs]

# Construct results
results = []
for i in range(len(inputs)):
	if inputs[i].digits() < outputs[i].digits():
		results.append(f'{inputs[i]}\t{outputs[i]}\t+')
	elif inputs[i].digits() > outputs[i].digits():
		results.append(f'{inputs[i]}\t{outputs[i]}\t-')
	else:
		results.append(f'{inputs[i]}\t{outputs[i]}\t0')

# Print results
print("INPUT\tOUTPUT\tTREND")
for row in results:
	print(row)