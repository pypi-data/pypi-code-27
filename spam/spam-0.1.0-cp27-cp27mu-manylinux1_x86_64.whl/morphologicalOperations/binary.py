""" This module is a set of morphological operations using structural elements.
    It is based points operation on the full image and on permutations (that depends on the structural elements) of it (see mmodule shift_image) instead of a displacement of the structural element
    Works in 2D and 3D

"""
from __future__ import print_function

import os
import time
import numpy
import tifffile
import spam.helpers.imageManipulation as iman


# print level
# 0 warning an error
# 1 titles and times
# 2 details
prlv = 0


def dilation(im):
    """
    Apply a dilation on a binary 3D image
    """
    # Step 0: import as bool
    im = im.astype(bool)
    # Step 1: check type and dimension
    dim = len(im.shape)
    # Step 1: apply dilation                             #  x  y  z
    o_im = im  # 0  0  0
    o_im = o_im | iman.singleShift(im,  1, 0, False)  # 1  0  0
    o_im = o_im | iman.singleShift(im, -1, 0, False)   # -1  0  0
    o_im = o_im | iman.singleShift(im,  1, 1, False)  # 0  1  0
    o_im = o_im | iman.singleShift(im, -1, 1, False)  # 0 -1  0
    if dim == 3:
        o_im = o_im | iman.singleShift(im,  1, 2, False)  # 0  0  1
        o_im = o_im | iman.singleShift(im, -1, 2, False)  # 0  0 -1
    return numpy.array(o_im).astype('<u1')


def erosion(im):
    """
    Apply a erosion on a binary 3D image
    """
    # Step 1: apply erosion with dilation --> erosion = ! dilation( ! image )
    return numpy.logical_not(dilation(numpy.logical_not(im))).astype('<u1')


def morphologicalGradient(im):
    """
    Calculate the outer morphological gradient of an image (binary)
    """
    # Step 1: compute outer gradient
    return (numpy.logical_xor(dilation(im), im)).astype('<u1')


def sieving(im, n_voxel=1, save_tif=False, o_name=None):
    """
    Get rid of small objects.
    This function labels the object which can take times.
    """
    from scipy import ndimage
    TSTART = time.time()
    iman.prlv = prlv

    if prlv > 0:
        print('*** Welcome to the function: {}'.format(sieving.__name__))
    if prlv > 1:
        print('* Sieving for: {}'.format(n_voxel))
    if prlv > 1:
        print('*')

    # Step 1: Read the image
    im, i_name = iman.return_array_if_tif(im)

    # Step 2: Find the objects and their sizes
    if prlv > 1:
        print('* Labelling the objects')
    lbl, nlbl = ndimage.label(im)
    lbls = numpy.arange(1, nlbl+1)
    if prlv > 1:
        print('* Calculating the sizes of the objects')
    sizes = ndimage.sum(im, lbl, range(1, nlbl+1))

    # Step 3: Sieving the image
    if prlv > 1:
        print('* Sieving the image')
    # sieve = numpy.where(sizes>n_voxel)[0] + 1
    sieve = lbls
    sieve = sieve[(sizes > n_voxel)]
    sieve_index = numpy.zeros(nlbl + 1, numpy.uint8)
    sieve_index[sieve] = 1
    sieved_im = sieve_index[lbl]

    # Step 4: Save the image
    if save_tif:
        if prlv > 1:
            print('* Save image')
        if o_name is None:
            root, ext = os.path.splitext(i_name)
            o_name = '{r}_s{s}{e}'.format(r=root, s=n_voxel, e=ext)
        tifffile.imsave(o_name, sieved_im)
        if prlv > 1: print( '* Save image' )
    if o_name is None:
        root, ext = os.path.splitext(i_name)
        o_name = '{r}_s{s}{e}'.format(r=root, s=n_voxel, e=ext)
        tifffile.imsave(o_name, sieved_im)
    TEND = time.time()
    if prlv > 1:
        print('*')
    if prlv > 0:
        print('*** You spent {:.2f} seconds in {fname}. See you soon.'.format(
            TEND - TSTART, fname=sieving.__name__))
    return sieved_im


def _binary_reconstruction_from_edges(im, dmax=0):
    """
    Calculate the morphological reconstruction of an image (binary) with the edges of a CUBE as a marker!
    PARAMETERS:
    - im (3D numpy.array): The input image (binary)
    - dmax (int): the maximum geodesic distance. If zero, the reconstruction is complete.
    RETURNS:
    - (3D numpy.array): The reconstructed image
    TODO:
    - Consider mask for other geometry than cube
    #- Consider different marker than the edges (for example, two opposite faces for percolation test)
    HISTORY:
    2016-04-21 (Sun Yue): First version of the function
    """
    # Step 1: compute marker
    size = im.shape[0]
    bord = numpy.zeros((size, size, size), dtype=bool)
    bord[0, :, :] = im[0, :, :]
    bord[-1, :, :] = im[-1, :, :]
    bord[:, 0, :] = im[:, 0, :]
    bord[:, -1, :] = im[:, -1, :]
    bord[:, :, 0] = im[:, :, 0]
    bord[:, :, -1] = im[:, :, -1]

    # Step 2: first dilation and intersection
    temp1 = (dilation(bord)) & (im)
    temp2 = temp1
    temp1 = (dilation(temp2)) & (im)
    distance = 1

    if dmax == 0:
        dmax = 1e99  # perform complete reconstruction
    while ((not(numpy.array_equal(temp1, temp2))) & (distance < dmax)):
        temp2 = temp1
        temp1 = (dilation(temp2)) & (im)
        distance += 1
        print('distance =', distance)

    return temp1  # send the reconstructed image


def reconstructionFromEdges(im, dmax=0):
    """
    Calculate the morphological reconstruction of an image (binary) with the edges of a CUBE as a marker!
    PARAMETERS:
    - im (3D numpy.array): The input image (binary)
    - dmax (int): the maximum geodesic distance. If zero, the reconstruction is complete.
    RETURNS:
    - (3D numpy.array): The reconstructed image
    TODO:
    - Consider mask for other geometry than cube
    - Consider different marker than the edges (for example, two opposite faces for percolation test)
    HISTORY:
    2016-04-21 (Sun Yue): First version of the function
    """
    # Step 1: compute marker
    size = im.shape[0]
    bord = numpy.zeros((size,size,size),dtype = bool)
    bord[0,:,:] = im[0,:,:]
    bord[-1,:,:] = im[-1,:,:]
    bord[:,0,:] = im[:,0,:]
    bord[:,-1,:] = im[:,-1,:]
    bord[:,:,0] = im[:,:,0]
    bord[:,:,-1] = im[:,:,-1]

    # Step 2: first dilation and intersection
    temp1 = (dilation(bord))&(im)
    temp2 = temp1
    temp1 = (dilation(temp2))&(im)
    distance = 1

    if dmax == 0:
        dmax=1e99 # perform complete reconstruction
    while ((not(numpy.array_equal(temp1,temp2)))&(distance<dmax)):
        temp2 = temp1
        temp1 = (dilation(temp2))&(im)
        distance += 1
        print( 'distance =',distance )

    return temp1 # send the reconstructed image

def reconstructionFromOppositeFaces(im, dmax=0):
    """
    Calculate the morphological reconstruction of an image (binary) with two opposite faces of a CUBE as a marker!
    PARAMETERS:
    - im (3D numpy.array): The input image (binary)
    - dmax (int): the maximum geodesic distance. If zero, the reconstruction is complete.
    RETURNS:
    - (3D numpy.array): The reconstructed image
    TODO:
    - Consider mask for other geometry than cube
    HISTORY:
    2016-04-25 (JB colliat): First version of the function
    """
    # Step 1: compute marker
    size = im.shape[0]
    bord = numpy.zeros((size, size, size), dtype=bool)
    bord[0, :, :] = im[0, :, :]
    bord[-1, :, :] = im[-1, :, :]

    # Step 2: first dilation and intersection
    temp1 = (dilation(bord)) & (im)
    temp2 = temp1
    temp1 = (dilation(temp2)) & (im)
    distance = 1

    if dmax == 0:
        dmax = 1e99  # perform complete reconstruction
    while ((not(numpy.array_equal(temp1, temp2))) & (distance < dmax)):
        temp2 = temp1
        temp1 = (dilation(temp2)) & (im)
        distance += 1
        print('distance =', distance)

    return temp1  # send the reconstructed image
