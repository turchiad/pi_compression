# by Daniel Turchiano 2021-07-30 6:24 p.m.

# Standard imports
import math
import sys

# External imports
import networkx as nx
from pyvis.network import Network

# Matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt

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

	def __eq__(self, other):
		return self.num == other.num

	def __hash__(self):
		return hash(self.num)

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

# returns the index of n
# n is a pi_pair
def index(pi_digits, n):
		try:
			return pi_pair(pi_digits.index(str(n)))
		except:
			print("index() failed:",n,"not found in pi")
			sys.exit()

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
print("Reading digits of pi...")
f = open("pi1B_decimals.txt")
pi_digits = f.read()

# Order of magnitude of the values ('1' -> 0,1,2...; '2' -> 00,01,02... etc.)
oom = int(sys.argv[1])
# # Depth of the digit searching
depth = int(sys.argv[2])

# Generate inputs/outputs
print("Generating values...")
for i in range(1,oom):
	inputs = gen_pi_pairs(oom)

outputs = [[recur_index(pi_digits, str(x), d+1) for x in inputs] for d in range(depth)]

# Create directed graph
G = nx.DiGraph()

# Giving user loading times
print("Graph construction:")
time_max = depth * len(inputs)
time_interval = 1000
timer = 0

for i in range(depth):
	for j in range(len(inputs)):
		G.add_nodes_from([str(inputs[j]), str(outputs[i][j])])
		G.add_edge(str(inputs[j]), str(outputs[i][j]))
		# Verbose
		timer += 1
		if timer % time_interval == 0:
			time_progress = timer / time_max
			print(f'{time_progress:2.2%}')


# Create visualization

# MatPlotLib
# print("Plotting...")

# nx.draw(G, with_labels=True)
# plt.show()

# PyVis
# net = Network("700px","1200px",directed=True,notebook=True)
# net.from_nx(G)
# net.show("Example.html")

# print(G)