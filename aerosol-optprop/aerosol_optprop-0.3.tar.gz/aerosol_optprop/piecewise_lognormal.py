import miepython as mie
import numpy as np
from aerosol_optprop.lognormal import Lognormal
from aerosol_optprop.util import CrossSection
from scipy.special import erfc


class PiecewiseLognormal(Lognormal):

    def __init__(self, median_radius: float, width: float, n: float=1.0,
                 min_radius: float=0.0, max_radius: float=np.inf):

        super().__init__(median_radius=median_radius, width=width, n=n)

        self.min_radius = min_radius
        self.max_radius = max_radius
        self._n /= self._cdf(self.max_radius)  # normalize _n so the pdf still sums to n

    @property
    def n(self):
        return self._n * self._cdf(self.max_radius)

    @property
    def radii(self):
        rad = super().radii
        rad = rad[(rad >= self.min_radius) & (rad <= self.max_radius)]
        return np.unique(np.concatenate([[self.min_radius], rad, [self.max_radius]]))

    def _cdf(self, radii: np.array=None):
        if radii is None:
            radii = self.radii

        cdf0 = erfc(-(np.log(self.min_radius) - np.log(self.median_radius)) / (np.log(self.width) * np.sqrt(2)))
        cdf = erfc(-(np.log(radii) - np.log(self.median_radius)) / (np.log(self.width) * np.sqrt(2)))
        return (cdf - cdf0) * 0.5

    def cdf(self, radii: np.array=None):
        """
        Compute the cumulative distribution function. If no radii are provided the internal values are used.

        Parameters
        ----------
        radii:
            array of radii to compute the CDF

        Returns
        -------
        np.ndarray
            CDF at specified radii
        """
        return self._cdf(radii=radii) * self._n

    def pdf(self, radii: np.ndarray=None):
        pdf = super().pdf(radii=radii)
        pdf[(radii < self.min_radius)] = 0
        pdf[(radii > self.max_radius)] = 0
        return pdf

    @property
    def surface_area_density(self):
        return np.trapz(self.pdf() * self.radii ** 2, self.radii) * np.pi

    @property
    def volume_density(self):
        return np.trapz(self.pdf() * self.radii ** 3, self.radii) * 4 / 3 * np.pi
