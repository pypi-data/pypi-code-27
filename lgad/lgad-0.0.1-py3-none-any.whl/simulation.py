
import numpy as np
from numpy import linspace
from numpy.polynomial.polynomial import polyfit
from numpy.random import normal
from math import *
from random import random
from utility import *
import sys, resource, json
#7.6*10**-4
THCK=THICKNESS=.00076
BE=BEAMENERGY=12500 #12.5GeV

def cmToRad(input):
    return input/9.370 #Silicon had rad length of 9.37cm

def getScatterRMS(thickness=THCK,velocity=BE):
    v=velocity
    thickness=cmToRad(thickness)
    out=(13.6)/(v) * sqrt(thickness) * (1+.088*log(thickness))
    return out

def getScatterAngle(thickness, use=True):
    if use is False: return 0
    rms=getScatterRMS()
    theta=normal(0,rms)
    return theta
    
def getPosition(positions,plates, use=True):
    out=[]
    theta=0
    last_x=0
    last_y=0
    for x,plate in zip(positions,plates):
        dx=x-last_x
        dy=dx*tan(theta)
        last_y+=dy
        out.append(last_y)
        theta=getScatterAngle(plate['thickness'], use)
        last_x=x
    #return [0 for i in plates]
    return out

def getMeasurement(real_track, plates, res=None):
    if res is None:
        return [ normal(y,plate['resolution']) for y,plate in zip(real_track, plates) ]
    else:
        return [ normal(y,res) for y in real_track ] 


def getSimulationData(plates, events=1, sensor=470, plt=None, res=None, toggle=None, use=True):
    if toggle is None: toggle=(0,len(plates))
    positions=[ plate['position'] for plate in plates ]
    real_tracks=[]
    measured_tracks=[]
    vals=[]
    risiduals=[]
    for e in range(events):
        start=e*len(plates)
        end=e*len(plates)+len(plates)
        real_tracks+=getPosition(positions, plates, use) # Start with a straight line
        measured_tracks+=getMeasurement(real_tracks[start:end],plates,res)
        vals.append(getTestPoint(sensor,positions[toggle[0]:toggle[1]],measured_tracks[start:end][toggle[0]:toggle[1]]))
        risiduals.append(getRisidual(positions[toggle[0]:toggle[1]],measured_tracks[start:end][toggle[0]:toggle[1]]))
    x=[]
    for i in range(events): x+=positions.copy()
    
    return vals, x, real_tracks, measured_tracks, risiduals


def simulate(events, sensor=470, config="plates.json", res=.0051826, plt=None, toggle=None, title=None, use=True):
    plates=loadPlateFile(config)
    vals, positions, real_track, measured_track, risiduals = getSimulationData( plates, events, sensor, res=res, toggle=toggle, use=use)
    
    if plt is not None:
        plt.subplot(221)
        plt.plot(positions, real_track, marker='.', linestyle='None')
        plt.plot([sensor,sensor], [min(measured_track),max(measured_track)], 'r')
        plt.title("Real Track")
        plt.ylabel("Hit Location (mm)")

        plt.subplot(222)
        plt.plot(positions, measured_track,marker='.', linestyle='None')
        plt.plot([sensor,sensor], [min(measured_track),max(measured_track)], 'r')
        plt.title("Measured Track")
        plt.xlabel("Plate Positions (mm)")

        plt.subplot(223)
        plt.hist(vals,linspace(min(vals),max(vals),300))
        plt.xlabel("Veritle Axis, Hit Location (mm)")
        plt.ylabel("Number of Hits (count)")
        #plt.title("Hits Line of Best Fit at x=%s"%sensor)

        plt.subplot(224)
        plt.axis("off")
        plt.annotate(xy=(.3,.8),s="%s Events"%events)
        plt.annotate(xy=(.3,.7),s="Sensor is at %smm"%sensor)
        plt.annotate(xy=(.3,.6),s="Resolution is %s"%res)
        if title is not None: plt.annotate(xy=(.3,.5),s=title)
        
        plt.show()

    return getRMS(vals)
