import matplotlib.pyplot as plt
from simulation import simulate
from numpy import linspace
import json
plate_min=305
plate_max=635
test_range=linspace(plate_min,plate_max,20)

select_plates=[]
_select_plates=[]
events=500
for test in test_range:
    use_coulomb=True
    plt.subplot(223)
    select_plates.append(simulate(events=events,sensor=test,toggle=None, use=use_coulomb,plt=plt))
    use_coulomb=False
    plt.subplot(224)
    _select_plates.append(simulate(events=events,sensor=test,toggle=None, use=use_coulomb, plt=plt))
    print("Finised sensor at %.04fmm." %test)

    
plt.subplot(221)
plt.plot(test_range,select_plates, linestyle='None', marker='o', label='Front Plates 2,3')
plt.xlabel("Scoring Plane Position (mm)")
plt.ylabel("RMS of Test Point in Line of Best Fits")
plt.ylim([0, max(select_plates)*1.05])
plt.legend(loc='upper left')
plt.grid(True, alpha=.2)
plt.title("Moving Scoring Plane %s Events"%events)

plt.subplot(222)
plt.plot(test_range,_select_plates, linestyle='None', marker='o', label='Front Plates 2,3')
plt.xlabel("Scoring Plane Position (mm)")
plt.ylabel("RMS of Test Point in Line of Best Fits")
plt.ylim([0, max(_select_plates)*1.05])
plt.legend(loc='upper left')
plt.grid(True, alpha=.2)
plt.title("Moving Scoring Plane, No Coulomb With %s Events"%events)

plt.show()
