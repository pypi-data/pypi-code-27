""" Last modification: 2016-04-07 (ER)
This module gives the Expected values of the Lipschitz-Killing Curvatures E(LKC)
in the context of excursion sets of correlated Ranfom Fields

It comes with a bunch a handy functions to compute them
"""
from __future__ import print_function
import os
import time
import numpy as np
from scipy.constants import pi
# from __future__ import print_function

#from math import sqrt
prlv = 0


def expectedMesures(kappa, j, n, hs='tail', dtype='gauss', mu=0.0, std=1.0, ctype='gauss', lc=1.0, nu=2.0, a=1.0):
    """
    Compute the Lipschitz-Killing Curvatures E(LKC)

    Parameters
    -----------
        kappa : float or list
            value of the threshold
        j : int
            number of the functionnal
        n : int
            spatial dimension
        hs : string
            the hitting set
        dtype : string
            type of distribution (see gmfGaussian)
        mu : float
            mean value of the distribution
        std : float
            standard deviation of the distribution
        ctype : string
            type of correlation function
        lc : float
            correlation length 
        nu : float
            parameter used for ctype='matern'
        a : float or list of floats
            size(s) of the object
            if float, the object is considered as a cube

    Returns
    --------
        mink : same type as kappa)
            the Gaussian Minkowski functionnal
    """
    # HISTORY:
    # 2016-04-08: First version of the function
    #

    e = 0.0*kappa
    # compute second spetral moment
    lam2 = secondSpectralMoment(std, lc, ctype=ctype, nu=nu)
    # loop over i
    if prlv > 5:
        print('IN ELKC: n = {}, j = {}'.format(n, j))
    for i in range(n-j+1):
        if prlv > 5:
            print('\t\ti = {}'.format(i))
        # comute LKC of the cube
        lkc = lkcParallelepiped(i+j, n, a)
        # compute GMF
        gmf = gmfGaussian(kappa, i, hs=hs, dtype=dtype, mu=mu, std=std)
        # compute
        fla = flag(i+j, i)
        e = e + fla*lkc*gmf*(lam2/(2.0*pi))**(i/2.0)

    return e


def gmfGaussian(kappa, j, hs='tail', dtype='gauss', mu=0.0, std=1.0):
    """
    Compute the Gaussian Minkowski functionals j

    Parameters
    -----------
        kappa : float or list
            value of the threshold
        j : int
            number of the functionnal
        hs : string
            the hitting set
        dtype : string
            type of distribution (see gmfGaussian)
            implemented: dtype='gauss' and dtype='log'
        mu : float
            mean value of the distribution
        std : float
            standard deviation of the distribution

    Returns
    --------
        mink : same type as kappa
            the Gaussian Minkowski functionnal
    """
    # HISTORY:
    # 2016-04-08: First version of the function
    #

    from scipy.special import erf
    if hs == 'tail':
        sign = 1.0
    elif hs == 'cumu':
        sign = (-1.0)**(j+1)
    else:
        err = '### ERROR in {}: hitting set {} not implemented ###'.format(
            'gmf', hs)
        print('{d}\n{m}\n{d}'.format(m=err, d='#'*len(err)))
        return -1

    # STEP 2: change variable
    if dtype == 'gauss':
        k = (kappa - mu) / std
    elif dtype == 'log':
        k = (np.log(kappa) - mu) / std

    if j < 0:
        err = '### ERROR in {}: j should be >0. {} given. ###'.format('gmf', j)
        print('{d}\n{m}\n{d}'.format(m=err, d='#'*len(err)))
        return -1
    elif j == 0:
        mink = 0.5*(1.0 - sign*erf(k/2**0.5))
    else:
        mink = sign*np.exp(-k**2.0/2.0)*hermitePolynomial(k,
                                                          j-1) / (std**j * (2.0*pi)**0.5)
        #mink = - (k**3 - 3*k)*np.exp(-k**2.0/2.0) / (std**4*(2.0*pi)**0.5)

    return mink


def secondSpectralMoment(std, lc, ctype='gauss', nu=2.0):
    """
    Compute the second spectral moment for a given covariance function:

    .. math::
        lambda2 = d^2 C(h) / dh^2 |_{h=0} $$

    Parameters
    -----------
        std : float
            standard deviation
        lc : float
            correlation length
        ctype : string
            type of correlation function
        nu : float
            parameter used for ctype='matern'

    Returns
    --------
        lambda2 : float
            the second spectral moment
    """
    # HISTORY:
    # 2016-04-07 (ER): First version of the function
    #

    v = std**2.0
    if ctype == 'gauss':
        return 2.0*v/lc**2.0
    if ctype == 'matern':
        if nu <= 1:
            err = '### ERROR in {}: for matern class, nu should be > 1. {} given. ###'.format(
                'secondSpectralMoment', nu)
            print('{d}\n{m}\n{d}'.format(m=err, d='#'*len(err)))
            return -1

        return (v*nu) / (lc**2.0 * (nu-1.0))
    else:
        err = '### ERROR in {}: covariance function {} not implemented ###'.format(
            'secondSpectralMoment', ctype)
        print('{d}\n{m}\n{d}'.format(m=err, d='#'*len(err)))
        return -1
    return lambda2


def flag(n, j):
    """
    Compute the flag coefficients
    [ n, j ] = ( n, j ) w_n / w_{n-j}w_j    

    Parameters
    -----------
        n : int 
        j : int

    Returns
    --------
        flag : float
            [n , j]
    """
    # HISTORY:
    # 2016-04-07 (ER): First version of the function
    #

    from scipy.special import binom
    if j > n:
        err = '### ERROR in {}: n = {} < j = {} ###'.format('flag', n, j)
        print('{d}\n{m}\n{d}'.format(m=err, d='#'*len(err)))
        return -1
    vn = ballVolume(n)
    vj = ballVolume(j)
    vnj = ballVolume(n-j)
    return binom(n, j)*vn / (vnj*vj)


def hermitePolynomial(x, n):
    """
    Evaluate a x the probabilitic Hermite polynomial n
    PARAMETERS:
    - x (float): point of evaluation
    - n (int): number of Hermite polynomia
    RETURNS:
    - h (float): He_n(x) the value of the polynomial
    HISTORY:
    2016-04-07 (ER): First version of the function    
    """
    from numpy.polynomial.hermite_e import hermeval
    coefs = [0]*(n+1)
    coefs[n] = 1
    return hermeval(x, coefs)


def ballVolume(n, r=1.0):
    """
    Compute the volume of the ball
    PARAMETERS:
    - n (int): spatial dimension
    - r (float): radius of the ball
    RETURNS:
    - w (float): volume of the unit ball
    HISTORY:
    2016-04-07 (ER): First version of the function    
    """
    from scipy.special import gamma
    return float(r)**float(n)*pi**(0.5*n) / gamma(1.0+0.5*n)


def lkcParallelepiped(i, n, a):
    """
    Compute the LKC for parallelepiped

    Parameters
    -----------
        i : int
            number of the LKC. 0 <= i <= n
        n : int
            spatial dimension
        a : float or list of float
            size(s) of the object
            if float, the object is considered as a cube

    Returns
    --------
        lkc : float
            the LKC
    """
    # HISTORY:
    # 2016-04-07 (ER): First version of the function
    #

    from scipy.special import binom
    #from scipy.spatial.distance import pdist
    # test if i > n
    # print "LKC {} in dim {} for size {}".format( i, n, a )
    if i > n or i < 0:
        err = '### ERROR in {}: lkc {} does not exist in {} dimensions ###'.format(
            'lkcParallelepiped', i, n)
        print('{d}\n{m}\n{d}'.format(m=err, d='#'*len(err)))
        return -1
    if isinstance(a, (int, float)):  # cube
        # general formula for every i and n
        lkc = binom(n, i)*a**i
        return lkc
    else:  # para
        # check if a is well defined
        if len(a) != n:
            err = '### ERROR in {}: size of a should be equal to n ###'.format(
                'lkcParallelepiped')
            print('{d}\n{m}\n{d}'.format(m=err, d='#'*len(err)))
            return -1
        # 2D
        if n == 2:
            switcher = {
                0: 1,
                1: a[0] + a[1],
                2: a[0]*a[1],
            }
            return switcher.get(i, -1)
        # 3D
        elif n == 3:
            switcher = {
                0: 1,
                1: a[0] + a[1] + a[2],
                2: a[0]*a[1] + a[0]*a[2] + a[2]*a[1],
                3: a[0]*a[1]*a[2],
            }
            return switcher.get(i, -1)
        else:
            err = '### ERROR in {}: {} dimension is not implemented for para ###'.format(
                'lkcParallelepiped')
            print('{d}\n{m}\n{d}'.format(m=err, d='#'*len(err)))
            return -1


def phi(x, s):
    return np.exp(-x**2/2.0)/(s*np.sqrt(2.0*pi))


def bigPhi(x, s):
    from scipy.special import erf, erfc
    return phi(x, s) - 0.5*x*(1.0+erf(-x/np.sqrt(2.0)))


def expectedMesuresLinearThreshold(alpha, beta, j, n, hs='tail', dtype='gauss', mu=0.0, std=1.0, ctype='gauss', lc=1.0, nu=2.0, a=1.0):
    """
    Compute the Lipschitz-Killing Curvatures E(LKC)

    Parameters
    -----------
        kappa : float or list
            value of the threshold
        j : int
            number of the functionnal
        n : int
            spatial dimension
        hs : string
            the hitting set
        dtype : string
            type of distribution (see gmfGaussian)
        mu : float
            mean value of the distribution
        std : float
            standard deviation of the distribution
        ctype : string
            type of correlation function
        lc : float
            correlation length 
        nu : float
            parameter used for ctype='matern'
        a : float or list of floats
            size(s) of the object
            if float, the object is considered as a cube

    Returns
    --------
        mink : same type as kappa
            the Gaussian Minkowski functionnal
    """
    # HISTORY:
    # 2016-04-08: First version of the function
    #

    e = 0.0*alpha
    # compute second spetral moment
    lam2 = secondSpectralMoment(std, lc, ctype=ctype, nu=2.0)
    # loop over i
    # if prlv>5: print 'IN ELKC: n = {}, j = {}'.format( n, j )
    # for i in range( n-j+1 ):
    #    if prlv>5: print '\t\ti = {}'.format( i )
    #    # comute LKC of the cube
    #    lkc = lkcParallelepiped( i+j, n, a )
    #    # compute GMF
    #    gmf = gmfGaussianLinearThreshold( alpha, beta, a, i, hs=hs, lam2=lam2 )

    #    # compute
    #    fla = flag( i+j , i )
    #    e = e + fla*gmf*lkc*( lam2/(2.0*pi) )**(i/2.0)

    e = 0.0
    if n == 1:
        from scipy.special import erf, erfc
        cstA = alpha*a/(np.sqrt(2.0)*std)
        cstB = beta/(np.sqrt(2.0)*std)
        cstAB = cstA+cstB

        # intOfMo = (( np.sqrt(2.0/pi) * std * ( np.exp(-cstAB**2.0) - np.exp(-cstB**2) ) + (alpha*a+beta) * erf(cstAB) - beta*erf(cstB) )/(2.0*alpha) + 0.5*a) # tail
        intOfMo = ((np.sqrt(2.0/pi) * std * (-np.exp(-cstAB**2.0) + np.exp(-cstB**2)) +
                    (alpha*a) * erfc(cstAB) - beta*erf(cstAB) + + beta*erf(cstB))/(2.0*alpha))  # cumu

        if j == 1:
            e = intOfMo
        elif j == 0:
            c = np.sqrt(lam2) * bigPhi(alpha/(np.sqrt(lam2)*std), std)
            intOfUpCrossed = c * (erf(cstAB) - erf(cstB))/(2.0*alpha)

            e = intOfMo/a + intOfUpCrossed
        else:
            print("ELKC not implemented for n={} and j={}-> exiting".format(n, j))

    else:
        print("ELKC not implemented for n={} -> exiting".format(n))

    return e


def gmfGaussianLinearThreshold(alpha, beta, a, j, hs='tail', dtype='gauss', mu=0.0, std=1.0, lam2=1.0):
    """
    Compute the Gaussian Minkowski functionals j

    Parameters
    -----------
        kappa : float or list
            value of the threshold
        j : int
            number of the functionnal
        hs : string
            the hitting set
        dtype : string
            type of distribution (see gmfGaussian)
            implemented: dtype='gauss' and dtype='log'
        mu : float
            mean value of the distribution
        std : float
            standard deviation of the distribution

    Returns:
        mink : same type as kappa
            the Gaussian Minkowski functionnal
    """
    # HISTORY:
    # 2016-04-08: First version of the function
    #

    from scipy.special import erf, erfc
    cstA = alpha*a/(np.sqrt(2.0)*std)
    cstB = beta/(np.sqrt(2.0)*std)
    cstAB = cstA+cstB

    if j == 0:
        if hs == 'tail':
            mink = ((np.sqrt(2.0/pi) * std * (np.exp(-cstAB**2.0) - np.exp(-cstB**2)) +
                     (alpha*a+beta) * erf(cstAB) - beta*erf(cstB))/(2.0*alpha) + 0.5*a)/a
        elif hs == 'cumu':
            mink = ((np.sqrt(2.0/pi) * std * (-np.exp(-cstAB**2.0) + np.exp(-cstB**2)) +
                     (alpha*a) * erfc(cstAB) - beta*erf(cstAB) + + beta*erf(cstB))/(2.0*alpha))/a

    elif j == 1:
        if hs == 'tail':
            mink = (erf(cstAB)-erf(cstB))/(2*alpha*a)
        elif hs == 'cumu':
            x = alpha/(np.sqrt(lam2)*std)
            mink = (erf(cstAB)-erf(cstB))/(2*alpha*a) * bigPhi(x, std)
    else:
        print("Error GMF not implemented", j)
        exit()
    return mink
