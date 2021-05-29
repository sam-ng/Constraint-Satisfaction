# Constraint-Satisfaction
<img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white"/>
A solver that applies DFS with backtracking and min-conflicts local search to solve constraint satisfaction problems, such as map coloring. Optimizations were implemented with most constrained variable selection, least constraining value selection, and arc consistency.

## Instructions on Running the Program
CSP .txt files should be formatted as such:\
8	16 3\
0	2\
0	4\
0	6\
0	7\
1	4\
1	6\
1	7\
2	3\
2	6\
2	7\
3	4\
3	5\
3	6\
3	7\
4	6\
5	7

where the first row contains the number of variables, the number of constraints, and the number of 'colors' (domain size of each variable) respectively. The successive rows are space-separated pairs of variables denoting variables containing an edge between them (i.e. the two variables cannot be the same color).

`python dfsb.py <input file> <output file> <mode>` where `<mode>` is 0 for plain DFS with backtracking and 1 for the optimized implementation of DFS with backtracking.
`python minconflicts.py <input file> <output file>` for running the min-conflicts local search.

Python version: 3.8.8
