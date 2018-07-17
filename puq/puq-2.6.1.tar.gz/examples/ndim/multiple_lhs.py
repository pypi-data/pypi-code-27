#!/usr/bin/env python
"""
Example of using a UQ method with a sweep.

Usage: puq start multiple
"""
from puq import *
import math

def run():
    # Declare our parameters here

    a = UniformParameter('alpha', 'alpha', min=-math.pi, max=math.pi)

    # Which host to use
    host = InteractiveHost()

    uq = LHS([a], 50)

    # If we create a TestProgram object, we can add a description
    # and the plots will use it.
    prog = TestProgram('./mult_prog.py', desc='Multiple Test Program')

    # Create a Sweep object
    return Sweep(uq, host, prog)
