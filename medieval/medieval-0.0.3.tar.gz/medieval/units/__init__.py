#!/usr/bin/env python
''' medieval.units
Logic and data models for representations of units in an army
'''


class located(object):

    def __init__(self, pos=(0,0), **kwargs):
        self.pos = pos

    @property
    def x(self):
        return self.pos[0]
    
    @property
    def y(self):
        return self.pos[1]


class Unit(located):
    
    def __init__(self, **kwargs):
        located.__init__(self, **kwargs)
        

class Squad(object):

    def __init__(self, units=None, formation=None):
        self.units = units
        self.formation = formation
