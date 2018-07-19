
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
'''
| Notes on Radiation Thickness

From arXiv:1603.09669v2,
the plates are:
 5.5e-3cm Silicon; radlen 9.37cm
 5.0e-3cm Kapton;  radlen 28.6cm
Plates are .0055/9.37 + 0.0050/28.6 = 7.6x10^-4 radlen
'''

def getScatterRMS(thickness,velocity=BE):
    v=velocity
    out=(13.6)/(v) * sqrt(thickness) * (1+.088*log(thickness))
    return out

def getScatterAngle(thickness, use=True):
    if use is False: return 0
    rms=getScatterRMS(thickness)
    theta=normal(0,rms)
    return theta
    
def getPosition(positions,plates, use=True):
    track=[]
    theta=0
    previous_x=0
    y=0
    for x,plate in zip(positions,plates):
        d=x-previous_x
        y+=d*tan(theta)
        track.append(y)
        theta+=getScatterAngle(plate['radlen'], use)
        previous_x=x
    return track

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
        if plt is not None and e%int(events/100) is 0:
            _plt=plt
        else:
            _plt=None
        vals.append(getTestPoint(sensor,positions[toggle[0]:toggle[1]],measured_tracks[start:end][toggle[0]:toggle[1]],plt=_plt))
        risiduals.append(getRisidual(positions[toggle[0]:toggle[1]],measured_tracks[start:end][toggle[0]:toggle[1]]))
    x=[]
    for i in range(events): x+=positions.copy()
    
    return vals, x, real_tracks, measured_tracks, risiduals

def simulate(events, sensor=470, config="plates.json", res=.0051826, plt=None, toggle=None, title=None, use=True):
    plates=loadPlateFile(config)
    vals, x, real_tracks, measured_tracks, risiduals = getSimulationData( plates, events, sensor, res=res, toggle=toggle, use=use, plt=plt)
    return getRMS(vals)

    

