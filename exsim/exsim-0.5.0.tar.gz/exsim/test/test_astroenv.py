########################################################################
#
# test_astroenv.py
#
#   Unit test for astroenv.py
#
# Copyright (C) 2018 EXSIM Development Team
#
########################################################################

import unittest
from astropy import units as u

from exsat import astroenv

class TestAstroEnv(unittest.TestCase):

    def setUp(self):
        self._astroenv = astroenv.AstroEnv()
        self._x = 7078.1366
        self._y = 0
        self._z = 0
        self._a = self._x * 1000 * u.m
        self._ecc = 0 * u.one
        self._inc = 0 * u.rad
        self._raan = 0 * u.rad
        self._argp = 0 * u.rad
        self._nu = 0 * u.rad
        self._init_state = (self._a, self._ecc, self._inc, self._raan, self._argp, self._nu)

    def assert_vehicle_state(self, expected_position, expected_velocity):
        computed_position = self._astroenv.get_vehicle_position()
        computed_velocity = self._astroenv.get_vehicle_velocity()
        for i in range(0, 3):
            self.assertAlmostEqual(computed_position[i].value, expected_position[i].value, places=4)
            self.assertEqual(computed_position[i].unit, expected_position[i].unit)
            self.assertAlmostEqual(computed_velocity[i].value, expected_velocity[i].value, places=4)
            self.assertEqual(computed_velocity[i].unit, expected_velocity[i].unit)

    def test_set_vehicle_state(self):
        self.assertEqual(self._astroenv.get_vehicle_position(), None)
        self._astroenv.set_vehicle_state(self._init_state)
        self.assert_vehicle_state(
                expected_position = [self._x, self._y, self._z] * u.km,
                expected_velocity = [0., 7.5042867 , 0.] * u.km/u.s)

    def test_propagate(self):
        # Initial position
        self._astroenv.set_vehicle_state(self._init_state)
        # Propagate 6 steps
        expected_positions = [
                [7.07813656e+03, 7.50428669e-01, 0.00000000e+00] * u.km,
                [7.07813644e+03, 1.50085733e+00, 0.00000000e+00] * u.km,
                [7.07813624e+03, 2.25128597e+00, 0.00000000e+00] * u.km,
                [7.07813596e+03, 3.00171459e+00, 0.00000000e+00] * u.km,
                [7.07813561e+03, 3.75214318e+00, 0.00000000e+00] * u.km,
                [7.07813517e+03, 4.50257172e+00, 0.00000000e+00] * u.km 
                ]
        expected_velocities = [
                [-7.95609381e-04, 7.50428666e+00, 0.00000000e+00] * u.km/u.s,
                [-1.59121875e-03, 7.50428653e+00, 0.00000000e+00] * u.km/u.s,
                [-2.38682811e-03, 7.50428632e+00, 0.00000000e+00] * u.km/u.s,
                [-3.18243744e-03, 7.50428603e+00, 0.00000000e+00] * u.km/u.s,
                [-3.97804673e-03, 7.50428565e+00, 0.00000000e+00] * u.km/u.s,
                [-4.77365597e-03, 7.50428518e+00, 0.00000000e+00] * u.km/u.s
                ]
        assert(len(expected_positions) == len(expected_velocities))
        for i in range(0, len(expected_positions)):
            self._astroenv.step(.1)
            self.assert_vehicle_state(expected_positions[i], expected_velocities[i])
