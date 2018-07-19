from platypus import *

problem = WFG1(2)
algorithm = NSGAIII(problem, divisions_outer=12,variator = SBX(probability = 1.0, distribution_index = 30.0))
algorithm.run(1000)