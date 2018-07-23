########################################################################
#
# astroenv.py
#
#   Model of a space environment basde on poliastro.
#
# Copyright (C) 2018 EXSIM Development Team
#
########################################################################

import numpy as np
from astropy import units as u
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.maneuver import Maneuver
from poliastro.plotting import OrbitPlotter
from poliastro.plotting import plot

from simcore import env

########################################################################
# class AstroEnv
#
#   Model a space environment based on poliastro
########################################################################

class AstroEnv(env.Env):
    """
    Realistic space environment based on poliastro.
    """

    def __init__(self):
        super().__init__()
        self.prop = None
        self.op = OrbitPlotter()

    @property
    def angular_speed(self):
        return 0.0

    def set_vehicle_state(self, state):
        self.prop = Orbit.from_classical(Earth, *state)

    def get_vehicle_velocity(self):
        if self.prop:
            return self.prop.state.v

    def get_vehicle_position(self):
        if self.prop:
            return self.prop.state.r

    def step(self, delta_time=1):
        if self.prop:
            self.prop = self.prop.propagate(delta_time * u.s)

    def thrust(self, dt, dv):
        """
        Apply dv (m/s) during dt (s).
        """
        if self.prop:
            v = self.prop.state.v.value
            vu = v / np.linalg.norm(v)
            dvvect = (vu * dv) * u.m / u.s
            man = Maneuver((dt * u.s, dvvect))
            self.op.plot(self.prop, label='initial')
            self.prop = self.prop.apply_maneuver(man)
            self.op.plot(self.prop, label='final')

    def plot(self, label):
            self.op.plot(self.prop, label=label)
