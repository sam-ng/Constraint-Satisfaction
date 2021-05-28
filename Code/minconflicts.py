# Samuel Ng 112330868
# CSE 352 Assignment 2

# Python standard library
import sys
import random
from operator import itemgetter
import time
from statistics import mean, stdev

# Global variables
steps = 0

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

# MIN-CONFLICT FUNCTIONS

# helper function for generating random initial assignment
def initial_assignment(matrix, K):
	assignment = []
	for i in range(len(matrix)):
		assignment.append(random.randrange(K))
	return assignment

# helper function to check if assignment is consistent
def consistent(assignment, matrix):
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if matrix[i][j] == 1 and assignment[i] == assignment[j]: # if there is a constraint between the two variables, they can't be the same color
				return False
	return True

# chooses the variable to fix with most constraining heuristic
def max_conflicts_variable(assignment, matrix):
	conflicted = [] # will hold a tuple with (conflicted var, conflict count)
	for i in range(len(matrix)):
		conflict_count = 0
		for j in range(len(matrix[i])):
			if matrix[i][j] == 1 and assignment[i] == assignment[j]:
				conflict_count += 1
		conflicted.append((i, conflict_count))
	if len(conflicted) > 0:
		var = max(conflicted, key=itemgetter(1))[0] # get the variable with the most conflicts
		return var
	return -1

# chooses the value to assign with least constraining heuristic
def min_conflicts_value(assignment, matrix, var, K):
	domain = [i for i in range(K)]
	conflict_list = [] # will hold a tuple with (value, conflict count)
	for value in domain:
		conflict_count = 0
		for j in range(len(matrix[var])): # for each potential value, check all of var's neighbors for any violated constraints 
			if matrix[var][j] == 1 and assignment[j] == value:
				conflict_count += 1
		conflict_list.append((value, conflict_count))
	return min(conflict_list, key=itemgetter(1))[0] # return the value with the least conflicts

# min_conflicts algorithm, takes in CSP matrix and K, the number of values per variable, and an explored list
# pages.cs.wisc.edu was referenced for this algorithm
def min_conflicts(matrix, K, explored):
	assignment = initial_assignment(matrix, K)
	explored.append(assignment)
	while not consistent(assignment, matrix):
		global steps
		steps += 1
		var = max_conflicts_variable(assignment, matrix)
		value = min_conflicts_value(assignment, matrix, var, K)
		if assignment[var] == value: # nothing changed! time to restart
			print(f'Restart at step {steps}!')
			unique = False
			while not unique: # randomize state until unique state found
				assignment = initial_assignment(matrix, K)
				unique = assignment not in explored
			continue
		assignment[var] = value
	return assignment

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

def run_search_20(matrix, K):
	global steps
	steps_list = []
	times = []
	for i in range(20):
		steps = 0
		time_start = time.time()
		result = min_conflicts(matrix, K, [])
		time_end = time.time()
		print(f'Steps: {steps}')
		steps_list.append(steps)
		print(f"Time: {(time_end - time_start) * 1000} ms")
		times.append((time_end - time_start) * 1000)

	print('Steps')
	print(f'Mean: {mean(steps_list)}')
	print(f'Standard deviation: {stdev(steps_list)}')
	print('Time')
	print(f'Mean: {mean(times)}')
	print(f'Standard deviation: {stdev(times)}')

# main function for running the script
def main():
	inputPath = sys.argv[1]
	outputPath = sys.argv[2]

	inf = open(inputPath, 'r')

	input_lines = inf.read().splitlines()
	first_line = input_lines[0].split()
	N = int(first_line[0]) # N is the number of variables
	M = int(first_line[1]) # M is the number of constraints
	K = int(first_line[2]) # K is the number of colors per variable
	matrix = convert_input_to_matrix(input_lines[1:], N) # matrix represents the CSP instance, where the vertices are the variables and the edges are the constraints
	
	time_start = time.time()
	result = min_conflicts(matrix, K, [])
	time_end = time.time()
	print(f'Steps: {steps}')
	print(f"Time: {(time_end - time_start) * 1000} ms")
	print(result)
	output(result, outputPath)
	#run_search_20(matrix, K)
	inf.close()

if __name__ == '__main__':
	main()
