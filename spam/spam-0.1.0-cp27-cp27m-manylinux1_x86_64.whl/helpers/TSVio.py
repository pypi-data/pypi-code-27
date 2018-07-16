"""
This module offers a set functions in order to manipulate TSV files.
It writes, reads, cleans and visualises TSV files used in DIC clients.
"""

from __future__ import print_function
import numpy
import os


def writeRegistration(fileName, regCentre, regReturns):
    '''
    This function writes a correctly formatted TSV file from the result of a single lucasKanade call, allowing it to be used as an initial registration.

    Parameters
    ----------

        fileName : string
            The file name for output, suggestion: it should probably end with ".tsv"

        regCentre : 3-component list
            A list contianing the point at which `Fcentre` has been measured.
            This is typically the middle of the image, and can be obtained as follows:
            numpy.array( im.shape )/2
            The conversion to a numpy array is necessary, since tuples cannot be divided by a number directly.

        regReturns : dictionary
            This should be the return dictionary from `lucasKanade`.
            From this dictionary will be extracted: 'Fcentre', 'error', 'iterationNumber', 'returnStatus', 'deltaFnorm'

    '''
    regF = regReturns['Fcentre']
    
    # catch 2D images
    if len(regCentre) == 2:
        regCentre = [1, regCentre[0], regCentre[1]]

    # Make one big array for writing:
    #   First the node number,
    #   3 node positions,
    #   F[0:3,0:2]
    #   Pixel-search CC
    #   SubPixError, SubPixIterations, SubPixelReturnStatus
    TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tF11\tF12\tF13\tZdisp\tF21\tF22\tF23\tYdisp\tF31\tF32\tF33\tXdisp\tSubPixError\tSubPixIterations\tSubPixReturnStat\tSubPixDeltaFnorm"
    outMatrix = numpy.array([[1],
                             [regCentre[0]],
                             [regCentre[1]],
                             [regCentre[2]],
                             [regF[0, 0]],
                             [regF[0, 1]],
                             [regF[0, 2]],
                             [regF[0, 3]],
                             [regF[1, 0]],
                             [regF[1, 1]],
                             [regF[1, 2]],
                             [regF[1, 3]],
                             [regF[2, 0]],
                             [regF[2, 1]],
                             [regF[2, 2]],
                             [regF[2, 3]],
                             [regReturns['error']],
                             [regReturns['iterationNumber']],
                             [regReturns['returnStatus']],
                             [regReturns['deltaFnorm']]])

    numpy.savetxt(fileName,
                  outMatrix.T,
                  fmt='%.7f',
                  delimiter='\t',
                  newline='\n',
                  comments='',
                  header=TSVheader)


def readTSV(fileName, onlyT=False, fieldBinRatio=1.0, returnRS=False, returnDeltaFnorm=False):
    """
    This function reads a TSV file containing a field of transformation operators `F` at a number of points.
    This is typically the output of the DICdiscrete and DICregularGrid clients

    Parameters
    ----------
    fileName : string
        Name of the file

    onlyT : bool, optional
        if True: will return only the translation part of the transformation

    fieldBinRatio : int, optional
        if the input field is refer to a binned version of the image
        `e.g.`, if ``fieldBinRatio = 2`` the field_name values have been calculated
        for an image half the size of what the returned Ffield is referring to

    returnRS : bool, optional
        if True: will return the SubPixelReturnStatus of the correlation

    returnDeltaFnorm : bool, optional
        if True: will return the SubPixelDeltaFnorm of the correlation

    Returns
    -------
    Dictionary containing:
        fieldDims: 1x3 array of the field dimensions (ZYX)

        fieldCoords: nx3 array of n points coordinates (ZYX)

        Ffield: nx4x4 array of n points transformation operators

        SubPixReturnStat: nx1 array of n points SubPixelReturnStatus from the correlation

        SubPixDeltaFnorm: nx1 array of n points SubPixelDeltaFnorm from the correlation
    """
    if not os.path.isfile(fileName):
        print("\tTSVio.readTSV(): {} is not a file. Exiting.".format(fileName))
        return

    f = numpy.genfromtxt(fileName, delimiter="\t", names=True)
    RS = []
    deltaFnorm = []

    # If this is a one-line TSV file (an initial registration for example)
    if f.size == 1:
        print("\tTSVio.readTSV(): {} seems only to have one line.".format(fileName))
        nPoints = 1
        fieldDims = [1, 1, 1]
        
        # Sort out the field coordinates
        fieldCoords = numpy.zeros((nPoints, 3))
        fieldCoords[:, 0] = f['Zpos']*fieldBinRatio
        fieldCoords[:, 1] = f['Ypos']*fieldBinRatio
        fieldCoords[:, 2] = f['Xpos']*fieldBinRatio
        
        # Sort out the components of F
        Ffield = numpy.zeros((nPoints, 4, 4))
        Ffield[0] = numpy.eye(4)
        
        # Fill in displacements
        try:
            Ffield[0, 0, 3] = f['Zdisp']*fieldBinRatio
            Ffield[0, 1, 3] = f['Ydisp']*fieldBinRatio
            Ffield[0, 2, 3] = f['Xdisp']*fieldBinRatio
        except ValueError:
            Ffield[0, 0, 3] = f['F14']*fieldBinRatio
            Ffield[0, 1, 3] = f['F24']*fieldBinRatio
            Ffield[0, 2, 3] = f['F34']*fieldBinRatio

        # Get non-displacement components if asked
        if not onlyT:
            Ffield[0, 0, 0] = f['F11']
            Ffield[0, 0, 1] = f['F12']
            Ffield[0, 0, 2] = f['F13']
            Ffield[0, 1, 0] = f['F21']
            Ffield[0, 1, 1] = f['F22']
            Ffield[0, 1, 2] = f['F23']
            Ffield[0, 2, 0] = f['F31']
            Ffield[0, 2, 1] = f['F32']
            Ffield[0, 2, 2] = f['F33']

        # Return ReturnStatus if asked
        if returnRS:
            RS = f['SubPixReturnStat']

        # Return deltaFnorm if asked
        if returnDeltaFnorm:
            deltaFnorm = f['SubPixDeltaFnorm']

    # there is more than one line in the TSV file -- a field -- typical case
    else:
        nPoints = f.size
        # Sort out the field coordinates
        fieldCoords = numpy.zeros((nPoints, 3))
        fieldCoords[:, 0] = f['Zpos']*fieldBinRatio
        fieldCoords[:, 1] = f['Ypos']*fieldBinRatio
        fieldCoords[:, 2] = f['Xpos']*fieldBinRatio

        # 2018-01-26: EA PB ER: back-calculate field dimensions
        fieldDims = numpy.array([len(numpy.unique(f['Zpos'])), len(numpy.unique(f['Ypos'])), len(numpy.unique(f['Xpos']))])
        print("\tTSVio.readTSV(): Field Dimensions: {}".format(fieldDims))

        # create ReturnStatus and deltaFNorm matrices if asked
        if returnRS:
            RS = numpy.zeros(nPoints)
            RS[:] = f[:]['SubPixReturnStat']
        if returnDeltaFnorm:
            deltaFnorm = numpy.zeros(nPoints)
            deltaFnorm = f[:]['SubPixDeltaFnorm']

        # Sort out the components of F
        Ffield = numpy.zeros((nPoints, 4, 4))
        for n in xrange(nPoints):
            # Initialise with Identity matrix
            Ffield[n] = numpy.eye(4)

            # Fill in displacements
            try:
                Ffield[n, 0, 3] = f[n]['Zdisp']*fieldBinRatio
                Ffield[n, 1, 3] = f[n]['Ydisp']*fieldBinRatio
                Ffield[n, 2, 3] = f[n]['Xdisp']*fieldBinRatio
            except ValueError:
                Ffield[n, 0, 3] = f[n]['F14']*fieldBinRatio
                Ffield[n, 1, 3] = f[n]['F24']*fieldBinRatio
                Ffield[n, 2, 3] = f[n]['F34']*fieldBinRatio

            # Get non-displacement components if asked
            if not onlyT:
                Ffield[n, 0, 0] = f[n]['F11']
                Ffield[n, 0, 1] = f[n]['F12']
                Ffield[n, 0, 2] = f[n]['F13']
                Ffield[n, 1, 0] = f[n]['F21']
                Ffield[n, 1, 1] = f[n]['F22']
                Ffield[n, 1, 2] = f[n]['F23']
                Ffield[n, 2, 0] = f[n]['F31']
                Ffield[n, 2, 1] = f[n]['F32']
                Ffield[n, 2, 2] = f[n]['F33']

    return {"fieldDims": fieldDims,
            "fieldCoords": fieldCoords,
            "Ffield": Ffield,
            "SubPixReturnStat": RS,
            "SubPixDeltaFnorm": deltaFnorm}

'''
def correctFfield(fileName=None, fieldCoords=None, fieldValues=None, fieldRS=None, fieldDF=None, onlyT=False, fieldBinRatio=1.0, ignoreBadPoints=False, correctBadPoints=False, deltaFnormMin=0.001, neighbours=12, filterPoints=False, filterPointsRadius=3, verbose=False, saveFile=False, saveFileName=None):
    """
    This function corrects a field of transformation operators `F` calculated at a number of points.
    This is typically the output of the DICdiscrete and DICregularGrid clients.
    The correction is done based on the `SubPixelReturnStatus` and `SubPixelDeltaFnorm` of the correlated points.
    It takes as an input either a tsv file containing the result of the correlation or
    4 separate arrays: 1)the coordinates of the points, 2)the Ffield, 3)the `SubPixelReturnStatus` and 4)the `SubPixelDeltaFnorm`

    Parameters
    ----------
    fileName : string, optional
        name of the file

    fieldCoords : 2D array, optional
        nx3 array of n points coordinates (ZYX)
        centre where each transformation operator `F` has been calculated

    fieldValues : 3D array, optional
        nx4x4 array of n points transformation operators

    fieldRS : 1D array, optional
        nx1 array of n points `SubPixelReturnStatus` from the correlation

    fieldDf : 1D array, optional
        nx1 array of n points `SubPixelDeltaFnorm` from the correlation

    onlyT : bool, optional
        if True: will consider only the translation part of the transformation
        Default = False

    fieldBinRatio : int, optional
        if the input field is referred to a binned version of the image
        `e.g.`, if `fieldBinRatio = 2` the fileName values have been calculated
        for an image half the size of what the returned Ffield is referring to
        Default = 1.0

    ignoreBadPoints : bool, optional
        if True: it will replace the `F` matrices of the badly correlated points with the identity matrix.
        Bad points are set according to `SubPixelReturnStatus` and `SubPixelDeltaFnorm` of the correlation
        Default = False

    correctBadPoints : bool, optional
        if True: it will replace the `F` matrices of the badly correlated points with the weighted function of the k nearest good points
        Bad points are set according to `SubPixelReturnStatus` and `SubPixelDeltaFnorm` of the correlation 
        The number of the nearest good neighbours can be defined (see below `neighbours`)
        Default = False

    deltaFnormMin= float, optional
        minimum value of subpixel change in F to consider a point with `SubPixelReturnStatus`=1 as good or bad
        Default = 0.001

    neighbours : int, optional
        if `correctBadPoints` is activated, it specifies the number of the nearest neighbours to consider
        If == 1, the nearest neighbour is used, if >1 neighbours are weighted according to distance
        Default = 12

    filterPoints : bool, optional
        if True: a median filter will be applied on the `F` of each point
        Default = False

    filterPointsRadius : int, optional
        Radius of median filter.
        Size of cubic structuring element is 2*filterPointsRadius+1.
        Default = 3

    verbose : bool, optional
        follow the progress of the function
        Default = False

    saveFile : bool, optional
        save the corrected file into a tsv
        Default = False

    Returns
    -------
    Ffield: nx4x4 array of n points transformation operators `F` after the correction

    """

    # read the input arguments
    if fileName:
        if not os.path.isfile(fileName):
            print("\tTSVio.correctFfield():{} is not a file. Exiting.".format(fileName))
            return
        else:
            fi = readTSV( fileName, fieldBinRatio = fieldBinRatio, onlyT=onlyT, returnRS=True, returnDeltaFnorm=True )
            Ffield = fi["Ffield"]
            fieldCoords = fi["fieldCoords"]
            fieldDims = fi["fieldDims"]
            RS = fi["SubPixReturnStat"]
            deltaFnorm = fi["SubPixDeltaFnorm"]
    #elif fieldCoords and fieldValues and fieldRS and fieldDF:
    elif fieldCoords is not None and fieldValues is not None and fieldRS is not None and fieldDF is not None:
        fieldCoords = fieldCoords
        fieldDims = numpy.array([len(numpy.unique(fieldCoords[0])), len(numpy.unique(fieldCoords[1])), len(numpy.unique(fieldCoords[2]))])
        Ffield = fieldValues
        RS = fieldRS
        deltaFnorm = fieldDF
    else:
        print("\tTSVio.correctFfield(): Not enough arguments given. Exiting.")
        return

    # check good and bad correlation points according to `SubPixelReturnStatus` and `SubPixelDeltaFnorm` conditions
    goodPoints = numpy.where(numpy.logical_or(RS == 2, numpy.logical_and(RS == 1, deltaFnorm <= deltaFnormMin)))
    badPoints = numpy.where(numpy.logical_or(RS <= 0, numpy.logical_and(RS == 1, deltaFnorm > deltaFnormMin)))

    # if asked, ignore the bad correlation points by setting their F to identity matrix
    if ignoreBadPoints:
        Ffield[badPoints] = numpy.eye(4)

    # if asked, replace the bad correlation points with the weighted influence of the k nearest good neighbours
    if correctBadPoints:
        # create the k-d tree of the coordinates of good points, we need this to search for the k nearest neighbours easily
        #   for details see: https://en.wikipedia.org/wiki/K-d_tree &
        #   https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.KDTree.query.html

        from scipy.spatial import KDTree
        treeCoord = KDTree(fieldCoords[goodPoints])

        # extract the F matrices of the bad points
        fieldBad = numpy.zeros_like(Ffield[badPoints])
        fieldBad[:, -1, :] = numpy.array([0, 0, 0, 1])

        # check if we have asked only for the closest neighbour
        if neighbours == 1:

            # loop over each bad point
            for badPoint in xrange(badPoints[0].shape[0]):
                if verbose: 
                    print("\rWorking on bad point: {} of {}".format( badPoint+1, badPoints[0].shape[0] ), end='')
                # call tree.query to calculate:
                #   {ind}: the index of the nearest neighbour (as neighbours we consider only good points)
                #   {distnace}: distance (Minkowski norm 2, which is  the usual Euclidean distance) of the bad point to the nearest neighbour
                distance, ind = treeCoord.query(fieldCoords[badPoints][badPoint], k=neighbours)

                # replace bad point's F with the F of the nearest good point
                fieldBad[badPoint][:-1] = Ffield[goodPoints][ind][:-1].copy()

            # replace the corrected F field
            Ffield[badPoints] = fieldBad

        # if we have asked for more neighbours
        else:

            # loop over each bad point
            for badPoint in xrange(badPoints[0].shape[0]):
                if verbose:
                    print("\rWorking on bad point: {} of {}".format(badPoint+1, badPoints[0].shape[0]), end='')
                # call tree.query to calculate:
                #   {ind}: k nearest neighbours (as neighbours we consider only good points)
                #   {distnace}: distance (Minkowski norm 2, which is  the usual Euclidean distance) of the bad point to each of the ith nearest neighbour
                distance, ind = treeCoord.query(fieldCoords[badPoints][badPoint], k=neighbours)

                # compute the "Inverse Distance Weighting" since the nearest points should have the major influence
                weightSumInv = sum(1/distance)

                # loop over each good neighbour point:
                for neighbour in xrange(neighbours):
                    # calculate its weight
                    weightInv = (1/distance[neighbour])/float(weightSumInv)

                    # replace the F components of the bad point with the weighted F components of the ith nearest good neighbour
                    fieldBad[badPoint][:-1] += Ffield[goodPoints][ind[neighbour]][:-1]*weightInv

            # replace the corrected F field
            Ffield[badPoints] = fieldBad

     # if asked, apply a median filter of a specific size in the F field
    if filterPoints:
        import scipy.ndimage

        Ffield[:, 0, 0] = scipy.ndimage.filters.median_filter(Ffield[:, 0, 0].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 1, 0] = scipy.ndimage.filters.median_filter(Ffield[:, 1, 0].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 2, 0] = scipy.ndimage.filters.median_filter(Ffield[:, 2, 0].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()

        Ffield[:, 0, 1] = scipy.ndimage.filters.median_filter(Ffield[:, 0, 1].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 1, 1] = scipy.ndimage.filters.median_filter(Ffield[:, 1, 1].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 2, 1] = scipy.ndimage.filters.median_filter(Ffield[:, 2, 1].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()

        Ffield[:, 0, 2] = scipy.ndimage.filters.median_filter(Ffield[:, 0, 2].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 1, 2] = scipy.ndimage.filters.median_filter(Ffield[:, 1, 2].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 2, 2] = scipy.ndimage.filters.median_filter(Ffield[:, 2, 2].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()

        Ffield[:, 0, -1] = scipy.ndimage.filters.median_filter(Ffield[:, 0, -1].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 1, -1] = scipy.ndimage.filters.median_filter(Ffield[:, 1, -1].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()
        Ffield[:, 2, -1] = scipy.ndimage.filters.median_filter(Ffield[:, 2, -1].reshape(fieldDims), size=(2*filterPointsRadius+1)).ravel()

    if saveFile:
        # if asked, write the corrected Ffield into a TSV
        if fileName:
            outDir = os.path.dirname(fileName)
            prefix = os.path.splitext(os.path.basename(fileName))[0]
        elif saveFileName:
            outDir = os.path.dirname(saveFileName)
            prefix = os.path.splitext(os.path.basename(saveFileName))[0]
        elif savefileName == None and fileName == None:
            outDir = "."
            prefix = "spam"
            
        TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tF11\tF12\tF13\tZdisp\tF21\tF22\tF23\tYdisp\tF31\tF32\tF33\tXdisp\tSubPixReturnStat\tSubPixDeltaFnorm"
        outMatrix = numpy.array( [  numpy.array(range( Ffield.shape[0] )),
                                    fieldCoords[:,0], fieldCoords[:,1], fieldCoords[:,2],
                                       Ffield[:,0,0],    Ffield[:,0,1],    Ffield[:,0,2],    Ffield[:,0,3],
                                       Ffield[:,1,0],    Ffield[:,1,1],    Ffield[:,1,2],    Ffield[:,1,3],
                                       Ffield[:,2,0],    Ffield[:,2,1],    Ffield[:,2,2],    Ffield[:,2,3],
                                       RS,               deltaFnorm                                        ] ).T

        if filterPoints:
            title = "{}/{}-corrected-N{}-filteredRad{}.tsv".format(outDir,prefix,neighbours,filterPointsRadius)
        else:
            title = "{}/{}-corrected-N{}.tsv".format(outDir,prefix,neighbours)
        numpy.savetxt(  title,
                        outMatrix,
                        fmt      = '%.7f',
                        delimiter= '\t',
                        newline  = '\n',
                        comments = '',
                        header   = TSVheader )

    return Ffield
'''

def TSVtoTIFF( fileName, onlyT=True, outDir=None, prefix=None):
    '''
    This function converts a TSV file (typically the output of the DICdiscrete and DICregularGrid clients)
    to a tiff file for visualising the F field.

    Parameters
    ----------
        fileName : string
            Name of the file

        onlyT : bool, optional
            if True: will return only the translation part of the transformation field

        outDir : string, optional
            Output directory
            Default is the dirname of input file

        prefix : string, optional
            Prefix for output files
            Default is basename of input file (without extension)
    '''

    import tifffile
    # use the helper function to read the TSV file
    fi = readTSV( fileName, onlyT=onlyT )
    dims = fi["fieldDims"]
    Ffield = fi["Ffield"]

    # output file directory
    if outDir == None:
        outDir = os.path.dirname(fileName)

    # output file name prefix
    if prefix == None:
        prefix = os.path.splitext(os.path.basename(fileName))[0]

    Fcomponents = [ [ 'Zdisp', 0, 3 ],
                    [ 'Ydisp', 1, 3 ],
                    [ 'Xdisp', 2, 3 ],]

    for component in Fcomponents:
        tifffile.imsave( "{}/{}-{}.tif".format( outDir, prefix, component[0] ),
                         Ffield[:,component[1],component[2]].reshape(dims).astype('<f4') )


def TSVtoVTK( fileName, onlyT=True, outDir=None, prefix=None):
    '''
    This function converts a TSV file (typically the output of the DICdiscrete and DICregularGrid clients)
    to a vtk file for visualising the F field.

    Parameters
    ----------
        fileName : string
            Name of the file

        outDir : string
            Output directory
            Default is the dirname of input file

        prefix : string
            Prefix for output files
            Default is basename of input file (without extension)
    '''
    # use the helper function to read the TSV file
    fi = readTSV(fileName, onlyT=True )
    dims = fi["fieldDims"]
    Ffield = fi["Ffield"]

    cellData = {'subpixel-disp-xyz':  Ffield[ :, :-1, 3 ].reshape((dims[0], dims[1], dims[2],3))}

    # output file directory
    if outDir == None:
        outDir = os.path.dirname(fileName)

    # output file name prefix
    if prefix == None:
        prefix = os.path.splitext(os.path.basename(fileName))[0]

    import spam.helpers.vtkio as vtkio
    vtkio.writeStructuredVTK(cellData=cellData, fileName="{}/{}.vtk".format( outDir, prefix ))