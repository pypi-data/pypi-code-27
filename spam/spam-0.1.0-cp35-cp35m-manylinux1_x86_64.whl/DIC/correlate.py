# 2017-05-29 ER and EA

# This is spam's DIC toolkit, but since we're in the tools/ directory we can import it directly
from __future__ import print_function
import spam.DIC._DICToolkit as DICToolkit

import numpy
numpy.set_printoptions(precision=3, suppress=True)

import scipy.ndimage
import tifffile

import spam.DIC.transformationOperator as transformationOperator
import spam.label.toolkit as ltk # for im1mask

""" Library of image correlation functions.
        These basic functions take two images acquired in the same modality and attempt
        to find a mapping between the two.
"""


def lucasKanade(im1, im2,
                im2mask=None,
                Finit=None, FinitBinRatio=1.0,
                margin=None,
                maxIterations=25, minFchange=0.001,
                interpolationOrder=1, interpolator='python',
                verbose=False,
                imShowProgress=None, imShowProgressNewFig=False):
    """ Perform subpixel image correlation between im1 and im2.

        This function will deform im1 until it best matches im2.
        The matching includes sub-pixel displacements, rotation, and linear straining of the whole image.
        The correlation of im1, im2 will give a transformationOperator F which maps im1 into im2.
        $$ im1(F.x) = im2(x) $$

        If im1 and im2 follow each other in time, then the resulting F is im1 -> im2 which makes sense in most cases.
        "Discrete correlation" can be performed by masking im1.

        im1 and im2 do not necessarily have to be the same size (`i.e.`, im1 can be bigger) -- this is good since there
        is a zone to accommodate movement. In the case of a bigger im2, im1 and im2 are centred with respect to each other.

        Parameters
        ----------

            im1 : 3D numpy array
                The greyscale image that will be deformed -- must not contain NaNs

            im2 : 3D numpy array
                The greyscale image that will not move -- must not contain NaNs

            im2mask : 3D boolean numpy array, optional
                A mask for the zone to correlate in im2 with `False` in the zone to not correlate.
                Default = None, `i.e.`, correlate all of im2 minus the margin.
                If this is defined, the F returned is in the centre of mass of the mask

            Finit : 4x4 numpy array, optional
                Initial transformation to apply. Default = numpy.eye(4), `i.e.`, no transformation
                This should be an F centred

            FinitBinRatio : float, optional
                Change translations in Finit, if it's been calculated on a differently-binned image. Default = 1

            margin : int, optional
                Margin, in pixels, to take in im1.
                Can also be a N-component list of ints, represeting the margin in ND.
                If im2 has the same size as im1 this is strictly necessary to allow space for interpolation and movement
                Default = None (`i.e.`, enough margin for a worse-case 45degree rotation with no displacement)

            maxIterations : int, optional
                Maximum number of quasi-Newton interations to perform before stopping. Default = 25

            minFchange : float, optional
                Smallest change in the norm of F (the transformation operator) before stopping. Default = 0.001

            interpolationOrder : int, optional
                Order of the greylevel interpolation for applying F to im1 when correlating. Reccommended value is 3, but you can get away with 1 for faster calculations. Default = 3

            interpolator : string, optional
                Which interpolation function to use from `spam`.
                Default = 'python'. 'C' is also an option

            verbose : bool, optional
                Get to know what the function is really thinking, recommended for debugging only. Default = False

            imShowProgress : String, optional (default = None)
                Pop up a window showing a ``imShowProgress`` slice of the image differences (im1-im2) as im1 is progressively deformed.
                Accepted options are "Z", "Y" and "X" -- the slicing direction.

            imShowProgressNewFig : bool, optional (defaul = False)
                Make a new plt.figure for each iteration

        Returns
        -------
        Dictionary containing:

            error : float
                    Error float describing mismatch between images

            transformation : "transformation" dictionary
                    Note this is not yet reclaculated with the correct centre of the image

            F : 4x4 float array
                transformation operator defined at 0,0,0

            Fcentre : 4x4 float array
                transformation operator at the centre of the image

            returnStatus : signed int
                Return status from the correlation:

                Keys:
                    2 : Achieved desired precision in the norm of delta F

                    1 : Hit maximum number of iterations while iterating

                    -1 : Error is more than 80% of previous error, we're probably diverging

                    -2 : Singular matrix M cannot be inverted

                    -3 : Displacement > 5*margin

            iterationNumber : int
                Number of iterations

            lastFchange : float
                Last norm of deltaF

        Note
        ----
        This correlation was written in the style of S. Roux (especially "An extension of Digital Image Correlation for intermodality image registration")
        especially equations 12 and 13.

        Since we're using classical DIC (without multimodal registration) there is no need to update the gradient image,
        so this is calculated once at the beginning.
    """
    # History:
    # 2018-03-20 EA: Trying to make margin a list of 3 values as z, y, x margins in order to try
    #   clean-ish 2D compatilibility

    # Explicitly set input images to floats
    im1 = im1.astype('<f4')
    im2 = im2.astype('<f4')

    # initialise exit clause for singular "M" matrices
    singular = False

    # Detect unpadded 2D image first:
    if len(im1.shape) == 2:
        # pad them
        im1 = im1[numpy.newaxis, ...]
        im2 = im2[numpy.newaxis, ...]
        if im2mask is not None:
            im2mask = im2mask[numpy.newaxis, ...]

    # Detect 2D images
    if im1.shape[0] == 1:
        twoD = True

        # Override interpolator for python in 2D
        interpolator = 'python'

        # Define masks for M and A in 2D since we'll ignore the Z components
        # Components of M and A which don't include Z
        twoDmaskA = numpy.zeros((12), dtype=bool)
        for i in [5, 6, 7, 9, 10, 11]:
            twoDmaskA[i] = True

        twoDmaskM = numpy.zeros((12, 12), dtype=bool)
        for y in range(12):
            for x in range(12):
                if twoDmaskA[y] and twoDmaskA[x]:
                    twoDmaskM[y, x] = True

    else:
        twoD = False

    # Automatically calculate margin if none is passed
    # Detect default case and calculate maring necessary for a 45deg rotation with no displacement
    if margin is None:
        # sqrt
        margin = [int((3**0.5 - 1.0) * max(im1.shape)*0.5)]*3
    elif type(margin) == list:
        pass
    else:
        # Make sure margin is an int
        margin = int(margin)
        margin = [margin]*3

    # Make sure im1 is bigger than im2 and check difference in size
    # Get difference in image sizes. This should be positive, since we must always have enough data for im1 interpolation
    im1im2sizeDiff = numpy.array(im1.shape) - numpy.array(im2.shape)

    # 2018-05-15 OS and EA: apply F in the COM of the mask by default
    #if im1mask is not None:
        ## calculate the centre of mass of the mask
        #im1Centre = ltk.getCentresOfMass( im1mask )[1]
    #else:
        ## there is not mask, just take the centre of the image.
    #im1Centre = (numpy.array(im1.shape)-1)/2.0

    # Check im2 is bigger or same size
    if (im1im2sizeDiff < 0).any():
        print("\tcorrelate.lucasKanade(): im1 is smaller than im2 in at least one dimension: im1.shape: {}, im2.shape: {}".format(im1.shape, im2.shape))
        raise ValueError("correlate.lucasKanade():DimProblem")

    # Make sure margin is at least 1 for the gradient calculation
    if twoD:
        margin[0] = 0
    elif min(margin) < 1 and min(im1im2sizeDiff) == 0:
        margin = [1]*3

    # Calculate crops -- margin for im2 and more for im1 if it is bigger
    # Margin + half the difference in size for im2 -- im1 will start in the middle.
    crop1 = [slice(im1im2sizeDiff[0]/2+margin[0], im1im2sizeDiff[0]/2+im2.shape[0]-margin[0]),
             slice(im1im2sizeDiff[1]/2+margin[1], im1im2sizeDiff[1]/2+im2.shape[1]-margin[1]),
             slice(im1im2sizeDiff[2]/2+margin[2], im1im2sizeDiff[2]/2+im2.shape[2]-margin[2])]

    # Get subvolume crops from both images -- just the margin for im2
    crop2 = [slice(margin[0], im2.shape[0]-margin[0]),
             slice(margin[1], im2.shape[1]-margin[1]),
             slice(margin[2], im2.shape[2]-margin[2])]

    # Create im2 crop to shift less data
    im2crop = im2[crop2].copy()

    # Calculate effective margin
    # to calculate displacement divergence
    # using max for the margin -- subjective choice
    realMargin = max(margin) + min(im1im2sizeDiff) / 2
    #print( "\tcorrelate.lucasKanade(): realMargin is:", realMargin)

    # If live plot is asked for, initialise canvas
    if imShowProgress is not None:
        import matplotlib.pyplot as plt
        # Plot ranges for signed residual
        vmin = -im2[crop2].max()/2
        vmax = im2[crop2].max()/2
        if not imShowProgressNewFig:
            if imShowProgress == "Z" or imShowProgress == "z":
                plt.axis([im2crop.shape[2], 0, im2crop.shape[1], 0])
            if imShowProgress == "Y" or imShowProgress == "y":
                plt.axis([im2crop.shape[2], 0, im2crop.shape[0], 0])
            if imShowProgress == "X" or imShowProgress == "x":
                plt.axis([im2crop.shape[1], 0, im2crop.shape[0], 0])
            plt.ion()

    # Numerical value for normalising the error
    #errorNormalisationTmp = im1[crop1]
    #errorNormalisation = errorNormalisationTmp[numpy.isfinite(errorNormalisationTmp)].sum()
    #del errorNormalisationTmp
    # 2018-07-10 EA and OS: Removing im1 mask, so errorNormalisation is one-shot
    errorNormalisation = im1[crop1].sum()

    # If there is no initial F, initalise it and im1defCrop to zero.
    if Finit is None:
        F = numpy.eye(4)
        im1defCrop = im1.copy()[crop1]

    else:
        # Make a copy, otherwise it's updated outside, could be a problem...
        F = Finit.copy()

        # Since we are now using Fcentred for iterations, do nothing
        # call FtoTransformation to apply Finit (calculated on the centre of the image) to the origin (0,0,0)
        #F[0:3, -1] = transformationOperator.FtoTransformation(Finit.copy(), Fcentre=im1Centre)["t"]

        # Apply binning on displacement
        #F[0:3,-1] *= FinitBinRatio

        if interpolator == 'C':
            im1defCrop = transformationOperator.applyTransformationOperator(im1, F=F, interpolationOrder=interpolationOrder)[crop1]

        elif interpolator == 'python':
            im1defCrop = transformationOperator.applyTransformationOperatorPython(im1, F=F, interpolationOrder=interpolationOrder)[crop1]

        else:
            return

    # Calculate gradient of the non-moving im2
    # 2017-11-06 EA: This is going in a try, since it's possible to have an error like this:
    #   "Shape of array too small to calculate a numerical gradient, "
    #   ValueError: Shape of array too small to calculate a numerical gradient, at least (edge_order + 1) elements are required.
    try:
        # Use gradient of image 2 which does NOT move
        if twoD:
            # If 2D image we have no gradients in the 1st direction
            im2gradY, im2gradX = numpy.gradient(im2[0])
            im2gradX = im2gradX[numpy.newaxis, ...]
            im2gradY = im2gradY[numpy.newaxis, ...]
            im2gradZ = numpy.zeros_like(im2gradX)
        else:
            im2gradZ, im2gradY, im2gradX = numpy.gradient(im2)
    # If gradient calculation failed, set singular to true, means early exit
    except ValueError:
        # Override max iteration and also set singular
        maxIterations = 0
        singular = True

    # Apply stationary im2 mask -- This has been moved to after the gradient calculation
    if im2mask is not None:
        im2crop[im2mask[crop2] == False] = numpy.nan

    # Initialise iteration variables
    iterationNumber = 0
    returnStatus = 0
    # Big value to start with to ensure the first iteration
    deltaFnorm = 100.0
    errorTmp = numpy.square(numpy.subtract(im2crop, im1defCrop))
    error = errorTmp[numpy.isfinite(errorTmp)].sum() / errorNormalisation

    if verbose:
        print("Start correlation with Error = {:0.2f}".format(error))

    # --- Start Iterations ---
    while iterationNumber < maxIterations and deltaFnorm > minFchange:
        errorPrev = error

        if verbose:
            print("\tIteration Number {:02d}".format(iterationNumber)),

        # No recomputation of gradient -- initialise M and A
        M = numpy.zeros((12, 12), dtype='<f4')
        A = numpy.zeros((12),     dtype='<f4')

        # Compute DIC operators A and M with C library
        DICToolkit.computeDICoperators(im2crop,
                                       im1defCrop,
                                       im2gradZ[crop2],
                                       im2gradY[crop2],
                                       im2gradX[crop2], M, A)

        if twoD:
            # If a twoD image, cut out the bits of the M and A matrices that interest us
            #   This is necessary since the rest is super singular
            A = A[twoDmaskA]
            M = M[twoDmaskM].reshape(6, 6)

        # Solve for delta F
        try:
            deltaF = numpy.dot(numpy.linalg.inv(M), A)
        except numpy.linalg.linalg.LinAlgError:
            singular = True
            break

        if twoD:
            # ...and now put deltaF components back in place for a 3D deltaF
            deltaFnew = numpy.zeros((12), dtype=float)
            deltaFnew[twoDmaskA] = deltaF
            del deltaF
            deltaF = deltaFnew

        deltaFnorm = numpy.linalg.norm(deltaF)

        # Add padding zeros
        deltaF = numpy.hstack([deltaF, numpy.zeros(4)]).reshape((4, 4))

        # Apply Delta F correction to F In Roux X-N paper equation number 11
        F = numpy.dot((numpy.eye(4) - deltaF), F)

        # reset im1def as emtpy matrix for deformed image
        if interpolator == 'C':
            im1defCrop = transformationOperator.applyTransformationOperator(im1, F=F, interpolationOrder=interpolationOrder)[crop1]

        elif interpolator == 'python':
            im1defCrop = transformationOperator.applyTransformationOperatorPython(im1, F=F, interpolationOrder=interpolationOrder)[crop1]

        else:
            return

        # Error calculation
        errorTmp = numpy.square(numpy.subtract(im2crop, im1defCrop))
        error = errorTmp[numpy.isfinite(errorTmp)].sum() / errorNormalisation

        # Keep interested people up to date with what's happening
        if verbose:
            print("Error = {:0.2f}".format(error)),
            print("deltaFnorm = {:0.4f}".format(deltaFnorm))

        # Catch divergence condition after half of the max iterations
        if errorPrev < error*0.8 and iterationNumber > maxIterations/2:
            # undo this bad F which has increased the error:
            F = numpy.dot((numpy.eye(4) + deltaF), F)
            returnStatus = -1
            if verbose:
                print("\t -> diverging on error condition")
            break

        # Second divergence criterion on displacement (Issue #62)
        #   If any displcement is bigger than 5* the margin...
        # if ( numpy.abs( transformationOperator.FtoTransformation( F.copy(), Fpoint=im1Centre )['t'] ) > 5*realMargin ).any():
        if (numpy.abs(transformationOperator.FtoTransformation(F.copy())['t']) > 5*realMargin).any():
            if verbose:
                print("\t -> diverging on displacement condition")
            returnStatus = -3
            break

        if imShowProgress is not None:
            if imShowProgress == "Z" or imShowProgress == "z":
                if imShowProgressNewFig: plt.figure()
                else: plt.clf()
                plt.imshow(numpy.subtract(im2crop, im1defCrop)[im2crop.shape[0]/2, :, :], cmap='coolwarm', vmin=vmin, vmax=vmax)
            if imShowProgress == "Y" or imShowProgress == "y":
                if imShowProgressNewFig: plt.figure()
                else: plt.clf()
                plt.imshow(numpy.subtract(im2crop, im1defCrop)[:, im2crop.shape[1]/2, :], cmap='coolwarm', vmin=vmin, vmax=vmax)
            if imShowProgress == "X" or imShowProgress == "x":
                if imShowProgressNewFig: plt.figure()
                else: plt.clf()
                plt.imshow(numpy.subtract(im2crop, im1defCrop)[:, :, im2crop.shape[2]/2], cmap='coolwarm', vmin=vmin, vmax=vmax)
            plt.title('\t\tIteration Number = {}'.format(iterationNumber))
            plt.pause(0.5)

        if verbose:
            # Convert F into F applied at the im1Centre
            #Fcentre = F.copy()
            #Fcentre[0:3,-1] -= ( im1Centre - numpy.dot( F[0:3,0:3], im1Centre ) )
            #Fcentre[0:3, -1] = transformationOperator.FtoTransformation(F.copy(), Fpoint=im1Centre)["t"]
            print("F = \n", F, "\n\n")

        iterationNumber += 1

    # Positive return status is a healthy end of while loop:
    if iterationNumber >= maxIterations:
        returnStatus = 1
    if deltaFnorm <= minFchange:
        returnStatus = 2
    if singular:
        returnStatus = -2

    if verbose:
        if iterationNumber >= maxIterations:
            print("\t -> No convergency before max iterations")
        if deltaFnorm <= minFchange:
            print("\t -> Convergency")
        if singular:
            print("\t -> Singular")

    # create human readable transformation
    #trans = transformationOperator.FtoTransformation( F.copy(), Fpoint=numpy.array(im1.shape)/2.0 )
    #trans = transformationOperator.FtoTransformation(F.copy())
    trans = transformationOperator.FtoTransformation(F.copy())
    # display transform if verbose
    if verbose:
        print("\t --> displacements:  z={:.2f} vox".format(trans['t'][0]))
        print("\t                     y={:.2f} vox".format(trans['t'][1]))
        print("\t                     x={:.2f} vox".format(trans['t'][2]))
        print("\t --> rotations comps:z={:.2f} deg".format(trans['r'][0]))
        print("\t                     y={:.2f} deg".format(trans['r'][1]))
        print("\t                     x={:.2f} deg".format(trans['r'][2]))

    # Create F appled at the centre of the image for returning
    #Fcentre = F.copy()
    FzeroOrigin = F.copy()
    FmaskCentre = F.copy()
    #Fcentre[0:3,-1] -= ( im1Centre - numpy.dot( F[0:3,0:3], im1Centre ) )
    #Fcentre[0:3, -1] = transformationOperator.FtoTransformation(    F.copy(), Fpoint=im1Centre)["t"]
    FzeroOrigin[0:3, -1] = transformationOperator.FtoTransformation(F.copy(), Fpoint=[0, 0, 0])["t"]

    if im2mask is not None:
        # If a mask on im2 is defined, return an F at the centre of the mass
        maskCOM = ltk.getCentresOfMass(im2mask[crop2])[-1]
        #print("Mask COM", maskCOM)
        #print( "\nNormal F:\n", F)
        F[0:3, -1] = transformationOperator.FtoTransformation(F.copy(), Fcentre=(numpy.array(im2crop.shape)-1)/2.0, Fpoint=maskCOM)["t"]
        #print( "\nF in mask:\n", F)

    return {'error': error,
            'transformation': trans,
            'F': FzeroOrigin,
            'Fcentre': F,
            'returnStatus': returnStatus,
            'iterationNumber': iterationNumber,
            'deltaFnorm': deltaFnorm}


def pixelSearch(imagette1, im2,
                searchCentre=None,
                searchRange={'zRange': [-2, 2],
                             'yRange': [-2, 2], 'xRange': [-2, 2]},
                skipPixels=1,
                globalCoords=False):
    """
        Interface to Pixel Search C code.

        Parameters
        ----------
        It important to remember that the C code runs MUCH faster in its current incarnation when it has
        a cut-out im2 to deal with (this is related to processor optimistaions).
        When the globalCoords flag is true we should search with all of im2 in memory, but (default) we will cut it out.

        - First two parameters are 3D numpy arrays, which are images

        - optional (but usually expected): The point in im2 around which the search range is defined

        - optional: Search range as a dictionary containing 3 keys: 'zRange', 'yRange', and 'xRange',
            Each of which contains a list with two items. Default +-2 pixels in every direction

        Returns
        -------
        Dictionary containing:

            'transformation': { 't': returns[0:3] }

            'cc': returns[3]
    """
    if searchCentre is None:
        searchCentre = numpy.array(im2.shape,  dtype='<f4')/2.0
    else:
        searchCentre = numpy.array(searchCentre, dtype='<f4')

    # If dictionary overwrite with numpy array
    if type(searchRange) is dict:
        searchRange = numpy.array(
            [searchRange['zRange'], searchRange['yRange'], searchRange['xRange']], dtype='<f4')
    else:
        print("searchRange should be a dict with 'zRange', 'yRange', and 'xRange' entries")

    # If we've asked for a local correlation, cut out im2
    if not globalCoords:
        # TODO: Check that these are not going outside the boundaries of im2, otherwise our displacement will be off...
        imagette2slice = [slice(int(searchCentre[0] - numpy.floor(imagette1.shape[0]/2.0) + searchRange[0, 0]),
                                int(searchCentre[0] + numpy.ceil(imagette1.shape[0]/2.0) + searchRange[0, 1])),
                          slice(int(searchCentre[1] - numpy.floor(imagette1.shape[1]/2.0) + searchRange[1, 0]),
                                int(searchCentre[1] + numpy.ceil(imagette1.shape[1]/2.0) + searchRange[1, 1])),
                          slice(int(searchCentre[2] - numpy.floor(imagette1.shape[2]/2.0) + searchRange[2, 0]),
                                int(searchCentre[2] + numpy.ceil(imagette1.shape[2]/2.0) + searchRange[2, 1]))]

        imagette2 = im2[imagette2slice].copy()

        # Update search centre:
        searchCentre = numpy.array([searchCentre[0]-imagette2slice[0].start,
                                    searchCentre[1]-imagette2slice[1].start,
                                    searchCentre[2]-imagette2slice[2].start], dtype='<f4')
    else:
        imagette2 = im2

    # Run the actual pixel search
    # print imagette1.shape, imagette2.shape, searchCentre, searchRange
    returns = DICToolkit.pixelSearchC(
        imagette1, imagette2, searchCentre, searchRange, 4)

    # Collect and pack returns
    return {'transformation': {'t': returns[0:3]},
            'cc': returns[3]}


def globalCorr(im1, im2, mesh, outputFolder="./", convergenceCriterion=0.01, debugFiles=True, maxIterations=20, initialDisplacement=None):
    print("correlate.globalCorr(): converting im1 to 32-bit float")
    im1 = im1.astype('<f4')

    print("\tcorrelate.globalCorr(): Loading mesh...")
    points = mesh["points"].astype('<f8')
    cells = mesh["cells"].astype('<u2')
    imTetLabel = mesh["lab"].astype('<u2')
    meshPadding = mesh["padding"]
    meshPaddingSlice = [slice(meshPadding+1, -meshPadding-1), slice(
        meshPadding+1, -meshPadding-1), slice(meshPadding+1, -meshPadding-1)]

    print("\tcorrelate.globalCorr(): Points: ", points.shape)
    print("\tcorrelate.globalCorr(): Cells:", cells.shape)
    print("\tcorrelate.globalCorr(): Mesh Padding:", meshPadding)

    ###############################################################
    # Step 2-1 Apply deformation and interpolate pixels
    ###############################################################
    print("\tcorrelate.globalCorr(): Allocating global matrix and vector...")
    globalMatrix = numpy.zeros(
        (3*points.shape[0], 3*points.shape[0]), dtype='<f4')
    globalVector = numpy.zeros(
        (3*points.shape[0]),                    dtype='<f4')
    displacements = numpy.zeros(
        (3*points.shape[0]),                    dtype='<f8')

    print("\tcorrelate.globalCorr(): Allocating 3D data (deformed image)")
    if initialDisplacement is None:
        im1Def = im1.copy()
    else:
        print("\tcorrelate.globalCorr(): Applying initial deformation to image")
        displacements = numpy.ravel(initialDisplacement)
        im1Def = numpy.zeros_like(im1)
        DICToolkit.applyMeshTransformation(
            im1, imTetLabel, im1Def, cells, points, displacements.reshape(3, points.shape[0]))
        tifffile.imsave(outputFolder+"/im1.tif",       im1[meshPaddingSlice])
        tifffile.imsave(outputFolder+"/im1def.tif", im1Def[meshPaddingSlice])
        tifffile.imsave(outputFolder+"/residual.tif",
                        im2[meshPaddingSlice]-im1[meshPaddingSlice])
    import time
    timeStart = time.time()

    print("correlate.globalCorr(): Correlating (MF)!")
    print("\tcorrelate.globalCorr(): Calculating gradient...")
    im2Grad = numpy.array(numpy.gradient(im2), dtype='<f4')

    print("\tcorrelate.globalCorr(): Computing global matrix")
    # This generates the globalMatrix (big M matrix) with imGrad as input
    #EnhancedMeshImageToolkitC.globalMatrix_func( imTetLabel, im1Grad, cells, points, globalMatrix )
    DICToolkit.computeDICglobalMatrix(
        imTetLabel, im2Grad, cells, points, globalMatrix)
    print("\tcorrelate.globalCorr(): Inversing global matrix")
    # print globalMatrix, "\n\n\n\n\n"
    # + 0.0*numpy.eye( globalMatrix.shape[0] ) )
    globalMatrixInv = numpy.linalg.inv(globalMatrix)
    # print globalMatrixInv

    print("\tcorrelate.globalCorr(): Computing gradient")
    # recalculate the gradients from the new im1def
    #EnhancedMeshImageToolkitC.imGradient_func( im1Def, im1Grad )
    #im1Grad = numpy.array( numpy.gradient( im1Def ), dtype='<f4')
    if debugFiles:
        print("\tcorrelate.globalCorr(): Writing Gradient and Residuals TIFFs")
        #tifffile.imsave( outputFolder+"/grad-%i.tif"%(0), im2Grad)
        #iman.save_as_vtk( imOut,      o_name="out" )
        tifffile.imsave(outputFolder+"/residual-%i.tif" %
                        (0), im1Def[meshPaddingSlice]-im2[meshPaddingSlice])

    def errorCalc(im1, im2, meshPaddingSlice):
        return numpy.square(im2[meshPaddingSlice] - im1[meshPaddingSlice]).sum()

    errorZero = errorCalc(im2, im1, meshPaddingSlice)
    print("\tcorrelate.globalCorr(): Initial Error (abs) = ", errorZero)

    errorFh = open(outputFolder+"/iterationsError.txt", "w")
    errorFh.write("#Iterations(b)\tError(%)\n")

    errorOut = 100.0
    errorIn = 101.0
    i = 0

    # We try to solve Md=F
    # while errorOut > 0.1 and errorOut < errorIn:
    # while errorOut > 0.1 and i <= maxIterations and errorOut < errorIn:
    while errorOut > 0.1 and i <= maxIterations:
        i += 1

        print("\tcorrelate.globalCorr(): Iteration", i)
        errorIn = 100 * (errorCalc(im2, im1Def, meshPaddingSlice)) / errorZero
        print("\t\tcorrelate.globalCorr(): Error In  = %0.5f%%" % (errorIn))

        print("\t\tcorrelate.globalCorr(): Computing global vector...")
        # This function returns globalVector (F) taking in im1Def and im2 and the gradients
        DICToolkit.computeDICglobalVector(
            imTetLabel, im2Grad, im1Def, im2, cells, points, globalVector)
        # print globalVector
        print("\t\tcorrelate.globalCorr(): Computing displacement...")
        # update displacements (d)
        dx = numpy.dot(globalMatrixInv, globalVector).astype('<f8')

        # print "\t\tcorrelate.globalCorr(): globalMatrixInv.mean() = ", globalMatrixInv.mean()
        print("\t\tcorrelate.globalCorr(): | globalVector | = ",
              numpy.linalg.norm(globalVector))
        print("\t\tcorrelate.globalCorr(): dx.mean() = ", dx.mean())

        displacements += dx
        # if printLevel > 3: print globalVector.sum()

        print("\t\tcorrelate.globalCorr(): Applying displacement to image...")
        # We generate a new im1def by adding the displacements to the nodes
        DICToolkit.applyMeshTransformation(
            im1, imTetLabel, im1Def, cells, points, displacements.reshape(3, points.shape[0]))

        if debugFiles:
            print("\t\tcorrelate.globalCorr(): Saving deformed images...")
            #iman.save_as_vtk( imOut,      o_name="out" )
            if debugFiles:
                tifffile.imsave(outputFolder+"/residual-%i.tif" %
                                (i),  im1Def[meshPaddingSlice]-im2[meshPaddingSlice])
                tifffile.imsave(outputFolder+"/im1def-%i.tif" %
                                (i),    im1Def[meshPaddingSlice])
            #meshio.write( outputFolder+"/meshDef-%i.vtu"%(i), points+displacements.reshape( points.shape[0], 3 ), cellsOrig )

        errorOut = 100 * (errorCalc(im2, im1Def, meshPaddingSlice)) / errorZero

        errorFh.write("{}\t{}\n".format(i, errorOut))
        errorFh.flush()

        print("\t\tcorrelate.globalCorr(): Error Out = %0.5f%%" % (errorOut))

    timeStop = time.time()
    print("\tcorrelate.globalCorr(): Time: I think I ran for: ",
          timeStop - timeStart, " Seconds")

    errorFh.close()

    return [errorIn, errorOut, i-1]





if __name__ == "__main__":
    import tifffile as tf
    import matplotlib.pyplot as plt

    margin = 10
    im1 = tf.imread('../../data/snow/snow.tif').astype('<f4')
    im2 = tf.imread('../../data/snow/snow-def.tif').astype('<f4')

    returns = lucasKanade(im1, im2, margin=margin,
                          Finit=transformationOperator.computeTransformationOperator(
                              {'r': [14.0, 0.0, 0.0]}),
                          maxIterations=100,
                          minFchange=0.001,
                          interpolationOrder=1,
                          interpolator='C',
                          verbose=True, imShowProgress=True)

    print(returns['transformation'])
