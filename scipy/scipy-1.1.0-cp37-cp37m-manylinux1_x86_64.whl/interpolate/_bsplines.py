from __future__ import division, print_function, absolute_import

import functools
import operator

import numpy as np
from scipy._lib.six import string_types
from scipy.linalg import (get_lapack_funcs, LinAlgError,
                          cholesky_banded, cho_solve_banded)
from . import _bspl
from . import _fitpack_impl
from . import _fitpack as _dierckx

__all__ = ["BSpline", "make_interp_spline", "make_lsq_spline"]


# copy-paste from interpolate.py
def prod(x):
    """Product of a list of numbers; ~40x faster vs np.prod for Python tuples"""
    if len(x) == 0:
        return 1
    return functools.reduce(operator.mul, x)


def _get_dtype(dtype):
    """Return np.complex128 for complex dtypes, np.float64 otherwise."""
    if np.issubdtype(dtype, np.complexfloating):
        return np.complex_
    else:
        return np.float_


def _as_float_array(x, check_finite=False):
    """Convert the input into a C contiguous float array.

    NB: Upcasts half- and single-precision floats to double precision.
    """
    x = np.ascontiguousarray(x)
    dtyp = _get_dtype(x.dtype)
    x = x.astype(dtyp, copy=False)
    if check_finite and not np.isfinite(x).all():
        raise ValueError("Array must not contain infs or nans.")
    return x


class BSpline(object):
    r"""Univariate spline in the B-spline basis.

    .. math::

        S(x) = \sum_{j=0}^{n-1} c_j  B_{j, k; t}(x)

    where :math:`B_{j, k; t}` are B-spline basis functions of degree `k`
    and knots `t`.

    Parameters
    ----------
    t : ndarray, shape (n+k+1,)
        knots
    c : ndarray, shape (>=n, ...)
        spline coefficients
    k : int
        B-spline order
    extrapolate : bool or 'periodic', optional
        whether to extrapolate beyond the base interval, ``t[k] .. t[n]``,
        or to return nans.
        If True, extrapolates the first and last polynomial pieces of b-spline
        functions active on the base interval.
        If 'periodic', periodic extrapolation is used.
        Default is True.
    axis : int, optional
        Interpolation axis. Default is zero.

    Attributes
    ----------
    t : ndarray
        knot vector
    c : ndarray
        spline coefficients
    k : int
        spline degree
    extrapolate : bool
        If True, extrapolates the first and last polynomial pieces of b-spline
        functions active on the base interval.
    axis : int
        Interpolation axis.
    tck : tuple
        A read-only equivalent of ``(self.t, self.c, self.k)``

    Methods
    -------
    __call__
    basis_element
    derivative
    antiderivative
    integrate
    construct_fast

    Notes
    -----
    B-spline basis elements are defined via

    .. math::

        B_{i, 0}(x) = 1, \textrm{if $t_i \le x < t_{i+1}$, otherwise $0$,}

        B_{i, k}(x) = \frac{x - t_i}{t_{i+k} - t_i} B_{i, k-1}(x)
                 + \frac{t_{i+k+1} - x}{t_{i+k+1} - t_{i+1}} B_{i+1, k-1}(x)

    **Implementation details**

    - At least ``k+1`` coefficients are required for a spline of degree `k`,
      so that ``n >= k+1``. Additional coefficients, ``c[j]`` with
      ``j > n``, are ignored.

    - B-spline basis elements of degree `k` form a partition of unity on the
      *base interval*, ``t[k] <= x <= t[n]``.


    Examples
    --------

    Translating the recursive definition of B-splines into Python code, we have:

    >>> def B(x, k, i, t):
    ...    if k == 0:
    ...       return 1.0 if t[i] <= x < t[i+1] else 0.0
    ...    if t[i+k] == t[i]:
    ...       c1 = 0.0
    ...    else:
    ...       c1 = (x - t[i])/(t[i+k] - t[i]) * B(x, k-1, i, t)
    ...    if t[i+k+1] == t[i+1]:
    ...       c2 = 0.0
    ...    else:
    ...       c2 = (t[i+k+1] - x)/(t[i+k+1] - t[i+1]) * B(x, k-1, i+1, t)
    ...    return c1 + c2

    >>> def bspline(x, t, c, k):
    ...    n = len(t) - k - 1
    ...    assert (n >= k+1) and (len(c) >= n)
    ...    return sum(c[i] * B(x, k, i, t) for i in range(n))

    Note that this is an inefficient (if straightforward) way to
    evaluate B-splines --- this spline class does it in an equivalent,
    but much more efficient way.

    Here we construct a quadratic spline function on the base interval
    ``2 <= x <= 4`` and compare with the naive way of evaluating the spline:

    >>> from scipy.interpolate import BSpline
    >>> k = 2
    >>> t = [0, 1, 2, 3, 4, 5, 6]
    >>> c = [-1, 2, 0, -1]
    >>> spl = BSpline(t, c, k)
    >>> spl(2.5)
    array(1.375)
    >>> bspline(2.5, t, c, k)
    1.375

    Note that outside of the base interval results differ. This is because
    `BSpline` extrapolates the first and last polynomial pieces of b-spline
    functions active on the base interval.

    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> xx = np.linspace(1.5, 4.5, 50)
    >>> ax.plot(xx, [bspline(x, t, c ,k) for x in xx], 'r-', lw=3, label='naive')
    >>> ax.plot(xx, spl(xx), 'b-', lw=4, alpha=0.7, label='BSpline')
    >>> ax.grid(True)
    >>> ax.legend(loc='best')
    >>> plt.show()


    References
    ----------
    .. [1] Tom Lyche and Knut Morken, Spline methods,
        http://www.uio.no/studier/emner/matnat/ifi/INF-MAT5340/v05/undervisningsmateriale/
    .. [2] Carl de Boor, A practical guide to splines, Springer, 2001.

    """
    def __init__(self, t, c, k, extrapolate=True, axis=0):
        super(BSpline, self).__init__()

        self.k = int(k)
        self.c = np.asarray(c)
        self.t = np.ascontiguousarray(t, dtype=np.float64)

        if extrapolate == 'periodic':
            self.extrapolate = extrapolate
        else:
            self.extrapolate = bool(extrapolate)

        n = self.t.shape[0] - self.k - 1

        if not (0 <= axis < self.c.ndim):
            raise ValueError("%s must be between 0 and %s" % (axis, c.ndim))

        self.axis = axis
        if axis != 0:
            # roll the interpolation axis to be the first one in self.c
            # More specifically, the target shape for self.c is (n, ...),
            # and axis !=0 means that we have c.shape (..., n, ...)
            #                                               ^
            #                                              axis
            self.c = np.rollaxis(self.c, axis)

        if k < 0:
            raise ValueError("Spline order cannot be negative.")
        if int(k) != k:
            raise ValueError("Spline order must be integer.")
        if self.t.ndim != 1:
            raise ValueError("Knot vector must be one-dimensional.")
        if n < self.k + 1:
            raise ValueError("Need at least %d knots for degree %d" %
                    (2*k + 2, k))
        if (np.diff(self.t) < 0).any():
            raise ValueError("Knots must be in a non-decreasing order.")
        if len(np.unique(self.t[k:n+1])) < 2:
            raise ValueError("Need at least two internal knots.")
        if not np.isfinite(self.t).all():
            raise ValueError("Knots should not have nans or infs.")
        if self.c.ndim < 1:
            raise ValueError("Coefficients must be at least 1-dimensional.")
        if self.c.shape[0] < n:
            raise ValueError("Knots, coefficients and degree are inconsistent.")

        dt = _get_dtype(self.c.dtype)
        self.c = np.ascontiguousarray(self.c, dtype=dt)

    @classmethod
    def construct_fast(cls, t, c, k, extrapolate=True, axis=0):
        """Construct a spline without making checks.

        Accepts same parameters as the regular constructor. Input arrays
        `t` and `c` must of correct shape and dtype.
        """
        self = object.__new__(cls)
        self.t, self.c, self.k = t, c, k
        self.extrapolate = extrapolate
        self.axis = axis
        return self

    @property
    def tck(self):
        """Equivalent to ``(self.t, self.c, self.k)`` (read-only).
        """
        return self.t, self.c, self.k

    @classmethod
    def basis_element(cls, t, extrapolate=True):
        """Return a B-spline basis element ``B(x | t[0], ..., t[k+1])``.

        Parameters
        ----------
        t : ndarray, shape (k+1,)
            internal knots
        extrapolate : bool or 'periodic', optional
            whether to extrapolate beyond the base interval, ``t[0] .. t[k+1]``,
            or to return nans.
            If 'periodic', periodic extrapolation is used.
            Default is True.

        Returns
        -------
        basis_element : callable
            A callable representing a B-spline basis element for the knot
            vector `t`.

        Notes
        -----
        The order of the b-spline, `k`, is inferred from the length of `t` as
        ``len(t)-2``. The knot vector is constructed by appending and prepending
        ``k+1`` elements to internal knots `t`.

        Examples
        --------

        Construct a cubic b-spline:

        >>> from scipy.interpolate import BSpline
        >>> b = BSpline.basis_element([0, 1, 2, 3, 4])
        >>> k = b.k
        >>> b.t[k:-k]
        array([ 0.,  1.,  2.,  3.,  4.])
        >>> k
        3

        Construct a second order b-spline on ``[0, 1, 1, 2]``, and compare
        to its explicit form:

        >>> t = [-1, 0, 1, 1, 2]
        >>> b = BSpline.basis_element(t[1:])
        >>> def f(x):
        ...     return np.where(x < 1, x*x, (2. - x)**2)

        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> x = np.linspace(0, 2, 51)
        >>> ax.plot(x, b(x), 'g', lw=3)
        >>> ax.plot(x, f(x), 'r', lw=8, alpha=0.4)
        >>> ax.grid(True)
        >>> plt.show()

        """
        k = len(t) - 2
        t = _as_float_array(t)
        t = np.r_[(t[0]-1,) * k, t, (t[-1]+1,) * k]
        c = np.zeros_like(t)
        c[k] = 1.
        return cls.construct_fast(t, c, k, extrapolate)

    def __call__(self, x, nu=0, extrapolate=None):
        """
        Evaluate a spline function.

        Parameters
        ----------
        x : array_like
            points to evaluate the spline at.
        nu: int, optional
            derivative to evaluate (default is 0).
        extrapolate : bool or 'periodic', optional
            whether to extrapolate based on the first and last intervals
            or return nans. If 'periodic', periodic extrapolation is used.
            Default is `self.extrapolate`.

        Returns
        -------
        y : array_like
            Shape is determined by replacing the interpolation axis
            in the coefficient array with the shape of `x`.

        """
        if extrapolate is None:
            extrapolate = self.extrapolate
        x = np.asarray(x)
        x_shape, x_ndim = x.shape, x.ndim
        x = np.ascontiguousarray(x.ravel(), dtype=np.float_)

        # With periodic extrapolation we map x to the segment
        # [self.t[k], self.t[n]].
        if extrapolate == 'periodic':
            n = self.t.size - self.k - 1
            x = self.t[self.k] + (x - self.t[self.k]) % (self.t[n] -
                                                         self.t[self.k])
            extrapolate = False

        out = np.empty((len(x), prod(self.c.shape[1:])), dtype=self.c.dtype)
        self._ensure_c_contiguous()
        self._evaluate(x, nu, extrapolate, out)
        out = out.reshape(x_shape + self.c.shape[1:])
        if self.axis != 0:
            # transpose to move the calculated values to the interpolation axis
            l = list(range(out.ndim))
            l = l[x_ndim:x_ndim+self.axis] + l[:x_ndim] + l[x_ndim+self.axis:]
            out = out.transpose(l)
        return out

    def _evaluate(self, xp, nu, extrapolate, out):
        _bspl.evaluate_spline(self.t, self.c.reshape(self.c.shape[0], -1),
                self.k, xp, nu, extrapolate, out)

    def _ensure_c_contiguous(self):
        """
        c and t may be modified by the user. The Cython code expects
        that they are C contiguous.

        """
        if not self.t.flags.c_contiguous:
            self.t = self.t.copy()
        if not self.c.flags.c_contiguous:
            self.c = self.c.copy()

    def derivative(self, nu=1):
        """Return a b-spline representing the derivative.

        Parameters
        ----------
        nu : int, optional
            Derivative order.
            Default is 1.

        Returns
        -------
        b : BSpline object
            A new instance representing the derivative.

        See Also
        --------
        splder, splantider

        """
        c = self.c
        # pad the c array if needed
        ct = len(self.t) - len(c)
        if ct > 0:
            c = np.r_[c, np.zeros((ct,) + c.shape[1:])]
        tck = _fitpack_impl.splder((self.t, c, self.k), nu)
        return self.construct_fast(*tck, extrapolate=self.extrapolate,
                                    axis=self.axis)

    def antiderivative(self, nu=1):
        """Return a b-spline representing the antiderivative.

        Parameters
        ----------
        nu : int, optional
            Antiderivative order. Default is 1.

        Returns
        -------
        b : BSpline object
            A new instance representing the antiderivative.

        Notes
        -----
        If antiderivative is computed and ``self.extrapolate='periodic'``,
        it will be set to False for the returned instance. This is done because
        the antiderivative is no longer periodic and its correct evaluation
        outside of the initially given x interval is difficult.

        See Also
        --------
        splder, splantider

        """
        c = self.c
        # pad the c array if needed
        ct = len(self.t) - len(c)
        if ct > 0:
            c = np.r_[c, np.zeros((ct,) + c.shape[1:])]
        tck = _fitpack_impl.splantider((self.t, c, self.k), nu)

        if self.extrapolate == 'periodic':
            extrapolate = False
        else:
            extrapolate = self.extrapolate

        return self.construct_fast(*tck, extrapolate=extrapolate,
                                   axis=self.axis)

    def integrate(self, a, b, extrapolate=None):
        """Compute a definite integral of the spline.

        Parameters
        ----------
        a : float
            Lower limit of integration.
        b : float
            Upper limit of integration.
        extrapolate : bool or 'periodic', optional
            whether to extrapolate beyond the base interval,
            ``t[k] .. t[-k-1]``, or take the spline to be zero outside of the
            base interval. If 'periodic', periodic extrapolation is used.
            If None (default), use `self.extrapolate`.

        Returns
        -------
        I : array_like
            Definite integral of the spline over the interval ``[a, b]``.

        Examples
        --------
        Construct the linear spline ``x if x < 1 else 2 - x`` on the base
        interval :math:`[0, 2]`, and integrate it

        >>> from scipy.interpolate import BSpline
        >>> b = BSpline.basis_element([0, 1, 2])
        >>> b.integrate(0, 1)
        array(0.5)

        If the integration limits are outside of the base interval, the result
        is controlled by the `extrapolate` parameter

        >>> b.integrate(-1, 1)
        array(0.0)
        >>> b.integrate(-1, 1, extrapolate=False)
        array(0.5)

        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> ax.grid(True)
        >>> ax.axvline(0, c='r', lw=5, alpha=0.5)  # base interval
        >>> ax.axvline(2, c='r', lw=5, alpha=0.5)
        >>> xx = [-1, 1, 2]
        >>> ax.plot(xx, b(xx))
        >>> plt.show()

        """
        if extrapolate is None:
            extrapolate = self.extrapolate

        # Prepare self.t and self.c.
        self._ensure_c_contiguous()

        # Swap integration bounds if needed.
        sign = 1
        if b < a:
            a, b = b, a
            sign = -1
        n = self.t.size - self.k - 1

        if extrapolate != "periodic" and not extrapolate:
            # Shrink the integration interval, if needed.
            a = max(a, self.t[self.k])
            b = min(b, self.t[n])

            if self.c.ndim == 1:
                # Fast path: use FITPACK's routine
                # (cf _fitpack_impl.splint).
                t, c, k = self.tck
                integral, wrk = _dierckx._splint(t, c, k, a, b)
                return integral * sign 

        out = np.empty((2, prod(self.c.shape[1:])), dtype=self.c.dtype)

        # Compute the antiderivative.
        c = self.c
        ct = len(self.t) - len(c)
        if ct > 0:
            c = np.r_[c, np.zeros((ct,) + c.shape[1:])]
        ta, ca, ka = _fitpack_impl.splantider((self.t, c, self.k), 1)

        if extrapolate == 'periodic':
            # Split the integral into the part over period (can be several
            # of them) and the remaining part.

            ts, te = self.t[self.k], self.t[n]
            period = te - ts
            interval = b - a
            n_periods, left = divmod(interval, period)

            if n_periods > 0:
                # Evaluate the difference of antiderivatives.
                x = np.asarray([ts, te], dtype=np.float_)
                _bspl.evaluate_spline(ta, ca.reshape(ca.shape[0], -1),
                                      ka, x, 0, False, out)
                integral = out[1] - out[0]
                integral *= n_periods
            else:
                integral = np.zeros((1, prod(self.c.shape[1:])),
                                    dtype=self.c.dtype)

            # Map a to [ts, te], b is always a + left.
            a = ts + (a - ts) % period
            b = a + left

            # If b <= te then we need to integrate over [a, b], otherwise
            # over [a, te] and from xs to what is remained.
            if b <= te:
                x = np.asarray([a, b], dtype=np.float_)
                _bspl.evaluate_spline(ta, ca.reshape(ca.shape[0], -1),
                                      ka, x, 0, False, out)
                integral += out[1] - out[0]
            else:
                x = np.asarray([a, te], dtype=np.float_)
                _bspl.evaluate_spline(ta, ca.reshape(ca.shape[0], -1),
                                      ka, x, 0, False, out)
                integral += out[1] - out[0]

                x = np.asarray([ts, ts + b - te], dtype=np.float_)
                _bspl.evaluate_spline(ta, ca.reshape(ca.shape[0], -1),
                                      ka, x, 0, False, out)
                integral += out[1] - out[0]
        else:
            # Evaluate the difference of antiderivatives.
            x = np.asarray([a, b], dtype=np.float_)
            _bspl.evaluate_spline(ta, ca.reshape(ca.shape[0], -1),
                                  ka, x, 0, extrapolate, out)
            integral = out[1] - out[0]

        integral *= sign
        return integral.reshape(ca.shape[1:])


#################################
#  Interpolating spline helpers #
#################################

def _not_a_knot(x, k):
    """Given data x, construct the knot vector w/ not-a-knot BC.
    cf de Boor, XIII(12)."""
    x = np.asarray(x)
    if k % 2 != 1:
        raise ValueError("Odd degree for now only. Got %s." % k)

    m = (k - 1) // 2
    t = x[m+1:-m-1]
    t = np.r_[(x[0],)*(k+1), t, (x[-1],)*(k+1)]
    return t


def _augknt(x, k):
    """Construct a knot vector appropriate for the order-k interpolation."""
    return np.r_[(x[0],)*k, x, (x[-1],)*k]


def _convert_string_aliases(deriv, target_shape):
    if isinstance(deriv, string_types):
        if deriv == "clamped":
            deriv = [(1, np.zeros(target_shape))]
        elif deriv == "natural":
            deriv = [(2, np.zeros(target_shape))]
        else:
            raise ValueError("Unknown boundary condition : %s" % deriv)
    return deriv


def make_interp_spline(x, y, k=3, t=None, bc_type=None, axis=0,
                       check_finite=True):
    """Compute the (coefficients of) interpolating B-spline.

    Parameters
    ----------
    x : array_like, shape (n,)
        Abscissas.
    y : array_like, shape (n, ...)
        Ordinates.
    k : int, optional
        B-spline degree. Default is cubic, k=3.
    t : array_like, shape (nt + k + 1,), optional.
        Knots.
        The number of knots needs to agree with the number of datapoints and
        the number of derivatives at the edges. Specifically, ``nt - n`` must
        equal ``len(deriv_l) + len(deriv_r)``.
    bc_type : 2-tuple or None
        Boundary conditions.
        Default is None, which means choosing the boundary conditions
        automatically. Otherwise, it must be a length-two tuple where the first
        element sets the boundary conditions at ``x[0]`` and the second
        element sets the boundary conditions at ``x[-1]``. Each of these must
        be an iterable of pairs ``(order, value)`` which gives the values of
        derivatives of specified orders at the given edge of the interpolation
        interval.
        Alternatively, the following string aliases are recognized:

        * ``"clamped"``: The first derivatives at the ends are zero. This is
           equivalent to ``bc_type=((1, 0.0), (1, 0.0))``.
        * ``"natural"``: The second derivatives at ends are zero. This is
          equivalent to ``bc_type=((2, 0.0), (2, 0.0))``.
        * ``"not-a-knot"`` (default): The first and second segments are the same
          polynomial. This is equivalent to having ``bc_type=None``.

    axis : int, optional
        Interpolation axis. Default is 0.
    check_finite : bool, optional
        Whether to check that the input arrays contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
        Default is True.

    Returns
    -------
    b : a BSpline object of the degree ``k`` and with knots ``t``.

    Examples
    --------

    Use cubic interpolation on Chebyshev nodes:

    >>> def cheb_nodes(N):
    ...     jj = 2.*np.arange(N) + 1
    ...     x = np.cos(np.pi * jj / 2 / N)[::-1]
    ...     return x

    >>> x = cheb_nodes(20)
    >>> y = np.sqrt(1 - x**2)

    >>> from scipy.interpolate import BSpline, make_interp_spline
    >>> b = make_interp_spline(x, y)
    >>> np.allclose(b(x), y)
    True

    Note that the default is a cubic spline with a not-a-knot boundary condition

    >>> b.k
    3

    Here we use a 'natural' spline, with zero 2nd derivatives at edges:

    >>> l, r = [(2, 0.0)], [(2, 0.0)]
    >>> b_n = make_interp_spline(x, y, bc_type=(l, r))  # or, bc_type="natural"
    >>> np.allclose(b_n(x), y)
    True
    >>> x0, x1 = x[0], x[-1]
    >>> np.allclose([b_n(x0, 2), b_n(x1, 2)], [0, 0])
    True

    Interpolation of parametric curves is also supported. As an example, we
    compute a discretization of a snail curve in polar coordinates

    >>> phi = np.linspace(0, 2.*np.pi, 40)
    >>> r = 0.3 + np.cos(phi)
    >>> x, y = r*np.cos(phi), r*np.sin(phi)  # convert to Cartesian coordinates

    Build an interpolating curve, parameterizing it by the angle

    >>> from scipy.interpolate import make_interp_spline
    >>> spl = make_interp_spline(phi, np.c_[x, y])

    Evaluate the interpolant on a finer grid (note that we transpose the result
    to unpack it into a pair of x- and y-arrays)

    >>> phi_new = np.linspace(0, 2.*np.pi, 100)
    >>> x_new, y_new = spl(phi_new).T

    Plot the result

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(x, y, 'o')
    >>> plt.plot(x_new, y_new, '-')
    >>> plt.show()

    See Also
    --------
    BSpline : base class representing the B-spline objects
    CubicSpline : a cubic spline in the polynomial basis
    make_lsq_spline : a similar factory function for spline fitting
    UnivariateSpline : a wrapper over FITPACK spline fitting routines
    splrep : a wrapper over FITPACK spline fitting routines

    """
    # convert string aliases for the boundary conditions
    if bc_type is None or bc_type == 'not-a-knot':
        deriv_l, deriv_r = None, None
    elif isinstance(bc_type, string_types):
        deriv_l, deriv_r = bc_type, bc_type
    else:
        deriv_l, deriv_r = bc_type

    # special-case k=0 right away
    if k == 0:
        if any(_ is not None for _ in (t, deriv_l, deriv_r)):
            raise ValueError("Too much info for k=0: t and bc_type can only "
                             "be None.")
        x = _as_float_array(x, check_finite)
        t = np.r_[x, x[-1]]
        c = np.asarray(y)
        c = np.ascontiguousarray(c, dtype=_get_dtype(c.dtype))
        return BSpline.construct_fast(t, c, k, axis=axis)

    # special-case k=1 (e.g., Lyche and Morken, Eq.(2.16))
    if k == 1 and t is None:
        if not (deriv_l is None and deriv_r is None):
            raise ValueError("Too much info for k=1: bc_type can only be None.")
        x = _as_float_array(x, check_finite)
        t = np.r_[x[0], x, x[-1]]
        c = np.asarray(y)
        c = np.ascontiguousarray(c, dtype=_get_dtype(c.dtype))
        return BSpline.construct_fast(t, c, k, axis=axis)

    x = _as_float_array(x, check_finite)
    y = _as_float_array(y, check_finite)
    k = int(k)

    # come up with a sensible knot vector, if needed
    if t is None:
        if deriv_l is None and deriv_r is None:
            if k == 2:
                # OK, it's a bit ad hoc: Greville sites + omit
                # 2nd and 2nd-to-last points, a la not-a-knot
                t = (x[1:] + x[:-1]) / 2.
                t = np.r_[(x[0],)*(k+1),
                           t[1:-1],
                           (x[-1],)*(k+1)]
            else:
                t = _not_a_knot(x, k)
        else:
            t = _augknt(x, k)

    t = _as_float_array(t, check_finite)

    axis = axis % y.ndim
    y = np.rollaxis(y, axis)    # now internally interp axis is zero

    if x.ndim != 1 or np.any(x[1:] <= x[:-1]):
        raise ValueError("Expect x to be a 1-D sorted array_like.")
    if k < 0:
        raise ValueError("Expect non-negative k.")
    if t.ndim != 1 or np.any(t[1:] < t[:-1]):
        raise ValueError("Expect t to be a 1-D sorted array_like.")
    if x.size != y.shape[0]:
        raise ValueError('x and y are incompatible.')
    if t.size < x.size + k + 1:
        raise ValueError('Got %d knots, need at least %d.' %
                         (t.size, x.size + k + 1))
    if (x[0] < t[k]) or (x[-1] > t[-k]):
        raise ValueError('Out of bounds w/ x = %s.' % x)

    # Here : deriv_l, r = [(nu, value), ...]
    deriv_l = _convert_string_aliases(deriv_l, y.shape[1:])
    if deriv_l is not None:
        deriv_l_ords, deriv_l_vals = zip(*deriv_l)
    else:
        deriv_l_ords, deriv_l_vals = [], []
    deriv_l_ords, deriv_l_vals = np.atleast_1d(deriv_l_ords, deriv_l_vals)
    nleft = deriv_l_ords.shape[0]

    deriv_r = _convert_string_aliases(deriv_r, y.shape[1:])
    if deriv_r is not None:
        deriv_r_ords, deriv_r_vals = zip(*deriv_r)
    else:
        deriv_r_ords, deriv_r_vals = [], []
    deriv_r_ords, deriv_r_vals = np.atleast_1d(deriv_r_ords, deriv_r_vals)
    nright = deriv_r_ords.shape[0]

    # have `n` conditions for `nt` coefficients; need nt-n derivatives
    n = x.size
    nt = t.size - k - 1

    if nt - n != nleft + nright:
        raise ValueError("number of derivatives at boundaries.")

    # set up the LHS: the collocation matrix + derivatives at boundaries
    kl = ku = k
    ab = np.zeros((2*kl + ku + 1, nt), dtype=np.float_, order='F')
    _bspl._colloc(x, t, k, ab, offset=nleft)
    if nleft > 0:
        _bspl._handle_lhs_derivatives(t, k, x[0], ab, kl, ku, deriv_l_ords)
    if nright > 0:
        _bspl._handle_lhs_derivatives(t, k, x[-1], ab, kl, ku, deriv_r_ords,
                                offset=nt-nright)

    # set up the RHS: values to interpolate (+ derivative values, if any)
    extradim = prod(y.shape[1:])
    rhs = np.empty((nt, extradim), dtype=y.dtype)
    if nleft > 0:
        rhs[:nleft] = deriv_l_vals.reshape(-1, extradim)
    rhs[nleft:nt - nright] = y.reshape(-1, extradim)
    if nright > 0:
        rhs[nt - nright:] = deriv_r_vals.reshape(-1, extradim)

    # solve Ab @ x = rhs; this is the relevant part of linalg.solve_banded
    if check_finite:
        ab, rhs = map(np.asarray_chkfinite, (ab, rhs))
    gbsv, = get_lapack_funcs(('gbsv',), (ab, rhs))
    lu, piv, c, info = gbsv(kl, ku, ab, rhs,
            overwrite_ab=True, overwrite_b=True)

    if info > 0:
        raise LinAlgError("Collocation matix is singular.")
    elif info < 0:
        raise ValueError('illegal value in %d-th argument of internal gbsv' % -info)

    c = np.ascontiguousarray(c.reshape((nt,) + y.shape[1:]))
    return BSpline.construct_fast(t, c, k, axis=axis)


def make_lsq_spline(x, y, t, k=3, w=None, axis=0, check_finite=True):
    r"""Compute the (coefficients of) an LSQ B-spline.

    The result is a linear combination

    .. math::

            S(x) = \sum_j c_j B_j(x; t)

    of the B-spline basis elements, :math:`B_j(x; t)`, which minimizes

    .. math::

        \sum_{j} \left( w_j \times (S(x_j) - y_j) \right)^2

    Parameters
    ----------
    x : array_like, shape (m,)
        Abscissas.
    y : array_like, shape (m, ...)
        Ordinates.
    t : array_like, shape (n + k + 1,).
        Knots.
        Knots and data points must satisfy Schoenberg-Whitney conditions.
    k : int, optional
        B-spline degree. Default is cubic, k=3.
    w : array_like, shape (n,), optional
        Weights for spline fitting. Must be positive. If ``None``,
        then weights are all equal.
        Default is ``None``.
    axis : int, optional
        Interpolation axis. Default is zero.
    check_finite : bool, optional
        Whether to check that the input arrays contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
        Default is True.

    Returns
    -------
    b : a BSpline object of the degree `k` with knots `t`.

    Notes
    -----

    The number of data points must be larger than the spline degree `k`.

    Knots `t` must satisfy the Schoenberg-Whitney conditions,
    i.e., there must be a subset of data points ``x[j]`` such that
    ``t[j] < x[j] < t[j+k+1]``, for ``j=0, 1,...,n-k-2``.

    Examples
    --------
    Generate some noisy data:

    >>> x = np.linspace(-3, 3, 50)
    >>> y = np.exp(-x**2) + 0.1 * np.random.randn(50)

    Now fit a smoothing cubic spline with a pre-defined internal knots.
    Here we make the knot vector (k+1)-regular by adding boundary knots:

    >>> from scipy.interpolate import make_lsq_spline, BSpline
    >>> t = [-1, 0, 1]
    >>> k = 3
    >>> t = np.r_[(x[0],)*(k+1),
    ...           t,
    ...           (x[-1],)*(k+1)]
    >>> spl = make_lsq_spline(x, y, t, k)

    For comparison, we also construct an interpolating spline for the same
    set of data:

    >>> from scipy.interpolate import make_interp_spline
    >>> spl_i = make_interp_spline(x, y)

    Plot both:

    >>> import matplotlib.pyplot as plt
    >>> xs = np.linspace(-3, 3, 100)
    >>> plt.plot(x, y, 'ro', ms=5)
    >>> plt.plot(xs, spl(xs), 'g-', lw=3, label='LSQ spline')
    >>> plt.plot(xs, spl_i(xs), 'b-', lw=3, alpha=0.7, label='interp spline')
    >>> plt.legend(loc='best')
    >>> plt.show()

    **NaN handling**: If the input arrays contain ``nan`` values, the result is
    not useful since the underlying spline fitting routines cannot deal with
    ``nan``. A workaround is to use zero weights for not-a-number data points:

    >>> y[8] = np.nan
    >>> w = np.isnan(y)
    >>> y[w] = 0.
    >>> tck = make_lsq_spline(x, y, t, w=~w)

    Notice the need to replace a ``nan`` by a numerical value (precise value
    does not matter as long as the corresponding weight is zero.)

    See Also
    --------
    BSpline : base class representing the B-spline objects
    make_interp_spline : a similar factory function for interpolating splines
    LSQUnivariateSpline : a FITPACK-based spline fitting routine
    splrep : a FITPACK-based fitting routine

    """
    x = _as_float_array(x, check_finite)
    y = _as_float_array(y, check_finite)
    t = _as_float_array(t, check_finite)
    if w is not None:
        w = _as_float_array(w, check_finite)
    else:
        w = np.ones_like(x)
    k = int(k)

    axis = axis % y.ndim
    y = np.rollaxis(y, axis)    # now internally interp axis is zero

    if x.ndim != 1 or np.any(x[1:] - x[:-1] <= 0):
        raise ValueError("Expect x to be a 1-D sorted array_like.")
    if x.shape[0] < k+1:
        raise ValueError("Need more x points.")
    if k < 0:
        raise ValueError("Expect non-negative k.")
    if t.ndim != 1 or np.any(t[1:] - t[:-1] < 0):
        raise ValueError("Expect t to be a 1-D sorted array_like.")
    if x.size != y.shape[0]:
        raise ValueError('x & y are incompatible.')
    if k > 0 and np.any((x < t[k]) | (x > t[-k])):
        raise ValueError('Out of bounds w/ x = %s.' % x)
    if x.size != w.size:
        raise ValueError('Incompatible weights.')

    # number of coefficients
    n = t.size - k - 1

    # construct A.T @ A and rhs with A the collocation matrix, and
    # rhs = A.T @ y for solving the LSQ problem  ``A.T @ A @ c = A.T @ y``
    lower = True
    extradim = prod(y.shape[1:])
    ab = np.zeros((k+1, n), dtype=np.float_, order='F')
    rhs = np.zeros((n, extradim), dtype=y.dtype, order='F')
    _bspl._norm_eq_lsq(x, t, k,
                      y.reshape(-1, extradim),
                      w,
                      ab, rhs)
    rhs = rhs.reshape((n,) + y.shape[1:])

    # have observation matrix & rhs, can solve the LSQ problem
    cho_decomp = cholesky_banded(ab, overwrite_ab=True, lower=lower,
                                 check_finite=check_finite)
    c = cho_solve_banded((cho_decomp, lower), rhs, overwrite_b=True,
                         check_finite=check_finite)

    c = np.ascontiguousarray(c)
    return BSpline.construct_fast(t, c, k, axis=axis)

