import numpy
import spam.helpers


def greyDilation(im, nBytes=1):
    """
    This function apply a dilation on a grey scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)

    Returns
    --------
        numpy array
            The dilated image
    """
    # Step 1: check type and dimension
    dim = len(im.shape)
    # Step 2: Determine substitution value
    sub = 2**(8*nBytes)-1
    # Step 3: apply dilation                                             #  x  y  z
    outputIm = im  # 0  0  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im,  1, 0, sub=sub))  # 1  0  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, -1, 0, sub=sub))  # -1  0  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im,  1, 1, sub=sub))  # 0  1  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, -1, 1, sub=sub))  # 0 -1  0
    if dim == 3:
        outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im,  1, 2, sub=sub))  # 0  0  1
        outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, -1, 2, sub=sub))  # 0  0 -1
    return outputIm


def greyErosion(im, nBytes=1):
    """
    This function apply a erosion on a grey scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)

    Returns
    --------
        numpy array
            The eroded image
    """
    # Step 1: check type and dimension
    dim = len(im.shape)
    # Step 2: Determine substitution value
    sub = 2**(8*nBytes)-1
    # Step 1: apply erosion                                                       #  x  y  z
    outputIm = im  # 0  0  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im,  1, 0, sub=sub))  # 1  0  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, -1, 0, sub=sub))  # -1  0  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im,  1, 1, sub=sub))  # 0  1  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, -1, 1, sub=sub))  # 0 -1  0
    if dim == 3:
        outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im,  1, 2, sub=sub))  # 0  0  1
        outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, -1, 2, sub=sub))  # 0  0 -1
    return outputIm


def greyMorphologicalGradient(im, nBytes=1):
    """
    This function apply a erosion on a grey scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)

    Returns
    --------
        numpy array
            The morphologycal gradient of the image
    """
    return (greyDilation(im, nBytes=nBytes) - im)
