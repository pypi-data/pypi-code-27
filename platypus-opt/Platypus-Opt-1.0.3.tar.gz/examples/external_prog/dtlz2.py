import sys
import math
import json
import operator
import functools

if __name__ == "__main__":
    # python dtlz2.py <input-file> <output-file> <nvars> <nobjs>
    input = sys.argv[1]
    output = sys.argv[2]
    nvars = int(sys.argv[3])
    nobjs = int(sys.argv[4])
    
    with open(input, "r") as f:
        vars = json.load(f)
    
    k = nvars - nobjs + 1
    g = sum([math.pow(x - 0.5, 2.0) for x in vars[nvars-k:]])
    objs = [1.0+g]*nobjs
 
    for i in range(nobjs):
        objs[i] *= functools.reduce(operator.mul, [math.cos(0.5 * math.pi * x) for x in vars[:nobjs-i-1]], 1)
             
        if i > 0:
            objs[i] *= math.sin(0.5 * math.pi * vars[nobjs-i-1])
         
    with open(output, "w") as f:
        json.dump(objs, f)
        