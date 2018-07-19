import os
import json
import subprocess
from platypus import NSGAII, Problem, Real

nvars = 11
nobjs = 2

def call_external(vars):
    with open("input.txt", "w") as f:
        json.dump(vars, f)
        
    subprocess.call(["python", "dtlz2.py", "input.txt", "output.txt", str(nvars), str(nobjs)])
        
    with open("output.txt", "r") as f:
        objs = json.load(f)
        
    return objs

problem = Problem(nvars, nobjs)
problem.types[:] = Real(0, 1)
problem.function = call_external

algorithm = NSGAII(problem)
algorithm.run(10000)

for solution in algorithm.result:
    print(solution.objectives)