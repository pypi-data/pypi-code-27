#!/usr/bin/env python3

########################################################################
#
# exsatsim_example.py
#
#   Example program of the EXSIM satellite simulator
#
# Copyright (C) 2018 EXSIM Development Team
#
########################################################################


########################################################################
# Required packages
########################################################################

import time
from matplotlib import pyplot as plt

from exsat import exsatsim

########################################################################
# Global variables
########################################################################


########################################################################
# Ancilliary classes
########################################################################

class Clock():
    """Simulator clock

    incSimTime - increment in seconds of the simulator clock
    sleepTime - increment in seconds of the wall clok

    incSimTime is used to move the simulator time.
    sleepTime is used to physically delay the clock.
    """

    def __init__(self, incSimTime=.1, sleepTime=.1):
        # All times in seconds
        self.incSimTime = incSimTime
        self.inv_incSimTime = 1./incSimTime
        self.sleepTime = sleepTime
        self.simTime = 0

    def move(self):
        # Sleep
        time.sleep(self.sleepTime)
        # Increase sim time, using integers to avoid rounding errors
        intSimTime = int(self.simTime * self.inv_incSimTime)
        intSimTime += 1
        self.simTime = 1.0 * intSimTime / self.inv_incSimTime

    def move_times(self, n):
        for i in range(0, n):
            self.move()

    def get_time(self):
        return self.simTime

    def print(self):
        print("Time: %.3f ms" % self.simTime)

########################################################################
# Global methods
########################################################################

def print_sim(clock, sim):
    evPos = sim.env.get_vehicle_position()
    evVel = sim.env.get_vehicle_velocity()
    x, y, z = evPos
    vx, vy, vz = evVel
    print_str = "Time: {} s    Pos: {} {} {}    Vel: {} {} {}".format(clock.get_time(), x, y, z, vx, vy, vz)
    print(print_str)

def print_step(title):
    print("\n***** " + title + "\n")

########################################################################
# main program
########################################################################

def main():
    # Init simulator
    clock = Clock(incSimTime=1, sleepTime=.001)
    sim = exsatsim.ExsatSimulator()
    sim.start()

    ### Play simulator

    print_step("Fly free")
    nSteps = 60
    for i in range(0, nSteps):
        print_sim(clock, sim)
        clock.move()
        sim.step()
    sim.stop()

    print_step("Add dV")
    sim.thrust(5, 1000)
    nSteps = 3
    for i in range(0, nSteps):
        print_sim(clock, sim)
        clock.move()
        sim.step()

    print_step("Fly free")
    nSteps = 60 * 30
    for i in range(0, nSteps):
        print_sim(clock, sim)
        clock.move()
        sim.step()

    ### Further play

    print_step("Fly free")
    nSteps = 60 * 49
    for i in range(0, nSteps):
        print_sim(clock, sim)
        clock.move()
        sim.step()

    print_step("Add dV")
    sim.thrust(5, 1000)
    nSteps = 3
    for i in range(0, nSteps):
        print_sim(clock, sim)
        clock.move()
        sim.step()

    print_step("Fly free")
    nSteps = 60 * 45
    for i in range(0, nSteps):
        print_sim(clock, sim)
        clock.move()
        sim.step()

    ### Stop simulator
    print_step("Stop simulator")
    sim.stop()

    plt.show(block=True)

if __name__ == '__main__':
    main()
