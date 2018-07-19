import math
import numpy
from platypus import *

problem = Problem(1,2,1) # Send 1 permutation, return 6 OF, and 1 constraint
problem.types[0] = Permutation(range(10)) # Permutation of elements [0, 1, ..., nvar-1]
problem.constraints[:] = "<=0"

lst = [Solution(problem) for i in range(5)]  #  List of the solutions casted from the Solution class

# Setting objectives and constraints
for i, item in enumerate(lst):
    item.objectives[:] = [0, 1]
    item.constraint_violation = 0
    item.problem = problem

sorted = nondominated(lst)

print(sorted)