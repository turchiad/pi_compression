# by Daniel Turchiano 2021-07-30 6:24 p.m.

# Imports for Error Printing
from __future__ import print_function

# Standard imports
import math
import sys
import time;
from collections.abc import Iterable


# External imports
import networkx as nx
from pyvis.network import Network

# Matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt

# Error Printing
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

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

# Flattens a list. From Cristian @ StackOverflow
# Returns a generator for the list
def flatten(l):
	for el in l:
		if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
			yield from flatten(el)
		else:
			yield el

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

# Find pi reduction
## Given a string `s` and Graph `G`
## depth/breadth first search `s` in `G` (`successors`)
### destructure `successors` with `[y for x,y in suc.items()]
### flatten the result with `flatten()`
### find the minimum of the result of `flatten` with `min([x for x in result], key=len) (`successor_min`)
## check if `len(successor_min)` is less than `len(s)`
### if not, no pi reduction is possible
### if so, shortest path from `s` to `successor_min` (len_path)
#### `len_path-1` is the number of times the number must be pi indexed to minimally reduce it.
def find_pi_reduction(G, s):
	successors = nx.dfs_successors(G,s)
	successor_tails = [z for z in flatten([y for x,y in successors.items()])]
	successors_min = min(successor_tails, key=len) if len(successor_tails) > 0 else s # Minimum is s
	if len(successors_min) < len(s):
		len_path = len(nx.shortest_path(G,s,successors_min))
		return (len_path - 1, len(s) - len(successors_min))
	else:
		return (0,0)

# Open Pi Digits
eprint("Reading digits of pi...")
f = open("pi1B_decimals.txt")
pi_digits = f.read()

# Order of magnitude of the values ('1' -> 0,1,2...; '2' -> 00,01,02... etc.)
oom = int(sys.argv[1])
# # Depth of the digit searching
depth = int(sys.argv[2])

# Generate inputs/outputs
eprint("Generating inputs...")
inputs = gen_pi_pairs(oom)

# Giving user loading times
eprint("Generating outputs:")
time_max = len(inputs)
time_interval = 5000
timer = 0

outputs = []
for d in range(depth):
	output = []
	for x in inputs:
		output.append(recur_index(pi_digits, str(x), d+1))
		# Verbose
		timer += 1
		if timer % time_interval == 0:
			time_progress = timer / time_max
			eprint(f'{time_progress:2.2%}')
	outputs.append(output)

# Old method
# outputs = [[recur_index(pi_digits, str(x), d+1) for x in inputs] for d in range(depth)]

# Create directed graph
G = nx.DiGraph()

# Giving user loading times
eprint("Graph construction:")
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
			eprint(f'{time_progress:2.2%}')

# Finding optimal reductions
print("NUM\tRED.#\tRED.AMT")
eprint("Printing:")
time_max = len(G.nodes())
time_interval = 1000
timer = 0

for node in sorted(G.nodes(), key=int):
	(reduction_num, digits_reduced) = find_pi_reduction(G, node)
	print(node, reduction_num, digits_reduced, sep='\t')
	# Verbose
	timer += 1
	if timer % time_interval == 0:
		time_progress = timer / time_max
		eprint(f'{time_progress:2.2%}')




# # Create visualization

# # MatPlotLib
# print("Plotting...")

# nx.draw(G, with_labels=True)
# plt.show()

# print(G)

# # PyVis
# net = Network("700px","1200px",directed=True,notebook=True)
# net.from_nx(G)
# net.show_buttons(filter_=['physics'])
# net.show("Example.html")