from findCircle import plotIntercept, runTest, findMaxIntercept, Circle
from numpy.random import normal
import matplotlib.pyplot as plt
def rcirc(x,y,r,std=1):
    return Circle(normal(x,std),normal(y,std),normal(r,std))

last=-1
while last<2:
    circles=[rcirc(0,0,4),rcirc(8,0,4),rcirc(8,8,4),rcirc(0,8,4)]
    intercepts, last = plotIntercept(circles)
    print(last)


