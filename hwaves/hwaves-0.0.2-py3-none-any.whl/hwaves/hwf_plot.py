import os

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#from mayavi import mlab
from skimage import measure

from .hwf import spherical_harmonic, radial_probability
from .hwf_density import real_wf_cartesian_density, cartesian_density

bohr_rad_A = 0.529177       #Angstrom
elec_mass_amu = 5.485799090 #amu

def plot_spherical_harmonic(l,m,th,ph,showplot=False):
    #
    # th and ph can be meshgrids
    #
    Ylm = spherical_harmonic(l,m,th,ph)
    sph_amp = np.abs(Ylm * np.conj(Ylm))
    #sph_amp = np.real(Ylm)
    x_amp = sph_amp * np.sin(ph) * np.cos(th)
    y_amp = sph_amp * np.sin(ph) * np.sin(th)
    z_amp = sph_amp * np.cos(ph)
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.plot_surface(x_amp, y_amp, z_amp,
    rstride=1, cstride=1, cmap=plt.get_cmap('jet'),
    linewidth=0, antialiased=False, alpha=0.5)
    if showplot:
        plt.show()
    return fig

def plot_radial_wf(n,l,r_A,Z=1,N_neut=0,showplot=False):
    #
    # r_A is an array
    #
    Rnl,Rnlsqr,Pnl = radial_probability(n,l,r_A,Z,N_neut)

    fig = plt.figure()
    ax = fig.gca()
    ax.plot(Z*r_A,Rnl)
    ax.set_xlabel('Z*r (Angstrom)')
    ax.set_ylabel('Rnl')

    fig = plt.figure()
    ax = fig.gca()
    ax.plot(Z*r_A,Rnlsqr)
    ax.set_xlabel('Z*r (Angstrom)')
    ax.set_ylabel('Rnl**2')

    fig = plt.figure()
    ax = fig.gca()
    ax.plot(Z*r_A,Pnl)
    ax.set_xlabel('Z*r (Angstrom)')
    ax.set_ylabel('Pnl')

    if showplot:
        plt.show()
    return fig

    #nx = 80
    #ny = 80
    #nz = 80
    #dx = 0.2
    #dy = 0.2
    #dz = 0.2

def plot_isosurface(n,l,m,nx,ny,nz,dx,dy,dz,isolevel=None,Z=1,N_neut=0,showplot=False):
    x_grid,y_grid,z_grid,PV = cartesian_density(n,l,m,nx,ny,nz,dx,dy,dz,Z,N_neut)
    if not isolevel:
        isolevel = 0.3*np.max(PV)
    make_isosurf(PV,isolevel,dx,dy,dz,showplot)

def plot_real_wf_isosurface(designation,nx,ny,nz,dx,dy,dz,isolevel=None,Z=1,N_neut=0,showplot=False):
    x_grid,y_grid,z_grid,PV = real_wf_cartesian_density(designation,nx,ny,nz,dx,dy,dz,Z,N_neut)
    if not isolevel:
        isolevel = 0.3*np.max(PV)
    make_isosurf(PV,isolevel,dx,dy,dz,showplot)

def make_isosurf(PV,isolevel,dx,dy,dz,showplot):
    verts, faces, norms, vals = measure.marching_cubes_lewiner(PV, isolevel, spacing=(dx,dy,dz))   
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(verts[:, 0], verts[:,1], faces, verts[:, 2], cmap='Spectral', lw=1)
    if showplot:
        plt.show()
    return fig

def plot_scatter():
    # TODO: take volumetric data, plot a 3d scatter
    pass




