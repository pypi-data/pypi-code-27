import os
import json
import uuid
import subprocess
from platypus import NSGAII, Problem, Real, ProcessPoolEvaluator

nvars = 11
nobjs = 2

def call_external(vars):
    id = str(uuid.uuid4())
    input = "input-%s.txt" % id
    output = "output-%s.txt" % id
    
    with open(input, "w") as f:
        json.dump(vars, f)
        
    subprocess.call(["python", "dtlz2.py", input, output, str(nvars), str(nobjs)])
        
    with open(output, "r") as f:
        objs = json.load(f)
        
    os.remove(input)
    os.remove(output)
        
    return objs

if __name__ == "__main__":
    problem = Problem(nvars, nobjs)
    problem.types[:] = Real(0, 1)
    problem.function = call_external
    
    with ProcessPoolEvaluator(4) as evaluator:
        algorithm = NSGAII(problem, evaluator=evaluator)
        algorithm.run(10000)

    for solution in algorithm.result:
        print(solution.objectives)