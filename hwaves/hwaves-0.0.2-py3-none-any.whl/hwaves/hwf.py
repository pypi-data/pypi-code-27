import os

import numpy as np
from scipy.special import sph_harm 
from scipy.special import genlaguerre 
from scipy.misc import factorial as fact
#from masstable import Table
#import periodictable as pt

bohr_rad_A = 0.529177       #Angstrom
elec_mass_amu = 5.485799090 #amu

def spherical_harmonic(l,m,theta,phi):
    """Compute values of a spherical harmonic function.

    This is a direct wrapper around scipy.special.sph_harm,
    and you may as well just use that.

    Parameters
    ----------
    l : int
        Angular momentum quantum number
    m : int
        Magnetic quantum number
    theta : array
        Theta values (azimuthal spherical coordinates)
        at which the spherical harmonic will be computed
    phi : array
        Phi values (polar spherical coordinates)
        at which the spherical harmonic will be computed

    Returns
    -------
    Ylm : array
        Array of complex-valued spherical harmonics 
    """
    return sph_harm(m,l,theta,phi)

def radial_wf(n,l,r_A,Z=1,N_neut=0):
    """Get wavefunction values wrt radial distance from the nucleus.

    Parameters
    ----------
    n : int
        principal quantum number
    l : int
        angular momentum quantum number
    r_A : array of float
        array of radial points (in Angstroms)
        at which the wavefunction will be computed
    Z : int
        number of protons in the nucleus
    N_neut : int
        number of neutrons in the nucleus

    Returns
    ------- 
    Rnl : array
        array of complex wavefunction values
        at all of the input points `r_A`
    """
    
    # TODO: 
    # use nucmt to determine nuclear mass from Z+N
    # nucmt gives mass excess in energy units
    # M_nuc = Z + N + (mass_excess)/c^2
    #atmass = Get atomic mass of either most common or weighted-average isotope
    #nucmt = Table('AME2003')
    #mu = (reduced mass of nucleus-electron system, approx equal to m_e) 
    #a_mu = elec_mass_amu / mu * bohr_rad_A  
    a_mu = bohr_rad_A       # a_mu in units of Angstrom

    r_a_mu = r_A/a_mu       # radius in units of a_mu
    Zr_a_mu = Z*r_a_mu      # Z*r in units of a_mu

    # get generalized laguerre for n,l
    lagpoly = genlaguerre(n-l-1,2*l+1)
    lag_of_r = lagpoly(2*Zr_a_mu/n)

    # a_mu has units of Angstrom --> Rnl has units of Angstrom^(-3/2)
    Rnl = np.array(
    np.sqrt( (2*Z/float(n*a_mu))**3 * fact(n-l-1) / (2*n*fact(n+l)) )
    * np.exp(-1*Zr_a_mu/n)
    * (2*Zr_a_mu/n)**l 
    * lag_of_r)

    return Rnl

def radial_density(n,l,r_A,Z=1,N_neut=0):
    Rnl = radial_wf(n,l,r_A,Z,N_neut)
    # Rnl has units of Angstrom^(-3/2)
    # Rnlsqr has units Angstrom^(-3): density per volume 
    return Rnl, Rnl * Rnl

def radial_probability(n,l,r_A,Z=1,N_neut=0):   
    Rnl, Rnlsqr = radial_density(n,l,r_A,Z,N_neut)
    # Rnlsqr has units Angstrom^(-3): density per volume 
    # Pnl has units Angstrom^(-1): spherical-shell integrated density per radius
    Pnl = Rnlsqr * 4 * np.pi * r_A**2  
    return Rnl, Rnlsqr, Pnl

def radial_wf_integral(n,l,r_A,Z=1,N_neut=0):
    Rnl, Rnlsqr, Pnl = radial_probability(n,l,r_A,Z,N_neut)
    return np.sum(Pnl) * max(r_A) / len(r_A)

def psi_xyz(n,l,m,x_grid,y_grid,z_grid,Z=1,N_neut=0):
    lag = genlaguerre(n-l-1,2*l+1)
    r_grid = np.sqrt(x_grid**2+y_grid**2+z_grid**2)
    Zr_a0 = Z*r_grid/bohr_rad_A
    #lag_of_r = lag(2*Zr_a0/n)
    Rnl = radial_wf(n,l,r_grid,Z,N_neut)
    #Rnl = np.sqrt( (2*Z/float(n*bohr_rad_A))**3 * fact(n-l-1) / (2*n*fact(n+l)) ) \
    #        * np.exp(-1*Zr_a0/n) * (2*Zr_a0/n)**l * lag_of_r
    th_grid = np.arctan(y_grid/x_grid)
    ph_grid = np.arctan(np.sqrt(x_grid**2+y_grid**2)/z_grid)
    #th_grid, ph_grid = np.meshgrid(th,ph)
    Ylm = sph_harm(m,l,th_grid,ph_grid) 
    return Rnl * Ylm

def real_wf_xyz(designation,x_grid,y_grid,z_grid,Z=1,N_neut=0):
    wf_func = lambda n,l,m: psi_xyz(n,l,m,x_grid,y_grid,z_grid,Z,N_neut)
    if designation == '1s':
        return wf_func(1,0,0)
    if designation == '2s':
        return wf_func(2,0,0)
    if designation == '3s':
        return wf_func(3,0,0)
    if designation == '4s':
        return wf_func(4,0,0)
    if designation == '5s':
        return wf_func(5,0,0)
    if '2p' in designation:
        if designation == '2pz': return wf_func(2,1,0) 
        psi_211 = wf_func(2,1,1)  
        psi_21m1 = wf_func(2,1,-1)  
        if designation == '2px': return 1./np.sqrt(2) * (psi_211 + psi_21m1)
        if designation == '2py': return 1./(1j*np.sqrt(2)) * (psi_211 - psi_21m1)
    if '3p' in designation:
        if designation == '3pz': return wf_func(3,1,0) 
        psi_311 = wf_func(3,1,1)  
        psi_31m1 = wf_func(3,1,-1)  
        if designation == '3px': return 1./np.sqrt(2) * (psi_311 + psi_31m1)
        if designation == '3py': return 1./(1j*np.sqrt(2)) * (psi_311 - psi_31m1)
    if '4p' in designation:
        if designation == '4pz': return wf_func(4,1,0) 
        psi_411 = wf_func(4,1,1)  
        psi_41m1 = wf_func(4,1,-1)  
        if designation == '4px': return 1./np.sqrt(2) * (psi_411 + psi_41m1)
        if designation == '4py': return 1./(1j*np.sqrt(2)) * (psi_411 - psi_41m1)
    if '5p' in designation:
        if designation == '5pz': return wf_func(5,1,0) 
        psi_511 = wf_func(5,1,1)  
        psi_51m1 = wf_func(5,1,-1)  
        if designation == '5px': return 1./np.sqrt(2) * (psi_511 + psi_51m1)
        if designation == '5py': return 1./(1j*np.sqrt(2)) * (psi_511 - psi_51m1)
    if '3d' in designation:
        if designation == '3dz2': return wf_func(3,2,0) 
        if 'xz' in designation or 'yz' in designation:
            psi_321 = wf_func(3,2,1) 
            psi_32m1 = wf_func(3,2,-1)  
            if designation == '3dxz': return 1./np.sqrt(2) * (psi_321 + psi_32m1)
            if designation == '3dyz': return 1./(1j*np.sqrt(2)) * (psi_321 - psi_32m1)
        if 'xy' in designation or 'x2-y2' in designation:
            psi_322 = wf_func(3,2,2)  
            psi_32m2 = wf_func(3,2,-2)  
            if designation == '3dxy': return 1./np.sqrt(2) * (psi_322 + psi_32m2)
            if designation == '3dx2-y2': return 1./(1j*np.sqrt(2)) * (psi_322 - psi_32m2)
    if '4d' in designation:
        if designation == '4dz2': return wf_func(4,2,0) 
        if 'xz' in designation or 'yz' in designation:
            psi_421 = wf_func(4,2,1) 
            psi_42m1 = wf_func(4,2,-1)  
            if designation == '4dxz': return 1./np.sqrt(2) * (psi_421 + psi_42m1)
            if designation == '4dyz': return 1./(1j*np.sqrt(2)) * (psi_421 - psi_42m1)
        if 'xy' in designation or 'x2-y2' in designation:
            psi_422 = wf_func(4,2,2)  
            psi_42m2 = wf_func(4,2,-2)  
            if designation == '4dxy': return 1./np.sqrt(2) * (psi_422 + psi_42m2)
            if designation == '4dx2-y2': return 1./(1j*np.sqrt(2)) * (psi_422 - psi_42m2)
    if '4f' in designation:
        if designation == '4fz3': return wf_func(4,3,0) 
        if 'xz2' in designation or 'yz2' in designation:
            psi_431 = wf_func(4,3,1) 
            psi_43m1 = wf_func(4,3,-1)  
            if designation == '4fxz2': return 1./np.sqrt(2) * (psi_431 + psi_43m1)
            if designation == '4fyz2': return 1./(1j*np.sqrt(2)) * (psi_431 - psi_43m1)
        if 'xyz' in designation or 'z(x2-y2)' in designation:
            psi_432 = wf_func(4,3,2)  
            psi_43m2 = wf_func(4,3,-2)  
            if designation == '4fxyz': return 1./np.sqrt(2) * (psi_432 + psi_43m2)
            if designation == '4fz(x2-y2)': return 1./(1j*np.sqrt(2)) * (psi_432 - psi_43m2)
        if 'x(x2-3y2)' in designation or 'y(3x2-y2)' in designation:
            psi_433 = wf_func(4,3,3)  
            psi_43m3 = wf_func(4,3,-3)  
            if designation == '4fx(x2-3y2)': return 1./np.sqrt(2) * (psi_433 + psi_43m3)
            if designation == '4fy(3x2-y2)': return 1./(1j*np.sqrt(2)) * (psi_433 - psi_43m3)


