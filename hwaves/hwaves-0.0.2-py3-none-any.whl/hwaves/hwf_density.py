import os

import numpy as np
from scipy import special
from scipy.special import sph_harm 
from scipy.special import genlaguerre 
from scipy.misc import factorial as fact

from .hwf import real_wf_xyz, psi_xyz, radial_wf, bohr_rad_A, elec_mass_amu

def real_wf_cartesian_density(designation,nx,ny,nz,dx,dy,dz,Z=1,N_neut=0):
    vol = dx * dy * dz
    x_grid, y_grid, z_grid = voxel_center_grid(nx,ny,nz,dx,dy,dz)
    psi_cart = real_wf_xyz(designation,x_grid,y_grid,z_grid,Z,N_neut)
    P_cart = np.array(np.abs(psi_cart*np.conj(psi_cart)),dtype=float)
    # multiply by voxel volume
    PV_cart = np.array(P_cart*vol,dtype=float)
    return x_grid, y_grid, z_grid, PV_cart

def cartesian_density(n,l,m,nx,ny,nz,dx,dy,dz,Z=1,N_neut=0):
    vol = dx * dy * dz
    x_grid, y_grid, z_grid = voxel_center_grid(nx,ny,nz,dx,dy,dz)
    psi_cart = psi_xyz(n,l,m,x_grid,y_grid,z_grid,Z,N_neut)
    # evaluate at voxel center
    P_cart = np.array(np.abs(psi_cart*np.conj(psi_cart)),dtype=float)
    # multiply by voxel volume
    PV_cart = np.array(P_cart*vol,dtype=float)
    return x_grid, y_grid, z_grid, PV_cart

def voxel_center_grid(nx,ny,nz,dx,dy,dz):
    x = np.arange(nx)*dx - (nx-1)*dx/2
    y = np.arange(ny)*dy - (ny-1)*dy/2
    z = np.arange(nz)*dz - (nz-1)*dz/2
    xabs = np.abs(x)
    yabs = np.abs(y)
    zabs = np.abs(z)
    x_grid, y_grid, z_grid = np.meshgrid(xabs,yabs,zabs)
    return x_grid, y_grid, z_grid

def spherical_density(n,l,m,r_max_A=3,nr=100,ntheta=72,nphi=36,Z=1,N_neut=0):

    dtheta = 360./ntheta
    dphi = 180./nphi
    r_step_A = float(r_max_A)/nr 

    # these arrays define the voxel centers
    th_deg = np.arange(float(dtheta)/2,360,dtheta)
    ph_deg = np.arange(float(dphi)/2,180,dphi)
    r_A = np.arange(float(r_step_A)/2,r_max_A,r_step_A)

    # various conversions etc
    th_rad = th_deg*np.pi/180 
    ph_rad = ph_deg*np.pi/180
    th_grid, ph_grid = np.meshgrid(th_rad,ph_rad)
    r_a0 = r_A/bohr_rad_A   
    Zr_A = Z*r_A
    Zr_a0 = Z*r_a0          
    Zr_step_A = Z*r_step_A
    
    # generalized laguerre poly for n,l:
    lagpoly = genlaguerre(n-l-1,2*l+1)
    # evaluate this at r
    lag_of_r = lagpoly(2*Zr_a0/n)

    # bohr_rad_A has units of Angstrom --> Rnl has units of Angstrom^(-3/2)
    Rnl = radial_wf(n,l,r_A,Z,N_neut)
    #Rnl = np.array(
    #np.sqrt( (2*Z/float(n*bohr_rad_A))**3 * fact(n-l-1) / (2*n*fact(n+l)) )
    #* np.exp(-1*Zr_a0/n)
    #* (2*Zr_a0/n)**l 
    #* lag_of_r
    #)

    # spherical harmonic for m,l:
    Ylm = sph_harm(m,l,th_grid,ph_grid)
   
    # total wavefunction: psi(r,theta,psi) = Rnl(r)*Ylm(theta,psi)
    psi = np.zeros(shape=(len(r_A),len(th_deg),len(ph_deg)),dtype=complex) 
    V_r_th_ph = np.zeros(shape=(len(r_A),len(th_deg),len(ph_deg)),dtype=float) 
    for ir in range(len(r_A)):
        psi[ir,:,:] = Ylm.T * Rnl[ir]
        Zri_center = Zr_A[ir]
        V_r_th_ph[ir,:,:] = float(4)/3*np.pi*((Zri_center+Zr_step_A/2)**3 - (Zri_center-Zr_step_A/2)**3) \
                            * np.ones(shape=(len(th_deg),len(ph_deg)),dtype=float)

    P_spherical = np.array(np.abs(psi*np.conj(psi)),dtype=float)
    PV_spherical = np.array(P_spherical*V_r_th_ph,dtype=float)

    return 

    r_th_ph_PV = []
    for ir,ri in enumerate(r_A):
        for ith,thi in enumerate(th_deg):
            for iph,phi in enumerate(ph_deg):
                r_th_ph_PV.append([ri,thi,phi,PV_spherical[ir,ith,iph]]) 
    return r_th_ph_PV

def pack_cartesian_data(x_grid,y_grid,z_grid,PV):
    ijk_xyz_PV = []
    for ix,xi in enumerate(x_grid[0,:,0]):
        for iy,yi in enumerate(y_grid[:,0,0]):
            for iz,zi in enumerate(z_grid[0,0,:]):
                ijk_xyz_PV.append([ix,iy,iz,xi,yi,zi,PV[ix,iy,iz]])
    return ijk_xyz_PV

def write_cartesian(ijk_xyz_PV,fpath):
    np.savetxt(
        fpath,
        np.array(ijk_xyz_PV),
        fmt='%i, %i, %i, %.3e, %.3e, %.3e, %.12e',
        header='ix, iy, iz, x [A], y [A], z [A], PV [e]'
        )

def write_radial_wf(r_A,Rnl,Rnlsqr,Pnl,fpath):
    np.savetxt(
        fpath,
        np.array([r_A,Rnl,Rnlsqr,Pnl]).T,
        fmt='%f, %.5e, %.5e, %.5e',
        header='r [A], Rnl [A^(-3/2)], Rnl**2 [A**-3], Pnl [A**-1]'
        )

