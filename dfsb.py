# Samuel Ng 112330868
# CSE 352 Assignment 2

# Python standard library
import sys
from queue import PriorityQueue
from operator import itemgetter
import copy
import time
from statistics import mean, stdev

# Global variables
states_explored = 0

# takes the input lines (not including the first line) and N, and returns an adjacency matrix where edges represent the coloring constraints
def convert_input_to_matrix(input_lines, N):
	matrix = [[0 for j in range(N)] for i in range(N)] # NxN matrix
	
	for line in input_lines:
		parsed = line.split()
		i = int(parsed[0])
		j = int(parsed[1])
		matrix[i][j] = 1
		matrix[j][i] = 1
	return matrix

# helper function for visualizing the matrix
def print_matrix(matrix):
	for lst in matrix:
		print(lst)

# DFSB FUNCTIONS

# helper function to check if assignment is consistent, value is the color attempting to be assigned to the current variable
def consistent(assignment, matrix, value):
	var_neighbors = matrix[len(assignment)] # contains the current variable's neighbors
	for j in range(len(assignment)):
		if var_neighbors[j] == 1: # there is an edge from current var to neighbor
			if assignment[j] == value: # value has already been assigned to neighbor j
				return False
	return True

# DFSB++ FUNCTIONS

# lecture notes were referenced for AC-3
# arc consistency algorithm #3, takes in a CSP, and list of domains for each variable, and returns the new CSP, possibly with reduced domains
def ac_3(matrix, domains):
	queue = PriorityQueue()
	add_all_arcs(queue, matrix) # initially adds all arcs in CSP

	while not queue.empty():
		arc = queue.get()
		if remove_inconsistent_values(arc, domains): # if value in domain of i was removed, add all arcs k to i
			add_arcs_k_to_i(queue, matrix, arc[0])

# helper function for initially adding all arcs in CSP into the queue
def add_all_arcs(queue, matrix):
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if matrix[i][j] == 1:
				queue.put((i, j))

# helper function for adding all arc to some variable Xi into the queue
def add_arcs_k_to_i(queue, matrix, i):
	for k in range(len(matrix)):
		if matrix[k][i] == 1:
			queue.put((k, i))

# helper function for removing inconsistent values, takes in an arc and list of domains and returns true on success
def remove_inconsistent_values(arc, domains):
	removed = False
	i = arc[0]
	j = arc[1]
	for x in domains[i]:
		consistentFound = False
		for y in domains[j]: # check all values y in domain of j
			if x != y: # consistent pairing found, no need to remove x
				consistentFound = True
		if not consistentFound:
			domains[i].remove(x)
			removed = True
	return removed

# uses the most constrained variable heuristic to select the next variable to assign
def select_unassigned_variable(assignment, matrix, domains):
	unassigned = [] # contains the unassigned variables
	for i in range(len(assignment)):
		if assignment[i] == -1:
			unassigned.append(i)
	return most_constrained_variable(unassigned, matrix, domains)

# finds the variable that is most constrained
def most_constrained_variable(unassigned, matrix, domains):
	min_var = unassigned[0]
	min_val = len(domains[unassigned[0]])

	for i in unassigned: # check each var in assigned and update min_var and min_val if current var is less constrained than min_var
		if len(domains[i]) < min_val:
			min_var = i
			min_val = len(domains[i])
		"""elif len(domains[i]) == min_val:
			# addition: tie-breaker heuristic -> take the most constraining variable
			i_count = 0
			min_count = 0
			for j in matrix[i]:
				if j in unassigned and matrix[i][j] == 1: # only remaining values count
					i_count += 1
			for k in matrix[min_var]:
				if k in unassigned and matrix[min_var][k] == 1:
					min_count += 1
			if i_count > min_count:
				min_var = i
				min_val = len(domains[i])"""
	return min_var

# uses the least constraining value heuristic to select the value to assign to var
def order_domain_values(assignment, matrix, domains, var):
	unassigned = []
	remaining_count = [] # keeps track of the number of possible values for remaining variables if each value is assigned to var
	for i in range(len(assignment)):
		if assignment[i] == -1 and i != var:
			unassigned.append(i)
	index = 0
	for value1 in domains[var]:
		count = 0
		for var_left in unassigned:
			for value2 in domains[var_left]:
				if matrix[var][var_left] == 1: # possible constrained value
					if value1 != value2:
						count += 1
				else:
					count += 1
		remaining_count.append((index, count)) # (index of value, count of unconstrained values)
		index += 1
	remaining_count = sorted(remaining_count, key=itemgetter(1), reverse=True) # sort the tuples by number of unconstrained values for remaining variables
	new_order = [] # will contain the new domain for domains[var]
	for tuple in remaining_count:
		new_order.append(domains[var][tuple[0]]) # append the var domain value at the new indices
	domains[var] = new_order

# plain DFS-B, takes in the problem matrix and # colors K, and returns a consistent assignment if possible or failure
# lecture notes were referenced for the algorithm
def dfs_b(matrix, K):
	return recursive_backtrack_plain([], matrix, K)

# recursive helper for plain DFS-B, takes in an assignment list, problem matrix, # colors K, and returns a consistent assignment if possible or failure
# assignment is a list that will eventually contain N elements, each variable is assigned colors in order from 0 to N-1
def recursive_backtrack_plain(assignment, matrix, K):
	global states_explored
	states_explored += 1
	if len(assignment) == len(matrix): # all variables have been assigned i.e. goal state
		return (True, assignment)
	for value in range(K): # try assigning each color to current variable
		if consistent(assignment, matrix, value):
			assignment.append(value)
			result = recursive_backtrack_plain(assignment, matrix, K) # result is a tuple containing a boolean denoting success and the assignment if success
			if result[0]:
				return result
			assignment.pop()
	return (False, [])

# improved DFS-B with variable/value ordering and arc consistency
# lecture notes were referenced for the algorithm
def dfs_b_improved(matrix, K):
	assignment = [-1 for x in range(len(matrix))]
	domains = [[x for x in range(K)] for y in range(len(matrix))] # available values for each variable
	return recursive_backtrack_improved(assignment, matrix, domains)

# recursive helper for DFS-B++
def recursive_backtrack_improved(assignment, matrix, domains):
	global states_explored
	states_explored += 1
	if assignment.count(-1) == 0: # all variables have been assigned a value
		return (True, assignment)
	var = select_unassigned_variable(assignment, matrix, domains) # use heuristic to select var to assign
	order_domain_values(assignment, matrix, domains, var) # use heuristic to select value to assign to var
	for value in domains[var]:
		assignment[var] = value
		domains_copy = copy.deepcopy(domains) # deepcopy domains in case need to revert changes for backtracking
		domains[var] = [value]
		ac_3(matrix, domains) # remove any inconsistent values
		result = recursive_backtrack_improved(assignment, matrix, domains)
		if result[0]:
			return result
		assignment[var] = -1 # take back assignment
		for i in range(len(domains)): # recover old domains
			domains[i] = domains_copy[i]
	return (False, [])

# functions for outputting solution to files
def output(solution_list, outputPath):
	outF = open(outputPath, 'w')
	solution_list_str = map(str, solution_list)
	outF.write('\n'.join(solution_list_str))
	outF.close()

def output_error(outputPath):
	outF = open(outputPath, 'w')
	outF.write('No answer')
	outF.close()

# function for running DFSB and DFSB++ 20 times for the report
def run_search_20(matrix, K):
	global states_explored
	states_dfsb = []
	times_dfsb = []
	states_dfsb_pp = []
	times_dfsb_pp = []
	for i in range(20):
		states_explored = 0
		time_start = time.time()
		result = dfs_b(matrix, K)
		time_end = time.time()
		print(f'States explored: {states_explored}')
		states_dfsb.append(states_explored)
		print(f"Time: {(time_end - time_start) * 1000} ms")
		times_dfsb.append((time_end - time_start) * 1000)

		states_explored = 0
		time_start = time.time()
		result = dfs_b_improved(matrix, K)
		time_end = time.time()
		print(f'States explored: {states_explored}')
		states_dfsb_pp.append(states_explored)
		print(f"Time: {(time_end - time_start) * 1000} ms")
		times_dfsb_pp.append((time_end - time_start) * 1000)

	print('DFSB')
	print('States explored')
	print(f'Mean: {mean(states_dfsb)}')
	print(f'Standard deviation: {stdev(states_dfsb)}')
	print('Time')
	print(f'Mean: {mean(times_dfsb)}')
	print(f'Standard deviation: {stdev(times_dfsb)}')
	print('\n\n')
	print('DFSB++')
	print('States explored')
	print(f'Mean: {mean(states_dfsb_pp)}')
	print(f'Standard deviation: {stdev(states_dfsb_pp)}')
	print('Time')
	print(f'Mean: {mean(times_dfsb_pp)}')
	print(f'Standard deviation: {stdev(times_dfsb_pp)}')


# main function for running the script
def main():
	inputPath = sys.argv[1]
	outputPath = sys.argv[2]
	mode = int(sys.argv[3]) # 0 for plain DFS-B, 1 for improved DFS-B

	inf = open(inputPath, 'r')

	input_lines = inf.read().splitlines()
	first_line = input_lines[0].split()
	N = int(first_line[0]) # N is the number of variables
	M = int(first_line[1]) # M is the number of constraints
	K = int(first_line[2]) # K is the number of colors per variable
	matrix = convert_input_to_matrix(input_lines[1:], N) # matrix represents the CSP instance, where the vertices are the variables and the edges are the constraints
	
	time_start = time.time()
	if mode == 0:
		dfsb_result = dfs_b(matrix, K)
	elif mode == 1:
		dfsb_result = dfs_b_improved(matrix, K)
	else:
		print('Invalid mode.')
		return
	time_end = time.time()
	print(f'States explored: {states_explored}')
	print(f"Time: {(time_end - time_start) * 1000} ms")
	if dfsb_result[0]:
		print(f'Solution list: {dfsb_result[1]}')
		output(dfsb_result[1], outputPath)
	else:
		print('No answer.')
	#run_search_20(matrix, K)
	inf.close()

if __name__ == '__main__':
	main()