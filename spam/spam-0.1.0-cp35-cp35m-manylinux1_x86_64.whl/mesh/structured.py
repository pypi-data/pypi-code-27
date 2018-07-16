"""
This module offers a set of tools in order to manipulate structured meshes.

>>> # import module
>>> import spam.mesh.structured as smesh


The strucutred VTK files used to save the data have the form:

.. code-block:: text

    # vtk DataFile Version 2.0
    VTK file from spam: spam.vtk
    ASCII

    DATASET STRUCTURED_POINTS
    DIMENSIONS nx ny nz
    ASPECT_RATIO lx ly lz
    ORIGIN ox oy oz

    POINT_DATA nx x ny x nz

    SCALARS myNodalField1 float
    LOOKUP_TABLE default
        nodalValue_1
        nodalValue_2
        nodalValue_3
        ...

    VECTORS myNodalField2 float
    LOOKUP_TABLE default
        nodalValue_1_X nodalValue_1_Y nodalValue_1_Z
        nodalValue_2_X nodalValue_2_Y nodalValue_2_Z
        nodalValue_3_X nodalValue_3_Y nodalValue_3_Z
        ...

    CELL_DATA (nx-1) x (ny-1) x (nz-1)

    SCALARS myCellField1 float
    LOOKUP_TABLE default
        cellValue_1
        cellValue_2
        cellValue_3
        ...

where nx, ny and nz are the number of nodes in each axis, lx, ly, lz, the mesh length in each axis and ox, oy, oz the spatial postiion of the origin.

"""


def computeStrainField(dispalcementField, aspectRatio=[1.0, 1.0, 1.0], onlyDiag=False):
    """
    Compute the strain field from a displacement field.

    The strain is computed in the centre of the cell
    using order one shape functions under the hypothesis of small strain.

    Parameters
    ----------
        nodalVectorField: array float
            The nodal vector field to compute the derivatives.
            Its shape is (nz, ny, nx, 3).
        aspectRatio : array float
            Length between two nodes in every direction e.g. size of a cell. Default value: [1, 1, 1]
        onlyDiag : bool, default=False
            If True returns only the diagonal term of the derivatives.

    Returns
    -------
        diagStrainField: array
            The diagonal part of the field (returned if ``onlyDiag=True``).
            Its shape is (nz, ny, nx, 3)
        fullStrainField: array
            The full strain field of 3x3 matrices (returned if ``onlyDiag=False``).
            Its shape is (nz, ny, nx, 3, 3)

    Example
    -------
        >>> import spam.helpers
        >>> fields = spam.helpers.readStructuredVTK("myFields.vtk")
        fields['myVectorFields'] is a (nz, ny, nx, 3) vector fields
        >>> strain     = spam.mesh.computeStrainField(fields['myVectorFields'])
        ouput the full 3x3 matrices field
        >>> diagStrain = spam.mesh.computeStrainField(fields['myVectorFields'], onlyDiag=True)
        output a vector field made of the diagonal of the 3x3 strain

    WARNING
    -------
        This function deals with structured mesh thus ``x`` and ``z`` axis are swapped **in python**.

    """
    import numpy

    # define dimensions
    nNodes = [n for n in dispalcementField.shape[0:3]]
    nCells = [n-1 for n in nNodes]

    # we only keep _xx, _yy and _zz componants of the derivatives
    diagStrainField = numpy.zeros((nCells[0], nCells[1], nCells[2], 3))
    # the full 3x3 strain field
    fullStrainField = numpy.zeros((nCells[0], nCells[1], nCells[2], 3, 3))

    # loop over the cells
    for kCell in range(nCells[0]):
        for jCell in range(nCells[1]):
            for iCell in range(nCells[2]):
                # nodal field values corresponding to the cell
                lid = numpy.zeros((8, 3)).astype('<u1')  # local index
                lid[0] = [0, 0, 0]
                lid[1] = [0, 0, 1]
                lid[2] = [0, 1, 0]
                lid[3] = [0, 1, 1]
                lid[4] = [1, 0, 0]
                lid[5] = [1, 0, 1]
                lid[6] = [1, 1, 0]
                lid[7] = [1, 1, 1]

                subDerivativeVoigt = numpy.zeros(6)
                for a in range(8):
                    # get field value
                    d = dispalcementField[int(kCell+lid[a, 0]), int(jCell+lid[a, 1]), int(iCell+lid[a, 2]), :]
                    # local node coordinates
                    locZ = 0.5*(float(lid[a, 0])-0.5)
                    locY = 0.5*(float(lid[a, 1])-0.5)
                    locX = 0.5*(float(lid[a, 2])-0.5)
                    # jacobian from local to global base
                    jacZ = 2.0/float(aspectRatio[0])
                    jacY = 2.0/float(aspectRatio[1])
                    jacX = 2.0/float(aspectRatio[2])
                    # create B matrix
                    Ba = numpy.zeros((6, 3))
                    Ba[0, 0] = jacZ * locZ / 8.0
                    Ba[1, 1] = jacY * locY / 8.0
                    Ba[2, 2] = jacX * locX / 8.0
                    Ba[3, 0] = jacY * locY / 8.0
                    Ba[3, 1] = jacZ * locZ / 8.0
                    Ba[4, 1] = jacX * locX / 8.0
                    Ba[4, 2] = jacY * locY / 8.0
                    Ba[5, 0] = jacX * locX / 8.0
                    Ba[5, 2] = jacZ * locZ / 8.0
                    # compute strain
                    subDerivativeVoigt += numpy.dot(Ba, d)

                # fill the fields array
                diagStrainField[kCell, jCell, iCell, :] = subDerivativeVoigt[0:3]
                fullStrainField[kCell, jCell, iCell, 0, 0] = 0.5*subDerivativeVoigt[0]  # eps_zz: coef 0.5 since eps <- eps + eps.T
                fullStrainField[kCell, jCell, iCell, 1, 1] = 0.5*subDerivativeVoigt[1]  # eps_yy: coef 0.5 since eps <- eps + eps.T
                fullStrainField[kCell, jCell, iCell, 2, 2] = 0.5*subDerivativeVoigt[2]  # eps_zz: coef 0.5 since eps <- eps + eps.T
                fullStrainField[kCell, jCell, iCell, 0, 1] = 0.5*subDerivativeVoigt[3]  # eps_zy: coef 0.5 factor 2 voigt notation
                fullStrainField[kCell, jCell, iCell, 1, 2] = 0.5*subDerivativeVoigt[4]  # eps_yx: coef 0.5 factor 2 voigt notation
                fullStrainField[kCell, jCell, iCell, 0, 2] = 0.5*subDerivativeVoigt[5]  # eps_zx: coef 0.5 factor 2 voigt notation
                fullStrainField[kCell, jCell, iCell, :, :] += fullStrainField[kCell, jCell, iCell, :, :].T

    if onlyDiag:
        return diagStrainField
    else:
        return fullStrainField


def createCylindricalMask(shape, radius, voxSize=1.0, centre=None):
    """
        Create a image mask of a cylinder in the z direction.

        Parameters
        ----------
            shape: array, int
                The shape of the array the where the cylinder is saved
            radius: float
                The radius of the cylinder
            voxSize: float (default=1.0)
                The physical size of a voxel
            centre: array of floats of size 2, (default None)
                The center [y,x] of the axis of rotation of the cylinder.
                If None it is taken to be the centre of the array.

        Returns
        -------
            cyl: array, int
                The cylinder

    """
    import numpy

    cyl = numpy.zeros(shape).astype('<u1')

    if centre is None:
        centre = [float(shape[1])/2.0, float(shape[2])/2.0]

    for iy in range(cyl.shape[1]):
        y = (float(iy)+0.5)*float(voxSize)
        for ix in range(cyl.shape[2]):
            x = (float(ix)+0.5)*float(voxSize)
            dist = numpy.sqrt((x-centre[1])**2 + (y-centre[0])**2)
            if dist < radius:
                cyl[:, iy, ix] = 1

    return cyl


def structuringElement(radius=1, order=2, margin=0, dim=3):
    """This function construct a structural element.

    Parameters
    -----------
        radius : int, default=1
            The `radius` of the structural element

            .. code-block:: text

                radius = 1 gives 3x3x3 arrays
                radius = 2 gives 5x5x5 arrays
                ...
                radius = n gives (2n+1)x(2n+1)x(2n+1) arrays

        order : int, default=2
            Defines the shape of the structuring element by setting the order of the norm
            used to compute the distance between the centre and the border.

            A representation for the slices of a 5x5x5 element (size=2) from the center to on corner (1/8 of the cube)

            .. code-block:: text

                order=numpy.inf: the cube
                1 1 1    1 1 1    1 1 1
                1 1 1    1 1 1    1 1 1
                1 1 1    1 1 1    1 1 1

                order=2: the sphere
                1 0 0    0 0 0    0 0 0
                1 1 0    1 1 0    0 0 0
                1 1 1    1 1 0    1 0 0

                order=1: the diamond
                1 0 0    0 0 0    0 0 0
                1 1 0    1 0 0    0 0 0
                1 1 1    1 1 0    1 0 0

        margin : int, default=0
            Gives a 0 valued margin of size margin.

        dim : int, default=3
            Spatial dimension (2 or 3).

    Returns
    --------
        array
            The structural element
    """
    import numpy

    tb = tuple([2*radius+2*margin+1 for _ in range(dim)])
    ts = tuple([2*radius+1 for _ in range(dim)])
    c = numpy.abs(numpy.indices(ts) - radius)
    d = numpy.zeros(tb)
    s = [slice(margin, margin+2*radius+1) for _ in range(dim)]
    d[s] = numpy.power(numpy.sum(numpy.power(c, order), axis=0), 1.0/float(order)) <= radius
    return d.astype('<u1')


def createLexicoCoordinates(lenghts, nNodes, origin=(0, 0, 0)):
    """Create a list of coordinates following the lexicographical order.

    Parameters
    ----------
        lengths: array of floats
            The length of the cuboids in every directions.
        nNodes: array of int
            The number of nodes of the mesh in every directions.
        origin: array of floats
            The coordinates of the origin of the mesh.

    Returns
    -------
        array
            The list of coordinates. ``shape=(nx*ny*nz, 3)``

    """
    import numpy

    x = numpy.linspace(origin[0], lenghts[0]+origin[0], nNodes[0])
    y = numpy.linspace(origin[1], lenghts[1]+origin[1], nNodes[1])
    z = numpy.linspace(origin[2], lenghts[2]+origin[2], nNodes[2])
    cx = numpy.tile(x, (1, nNodes[1]*nNodes[2]))
    cy = numpy.tile(numpy.sort(numpy.tile(y, (1, nNodes[0]))), (1, nNodes[2]))
    cz = numpy.sort(numpy.tile(z, (1, nNodes[0]*nNodes[1])))
    return numpy.transpose([cx[0], cy[0], cz[0]])
