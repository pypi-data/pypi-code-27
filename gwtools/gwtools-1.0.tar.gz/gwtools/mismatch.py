# --- fitfuncs.py

"""
A collection of useful functions for comparing frequency domain
waveforms and evaluating errors.
Throughout, "overlap_err" is 1 - overlap, NOT optimizing over time shifts,
and "mismatch" is (1 - overlap) minimized over time shifts.
Other parameters are not optimized unless explicitly stated in the docstring.

See docs/mismatches.pdf for mathematics.
"""

from __future__ import division # for python 2


__copyright__ = "Copyright (C) 2015 Jonathan Blackman"
__status__    = "testing"
__author__    = "Jonathan Blackman"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import numpy as np
from . import const
from .harmonics import sYlm
from scipy.interpolate import UnivariateSpline as uspline

###############################################################################
# Inner products

def inner_complex(h1, h2, psd=None, df=1.0, ligo=False):
    """Frequency domain weighted complex inner product.
    h1, h2 are frequency domain waveforms (complex 1d arrays).
    psd can be None for unweighted (equivalent to a psd of ones) or an array
    of values the same length as h1 and h2.
    Note: PSD = ASD^2, should be ~ 10^-42 (not 10^-21) for aLIGO.

    if ligo=True we use the typical gw convention

        inner_ligo = 4 * Real(inner_complex)

    which comes from (i) folding f<0 frequencies (accounts for "2 * Real()")
    and (ii) overall factor of 2 which is convention.

    See, for example,
            https://arxiv.org/pdf/1602.03839.pdf (Eq 1)
            https://arxiv.org/pdf/1602.03509.pdf (Eq 6)
            https://arxiv.org/pdf/gr-qc/0509116.pdf (Eq 4.1) """

    if psd is None:
        result = df * h1.dot(h2.conjugate())
    else:
        result = df * h1.dot(h2.conjugate()/psd)

    if ligo:
        return 4.0 * np.real(result)
    else:
        return result 

#-----------------------------------------------------------------------------

def inner(h1, h2, psd=None, df=1.0, ligo=False):
    """Real frequency domain inner product.
    See inner_complex for details."""

    return np.real(inner_complex(h1, h2, psd, df, ligo))

#-----------------------------------------------------------------------------

def inner_complex_timeshift_series(h1, h2, psd=None, n_zeros=0):
    """Uses an inverse fft to compute inner_complex of h1 and
    h2*exp(2*pi*i*f*dt) for dt=0, 1/f_max, 2/f_max, ..."""

    if n_zeros > 0:
        h1_z = np.append(h1, np.zeros(n_zeros))
        h2_z = np.append(h2, np.zeros(n_zeros))
        if psd is None:
            psd2 = None
        else:
            psd2 = np.append(psd, np.ones(n_zeros))

        return inner_complex_timeshift_series(h1_z, h2_z, psd=psd2)

    if psd is None:
        return np.fft.fft(h1*h2.conjugate())
    return np.fft.fft(h1*h2.conjugate()/psd)

#-----------------------------------------------------------------------------

def inner_timeshift_series(h1, h2, psd=None, n_zeros=0):
    """Real part of inner_complex_timeshift_series"""

    return np.real(inner_complex_timeshift_series(h1, h2, psd, n_zeros))

#-----------------------------------------------------------------------------


###############################################################################
# h conversions

def modes_to_hf(h_modes, theta, phi):
    """Sums spin-weighted spherical harmonic modes (s=-2) evaluated at
    (theta, phi) to obtain the waveform.

    h_modes: A 2d array with shape (n_modes, n_samples), ordered
        [(2, -2), ..., (2, 2), (3, -3), ..., (3, 3), ...]

    returns hf, a 1d array with length n_samples."""

    L, m = 2, -2
    coefs = 1.j*np.zeros(len(h_modes))
    for i in range(len(h_modes)):
        coefs[i] = sYlm(-2, L, m, theta, phi)
        m += 1
        if m > L:
            L += 1
            m = -L

    if m != -L:
        raise Exception("Incomplete set of modes! Missing (%s, %s)"%(L, m))

    return coefs.dot(h_modes)

#-----------------------------------------------------------------------------

###############################################################################
# Utility

def _cyclic_quadratic_peak(y):
    """Finds the peak value of y using a quadratic curve through the max
    value and its neighbors. Assumes periodic boundary conditions if the max
    is at the edge.
    Returns i_peak (float), y_peak."""

    n = len(y)
    idx = np.argmax(y)
    y0 = y[idx]
    rp1 = y[(idx+1)%n] - y0
    rm1 = y[(idx-1)%n] - y0
    b = 0.5*(rp1 - rm1)
    c = 0.5*(rp1 + rm1)
    if c==0.:
        print('Warning: no quadratic term present in time optimization, using argmax')
        return idx, y0
    y_peak = y0 - 0.25*b*b/c
    i_peak = idx - 0.5*b/c
    return i_peak, y_peak

#-----------------------------------------------------------------------------

def _timeshift(df, nsamples, i_peak):
    """Finds the timeshift from inverse fft information"""
    dt = i_peak/(df*nsamples)
    if i_peak > 0.5*nsamples:
        dt -= 1./df
    return dt

#-----------------------------------------------------------------------------

def _cyclic_interp_phase(x, i_interp):
    """
    Uses a cubic spline to interpolate the angle of x onto the
    "index" i_interp which can be a float.
    Uses periodic boundary conditions.
    """

    i0 = int(i_interp)
    x2 = np.unwrap(np.angle(np.roll(x, -i0+1)[:4]))
    return uspline(np.array([-1., 0., 1., 2.]), x2, s=0)(np.array([i_interp - i0]))[0]

###############################################################################

def overlap_err(h1, h2, psd=None):
    n1 = inner(h1, h1, psd)
    n2 = inner(h2, h2, psd)
    return 1. - inner(h1, h2, psd)/np.sqrt(n1*n2)

#-----------------------------------------------------------------------------

def mismatch(h1, h2, psd=None, df=1., polarization_shift=True):
    """
    Minimizes the overlap error over time shifts and (possibly)
    polarization angle shifts.
    Returns:
        mismatch
        time shift
        polarization angle shift (returns zero if polarization_shift is False)
    If df is in Hz, the returned time shift is in seconds.
    A quadratic fit to the largest overlap and its nearest neighbors is used
    to determine the maximum, but be sure the waveforms are long enough
    (pad with zeros if needed) to get a good time-shift resolution!
    """

    n1 = inner(h1, h1, psd)
    n2 = inner(h2, h2, psd)
    d = inner_complex_timeshift_series(h1, h2, psd)
    if polarization_shift:
        i_max, d_max = _cyclic_quadratic_peak(abs(d))
        psi = 0.5 * _cyclic_interp_phase(d, i_max)
    else:
        i_max, d_max = _cyclic_quadratic_peak(np.real(d))
        psi = 0.
        
    dt = _timeshift(df, len(d), i_max)
    return 1. - d_max/np.sqrt(n1*n2), dt, psi
        

#-----------------------------------------------------------------------------
