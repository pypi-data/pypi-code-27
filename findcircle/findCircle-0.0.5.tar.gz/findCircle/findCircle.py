from operator import itemgetter
import matplotlib.pyplot as plt
from numpy import linspace
import json
import timeit
from math import *
from random import random

#Defines an object with:
# - x position
# - y position
# - r radius
class Circle:
    #Constructor
    def __init__(self,x,y,r):
        self.x=x
        self.y=y
        self.r=r

    #This is called when a circle is printed
    def __str__(self):
        return "(%.03f,%.03f,%.03f)"%(self.x,self.y,self.r)

#Input x,y min & max
#Randomly picks a position within range
#Outputs array of three vertex points to a right trangle
#The triangle oriented with the  90deg corner in the  bottom right corner
def getTriangle(xmin=0,xmax=10,ymin=0,ymax=10):
    x1=random()*(xmax-xmin)+xmin
    x2=random()*(xmax-xmin)+xmin
    y1=random()*(ymax-ymin)+ymin
    y2=random()*(ymax-ymin)+ymin
    plt.plot([x1,x2,x2],[y1,y1,y2])
    return [(x1,y1),(x2,y1),(x2,y2)]

#Input the min & max radius desired
#Randomly picks radius in range
#Positions picked by getTriangle function
#Returns three Circle objects
def getCircles(rmin=4, rmax=5):
    circs=[]
    tri=getTriangle()
    circles=[ Circle(triangle[0],triangle[1],random()*(rmax-rmin)+rmin) for triangle in tri ]
    return circles
        
#Input position and radius of two circles
#Assumes the circles share the y-coordinates
#y0 is the distance from the y-axis
#Returns an array of intersecting points
def getTwoCircleIntercepts(C,K):
    point=None
    radius=None
    offset=0
    if   C.y==K.y:
        if C.x<K.x:
            point=(C.x,K.x)
            radius=(C.r,K.r)
        else:
            point=(K.x,C.x)
            radius=(K.r,C.r)
        offset=C.y
    elif C.x==K.x:
        if C.y<K.y:
            point=(C.y,K.y)
            radius=(C.r,K.r)
        else:
            point=(K.y,C.y)
            radius=(K.r,C.r)
        offset=K.x
    else:
        return transform(C,K)
    #point[0] < point[1]
    overlap=(point[0]+radius[0])-(point[1]-radius[1])
    if  overlap < 0:
        #No intersection
        return [] 
    elif radius[0]+radius[1] == overlap:
        #Touching circles
        return [(point[0]+radius[0], offset+0)] 
    else:
        #Overlapping circles
        d=point[1]-point[0]
        x=(d**2-radius[1]**2+radius[0]**2)/(2*d)
        ysquared=(4*d**2*radius[0]**2-(d**2-radius[1]**2+radius[0]**2)**2)/(4*d**2)
#        print("ys %s"%ysquared)
        y=sqrt(ysquared)
        if   C.y==K.y:
            return [(point[0]+x,offset+y),(point[0]+x,offset-y)]
        elif C.x==K.x:
            return [(offset+y,point[0]+x),(offset-y,point[0]+x)]

def diff(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return qx, qy

#For the case that they are diagonal circles.        
def transform(C,K):
    d=diff((C.x,C.y),(K.x,K.y))
    if K.r < C.r:
        points=getTwoCircleIntercepts(Circle(0,0,K.r),Circle(d,0,C.r))
    else:
        points=getTwoCircleIntercepts(Circle(0,0,C.r),Circle(d,0,K.r))
    
    theta=atan((K.y-C.y)/(K.x-C.x))
    #Rotate then transform
    #because C was at the origin, add to C.
    #Rotate
    points=[ rotate((0,0),p,theta) for p in points ]
    #transform
    if K.r < C.r:
        points=[ (p[0]+K.x,p[1]+K.y) for p in points ]
    else:
        points=[ (p[0]+C.x,p[1]+C.y) for p in points ]
    
#    print("K.r %.04f\nC.r %.04f"%(K.r,C.r))
#    print(points,_points)
    return points
#Input an array of Circle objects
#Retuns an ordered list of intersecting points
def getIntercepts(circles):
    intersections=[]
    #Inefficient way of looping but I can't figure out how to optimize.
    for circle in circles:
        for kircle in circles:
            if circle is kircle: continue
            intersections+=getTwoCircleIntercepts(circle,kircle)
    return intersections

def getTripleIntercept(inputs):
    for i in inputs:
        if inputs.count(i) == 4:
            print(i)
            return i
    return None

def getMaxIntercept(inputs):
    lastElement=None
    lastValue=0
    for i in inputs:
        if inputs.count(i) > lastValue:
            lastElement=i
            lastValue=inputs.count(i)
    return lastElement

#Run a brief implementation of the above functions
fig,ax=plt.subplots()
def runTest():
    circles=getCircles()
    
    #for c in circles: print(c)
    inters=getIntercepts(circles)
    triple=getTripleIntercept(inters)
    print("The triple intercept is (%.04f,%.04f)"%(triple[0],triple[1]))
    colors=['r','y','b']
    circs=[plt.Circle((c.x,c.y), c.r,alpha=.3,color=color) for c,color in zip(circles,colors)]
    ax.set_xlim((-10,20))
    ax.set_ylim((-10,20))
    for c in circs:
        ax.add_artist(c)
    x=[p[0] for p in inters]
    y=[p[1] for p in inters]
    plt.plot(x,y, linestyle="None", marker=".")
    plt.show()


def plotIntercept(circles=None):
    if circles is None: circles=[Circle(0,0,4),Circle(8,0,4),Circle(4,4,4)]
    inters=getIntercepts(circles)
    triple=getTripleIntercept(inters)
    print("The triple intercept is (%.04f,%.04f)"%(triple[0],triple[1]))
    colors=['r','y','b']
    circs=[plt.Circle((c.x,c.y), c.r,alpha=.3,color=color) for c,color in zip(circles,colors)]
    ax.set_xlim((-10,20))
    ax.set_ylim((-10,20))
    for c in circs:
        ax.add_artist(c)
    x=[p[0] for p in inters]
    y=[p[1] for p in inters]
    plt.plot(x,y, linestyle="None", marker=".")
    plt.show()
    
def findIntercept(circles):
    inters=getIntercepts(circles)
    return getTripleIntercept(inters)

