""" 
    Last modification: 2016-03-11 (ER)
    This module is a set of morphological operations using structural elements.
    It is based points operation on the full image and on permutations (that depends on the structural elements) of it instead of a displacement of the structural element
    Works in 2D and 3D

"""

import os, time, numpy, tifffile
import spam.helpers.imageManipulation as iman


# print level
# 0 warning an error
# 1 titles and times
# 2 details
prlv = 2

def dilation( im ):
    """
    This function apply a dilation on a grey scale image      

    Parameters
    -----------
        im : 3D numpy.array
            The input image (binary)

    Returns
    --------
        o_im : numpy.array
            the dilated image
    """
    #History
    #2016-03-24 (JBC): First version of the function    
    #2016-04-11 (ER): add 2D

    # Step 1: check type and dimension
    dim = len( im.shape )
    # Step 2: apply dilation                                             #  x  y  z
    o_im = im                                                            #  0  0  0
    o_im = numpy.maximum( o_im, iman.singleShift( im,  1, 0 ) )  #  1  0  0
    o_im = numpy.maximum( o_im, iman.singleShift( im, -1, 0 ) )  # -1  0  0
    o_im = numpy.maximum( o_im, iman.singleShift( im,  1, 1 ) )  #  0  1  0
    o_im = numpy.maximum( o_im, iman.singleShift( im, -1, 1 ) )  #  0 -1  0
    if dim==3:
        o_im = numpy.maximum( o_im, iman.singleShift( im,  1, 2 ) )  #  0  0  1
        o_im = numpy.maximum( o_im, iman.singleShift( im, -1, 2 ) )  #  0  0 -1
    return o_im

def erosion( im, nbytes = 1 ):
    """
    This function apply an erosion on a grey scale image      
    PARAMETERS:
    - im (3D numpy.array): The input image (binary)      
    RETURNS:
    - o_im (numpy.array): the eroded image
    HISTORY:
    2016-03-24 (JBC): First version of the function    
    2016-04-11 (ER): add 2D
    """    
    # Step 1: check type and dimension
    dim = len( im.shape )
    # Step 2: Determine substitution value
    sub = 2**(8*nbytes)-1
    # Step 1: apply erosion                                                       #  x  y  z
    o_im = im                                                                     #  0  0  0
    o_im = numpy.minimum( o_im, iman.singleShift( im,  1, 0, sub=sub ) )  #  1  0  0
    o_im = numpy.minimum( o_im, iman.singleShift( im, -1, 0, sub=sub ) )  # -1  0  0
    o_im = numpy.minimum( o_im, iman.singleShift( im,  1, 1, sub=sub ) )  #  0  1  0
    o_im = numpy.minimum( o_im, iman.singleShift( im, -1, 1, sub=sub ) )  #  0 -1  0
    if dim==3:
        o_im = numpy.minimum( o_im, iman.singleShift( im,  1, 2, sub=sub ) )  #  0  0  1
        o_im = numpy.minimum( o_im, iman.singleShift( im, -1, 2, sub=sub ) )  #  0  0 -1
    return o_im

def morphologicalGradient( im ):
    """
    Calculate the outer morphological gradient of an image (grey)
    PARAMETERS:
    - im (3D numpy.array): The input image (grey)      
    RETURNS:
    - o_im (3D numpy.array): The gradient
    TODO:
    - Add inner and total gradients
    HISTORY:
    2016-03-22 (Sun Yue): First version of the function
    2017-07-25 (ER): Changed binary_dilation(im) to grey()
    """ 
    # Step 1: compute outer gradient
    return ( dilation(im) - im ) 
      
    
