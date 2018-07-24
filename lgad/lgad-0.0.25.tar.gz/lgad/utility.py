from numpy.polynomial.polynomial import polyfit
import json
from math import *
from operator import itemgetter, attrgetter

def cmToRad(input):
    return input/9.370 #Silicon had rad length of 9.37cm

def transform_to_origin(input):
    minimum=min(input)
    return [i-minimum for i in input]

def loadPlateFile(url):
    with open("plates.json") as f:
        plates=json.loads(f.read())
    return plates

def plotLine(plotter, inputs, outputs):
    b,m=polyfit(inputs,outputs, 1)
    plotter.plot(inputs,[m*x+b for x in inputs])
    return b,m

def getTestPoint(x,y,test_point,toggle,plt=None):
    b,m=polyfit(x[toggle[0]:toggle[1]],y[toggle[0]:toggle[1]],1)
    if plt is not None:
        plt.plot(x,[m*i+b for i in x])
    return m*test_point+b
'''

a= sum 1
b=sum x
c=sumx^2
rms = sqrt((b/a)^2 - c/a)
'''
def getRMS(risiduals):
    a=len(risiduals)
    b=sum(risiduals)
    b=b*b
    c=sum([x*x for x in risiduals])/a
    return sqrt(c - (b/a)**2)

#this is going to get messy, I don't want to have the sensor plate be defined as a plate because it is moving around a lot, so instead it finds a line between the two nearest plates and assumes a straight path between them.
def getRisidual( x, measured_tracks, test_point, toggle, real_tracks ):
    b,m=polyfit(x[toggle[0]:toggle[1]],measured_tracks[toggle[0]:toggle[1]], 1)
    x.append(test_point)
    real_tracks.append(None)
    points=sorted(zip(x,real_tracks),key=itemgetter(0))
    real_y=0
    for i,p in enumerate(points):
        if p[0] is test_point and p[1] is None:
            dy=(points[i-1][1]-points[i+1][1])
            dx=(points[i-1][0]-points[i+1][0])
            slope=dy/dx
            real_y=slope*(test_point-points[i-1][0]) + points[i-1][1]
    pred_y=m*test_point+b
    return real_y-pred_y

# Plotting for json formatted like:
# [ [x_0,y_0],[x_1,y_1],...,[x_n,y_n] ]
def generalPloting(file_name, title, xlabel,ylabel,plt):
    data=None
    with open(file_name) as f:
        data=json.loads(f.read())
    x=[datum[0] for datum in data]
    y=[datum[1] for datum in data]
    plt.plot(x,y, linestyle="None", marker="o")
    b,m=plotLine(plt,x,y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def getComposition(materials):
    #materials should be an array with 2-tuples, (material, thickness)
    radlen=0
    for material in materials:
        radlen+=getRadlen(material[0],material[1])
    return radlen
    
KAPTON=28.6  #cm
SILICON=9.37 #cm
def getRadlen(thickness, material):
    material=material.lower()
    if material == "kapton":
        return thickness/KAPTON
    elif material == "silicon":
        return thickness/SILICON
    else:
        return None
