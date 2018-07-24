import numpy as np
from numpy import linspace
from numpy.polynomial.polynomial import polyfit
from numpy.random import normal
from math import *
from random import random
from utility import *
import sys, resource, json
from simulation import *
import matplotlib.pyplot as plt

def sim(events, sensor=470, config="plates.json", res=.0051826, plt=None, toggle=None, title=None, use=True):
    plates=loadPlateFile(config)
    vals, positions, real_track, measured_track, risiduals = getSimulationData( plates, events, sensor, res=res, toggle=toggle, use=use)
    
#    rms=getRMS(risiduals)
    a = abs(sensor-plates[2]['position'])
    d = abs(plates[2]['position']-plates[1]['position'])
    r=a/d
    s = res
    S=s*sqrt(1+2*r*r)

    print("The given resolution is %.06f and the calculated S=%.06f"%(s,S))
    print("The scoring plane location is %s and plate 3 is at %s"%(sensor, plates[2]['position']))
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
        plt.annotate(xy=(0,.8),s="%s Events"%events)
        plt.annotate(xy=(0,.7),s="Sensor is at %smm"%sensor)
        plt.annotate(xy=(0,.6),s="Resolution is %s"%res)
        plt.annotate(xy=(0,.5),s="Calculated rms at sensor is %.07f"%S)
        plt.annotate(xy=(0,.4),s="Plate 3 is located at %.07fmm"%plates[2]['position'])
        if title is not None: plt.annotate(xy=(.3,.5),s=title)
        
        plt.show()
    return S
plate_min=285
plate_max=750
test_range=linspace(plate_min,plate_max,20)
res=[]
events=50000
for test in test_range:
    res.append(sim(events, sensor=test))

plt.title("Scoring Plane Position vs RMS at the Scoring Plane %s events"%events)
plt.plot(test_range,res,linestyle='None', marker='o')
plt.xlabel("Scoring Plane Position (mm)")
plt.ylabel("RMS at the Scoring Plane (S)")
plt.show()
    
