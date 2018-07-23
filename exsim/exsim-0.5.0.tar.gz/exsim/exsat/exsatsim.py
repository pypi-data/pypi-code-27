########################################################################
#
# exsatsim.py
#
#   EXSIM satellite simulator, based on poliastro.
#
# Copyright (C) 2018 EXSIM Development Team
#
########################################################################

from astropy import units as u

from simcore import simulator
from simcore import vehicle
from . import astroenv

########################################################################
# class ExsatSimulator
#
#   Satellite simulator based on poliastro
#
########################################################################

class ExsatSimulator(simulator.Simulator):
    """EXSIM satellite simulator, based on poliastro.
    """

    class DummySat2d(vehicle.Vehicle):
        """Dummy model of a satellite vehicle
        To be replaced by a proper model on a separate module.
        """
        def __init__(self):
            super().__init__()
        def step(self, delta_simclock):
            pass

    def __init__(self):
        super().__init__()

    def create_env(self):
        env = astroenv.AstroEnv()
        return env

    def create_vehicle(self):
        vehicle = ExsatSimulator.DummySat2d()
        return vehicle

    def vehicle_init_state(self):
        a = 7078136.6 * u.m
        ecc = 0 * u.one
        inc = 0 * u.rad
        raan = 0 * u.rad
        argp = 0 * u.rad
        nu = 0 * u.rad
        return (a, ecc, inc, raan, argp, nu)

    def thrust(self, dt, dv):
        """
        Apply dv (m/s) during dt (s).
        """
        self.env.thrust(dt, dv)

    def stop(self):
        self.env.plot('stop')
