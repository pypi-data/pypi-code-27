import timeit

plates=range(6)
events=100
start = timeit.default_timer()
a=[i%len(plates) for i in range(len(plates)*events)]
stop  = timeit.default_timer()
time1 = stop-start

print("Done in %.05f"%time1)
start = timeit.default_timer()
b=[7,8,4,3,6,7]
for i in range(events):
    b+=b.copy()
stop  = timeit.default_timer()
time2 = stop-start
print("Done in %.05f"%time2)
print(time1,time2)
if time1>time2:
    print("first method better.")
else:
    print("second method better.")
