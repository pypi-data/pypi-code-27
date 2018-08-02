from unittest import TestCase
from aerosol_optprop import Lognormal
from aerosol_optprop import PiecewiseLognormal


class TestLognormal(TestCase):

    def test_lognormal_crosssection(self):
        aerosol = Lognormal(median_radius=0.08, width=1.6)
        xsec = aerosol.cross_section(wavelength=0.75)
        self.assertAlmostEqual(xsec.scattering, 1.2596131660579982e-10, delta=1e-17)
        self.assertAlmostEqual(xsec.extinction, 1.2596140435184066e-10, delta=1e-17)
        self.assertAlmostEqual(xsec.absorption, 8.7746040867533813e-17, delta=1e-20)


class TestPiecewiseLognormal(TestCase):

    def test_lognormal_crosssection(self):
        aerosol = PiecewiseLognormal(median_radius=0.08, width=1.6, min_radius=0.08, max_radius=0.1)
        xsec = aerosol.cross_section(wavelength=0.75)
        self.assertAlmostEqual(xsec.scattering, 1.4306691020243164e-11, delta=1e-17)
        self.assertAlmostEqual(xsec.extinction, 1.4306726763014103e-11, delta=1e-17)
        self.assertAlmostEqual(xsec.absorption, 3.5742770940776321e-17, delta=1e-20)
