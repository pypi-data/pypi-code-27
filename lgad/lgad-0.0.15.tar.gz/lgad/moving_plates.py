import matplotlib.pyplot as plt
from simulation import simulate
from numpy import linspace
import json

import argparse
parser = argparse.ArgumentParser(description="Utility for running simulation on a moving sensor.")
parser.add_argument('title', metavar="title", type=str, nargs='?', help="Title of the plot")
parser.add_argument('-b', metavar="bins", type=int, nargs='?', help="Number of points to collect.", default=20)
parser.add_argument('-e', metavar="events", type=int, nargs='?', help="Number of events to run.", default=300)
parser.add_argument('--min', metavar="xmin", type=float, nargs='?', help="Minimum x position for sensor.", default=305)
parser.add_argument('--max', metavar="xmax", type=float, nargs='?', help="Maximum x position for sensor.", default=635)
args=parser.parse_args()

plate_min=305
plate_max=635
test_range=linspace(plate_min,plate_max,20)

both_plates=[]
front_plates=[]
select_plates=[]
_both_plates=[]
_front_plates=[]
_select_plates=[]

events=10000
for test in test_range:
    use_coulomb=True
    front_plates.append(simulate(events=events,sensor=test,plt=None,toggle=(0,3), use=use_coulomb))
    select_plates.append(simulate(events=events,sensor=test,plt=None,toggle=(1,3), use=use_coulomb))
    both_plates.append(simulate(events=events,sensor=test,plt=None,toggle=None, use=use_coulomb))
    use_coulomb=False
    _front_plates.append(simulate(events=events,sensor=test,plt=None,toggle=(0,3), use=use_coulomb))
    _select_plates.append(simulate(events=events,sensor=test,plt=None,toggle=(1,3), use=use_coulomb))
    _both_plates.append(simulate(events=events,sensor=test,plt=None,toggle=None, use=use_coulomb))
    print("Finised sensor at %.04fmm." %test)

    
plt.subplot(121)
plt.plot(test_range,front_plates, linestyle='None', marker='o', label='Plates 1,2,3')
plt.plot(test_range,select_plates, linestyle='None', marker='o', label='Front Plates 2,3')
plt.plot(test_range,both_plates, linestyle='None', marker='o', label='Plates 1-6')
plt.xlabel("Scoring Plane Position (mm)")
plt.ylabel("RMS of Test Point in Line of Best Fits")
plt.ylim([0, max(front_plates+both_plates+select_plates)*1.05])
plt.legend(loc='upper left')
plt.grid(True, alpha=.2)
plt.title("Moving Scoring Plane %s Events"%events)

plt.subplot(122)
plt.plot(test_range,_front_plates, linestyle='None', marker='o', label='Plates 1,2,3')
plt.plot(test_range,_select_plates, linestyle='None', marker='o', label='Front Plates 2,3')
plt.plot(test_range,_both_plates, linestyle='None', marker='o', label='Plates 1-6')
plt.xlabel("Scoring Plane Position (mm)")
plt.ylabel("RMS of Test Point in Line of Best Fits")
plt.ylim([0, max(front_plates+both_plates+select_plates)*1.05])
plt.legend(loc='upper left')
plt.grid(True, alpha=.2)
plt.title("Moving Scoring Plane, No Coulomb With %s Events"%events)

file_name="moving_sensor.json"
with open(file_name,"w+") as f:
    output={
        'test_range': test_range.tolist(),
        'all_plates': both_plates,
        'front_plates': front_plates,
        'select_plates': select_plates
    }
    f.write(json.dumps(output))

print('wrote to file %s' % file_name)
plt.show()
