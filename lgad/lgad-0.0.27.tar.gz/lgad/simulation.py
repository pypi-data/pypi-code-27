from operator import itemgetter, attrgetter
import numpy as np
from numpy import linspace
from numpy.polynomial.polynomial import polyfit
from numpy.random import normal
from math import *
from random import random
from multiprocessing import Pool as ThreadPool
#from multiprocessing.dummy import Pool as ThreadPool 
from itertools import repeat
import sys, resource, json
import timeit
try:
    from utility import *
except Exception:
    from lgad.utility import *

#7.6*10**-4
'''
Run the simulation with a .1 radiation length for the scoring plane.
'''

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


'''

Set resolution to zero, the RMS should grow by sqrt(2)*rms(plate1);
'''
def getScatterRMS(thickness,velocity=BE):
    if thickness == 0: return 0
    v=velocity
    out=(13.6)/(v) * sqrt(thickness) * (1+.088*log(thickness))
    return out

def getScatterAngle(thickness, use=True):
    if use is False: return 0
    rms=getScatterRMS(thickness)
    theta=normal(0,rms)
    return theta
    
def getPosition(positions,radlens, use=True):
    track=[]
    theta=0
    previous_x=0
    y=0
    for x,radlen in zip(positions,radlens):
        d=x-previous_x
        y+=d*tan(theta)
        track.append(y)
        theta+=getScatterAngle(radlen, use)
        previous_x=x
    return track

def getMeasurement(real_track, resolution):
    return [ normal(y,res) for y,res in zip(real_track,resolution) ] 

def getEvent(positions, radlengths, resolutions, scoringPlane, togglePlates, useCoulomb):
    realTrack   = getPosition ( positions, radlengths, useCoulomb )
    measurement = getMeasurement( realTrack, resolutions)
    score       = getTestPoint( positions, measurement, scoringPlane, togglePlates )
    risidual    = getRisidual ( positions, measurement, scoringPlane, togglePlates , realTrack)
    return realTrack,measurement,score,risidual,positions

def simulate(events=1, sensor=405, sensor_radlen=0.0,config="plates.json", res=.0051826, plt=None, toggle=None, title=None, use=True, threads=8):
    sensor_pos=sensor
    plates=loadPlateFile(config)
    if toggle is None: toggle=(0,len(plates))
    plates.append({'position': sensor_pos, 'radlen': sensor_radlen, 'resolution': plates[0]['resolution']})
    plates=sorted(plates, key=lambda ele: ele['position'])
    positions=[ plate['position'] for plate in plates ]
    radlens=[ plate['radlen'] for plate in plates ]
    res=[ plate['resolution'] for plate in plates ]
    pos=[positions for i in range(events)]
    params=zip(pos,repeat(radlens),repeat(res),repeat(sensor),repeat(toggle),repeat(use))
    with ThreadPool(threads) as pool:
        results=pool.starmap(getEvent,params)
    risiduals = [datum[3] for datum in results]
    if plt is not None:
        plotData(results, sensor, events, res[0])
    return getRMS(risiduals)

def plotData(res, sensor, events, resolution):
    import matplotlib.pyplot as plt
    _positions=[datum[4] for datum in res]
    _real_track=[datum[0] for datum in res]
    _measured_track=[datum[1] for datum in res]
    positions=[]
    real_track=[]
    measured_track=[]
    for i in range(len(_real_track)):
        positions+=_positions[i]
        real_track+=(_real_track[i])
        measured_track+=(_measured_track[i])
    vals=[datum[2] for datum in res]
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
    plt.annotate(xy=(.3,.6),s="Resolution is %s"%resolution)
    plt.show()

