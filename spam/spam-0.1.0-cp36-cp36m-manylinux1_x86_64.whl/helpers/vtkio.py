"""This module offers a set functions in order to read and writes VTK files.

This module is mainly made of ``meshio`` wrappers adapted to ``spam``.
The types of data currently handled are:

    * Structured meshes of cuboids
    * Unstructured meshes of tetrahedrs
    * List of objects (TODO)

WARNING
-------
    Python dependencies
        * ``meshio``

"""


# Structured meshes

def readStructuredVTK(f, fieldAsked=None, zFirst=True):
    """Read a plain text VTK.

    By default read the full text and put all fields in a dictionnay.
    Specific fields can be selected with `fieldAsked`.

    Parameters
    ----------
        f : string
            Name of the VTK file.
        fieldAsked : array of string, default=None
            List of the field names.
        zFirst : bool, default=True
            Switch the x and z axis for the vector valued fields.

    Returns
    -------
        fields : dict
            Dictionnary of all the fields without nodal or cell distinctions.

        .. code-block:: python

            fields = { 'field1name':[field1value1, field1value2, ...],
                       'field2name':[field2value1, field2value2, ...],
                       ...}

    Note
    ----
        The ouputs are kept flattened.

    """
    import numpy

    # read the full file
    with open(f) as content_file:
        content = [l.strip() for l in content_file if l.strip()]

    # find line numbers of principal key words
    pl = {l.split()[0]: i
          for i, l in enumerate(content)
          if l.split()[0] in ['CELLS', 'POINTS', 'CELL_DATA', 'POINT_DATA']}

    # find keys in the file
    nl = {}
    keys_found = {}
    if('POINT_DATA' in pl):
        nl.update({'POINT_DATA': int(content[pl['POINT_DATA']].split()[1])})
        keys_found.update({l.split()[1]: [pl['POINT_DATA']+i, content[pl['POINT_DATA']+i].split()[0], 'POINT_DATA'] for i, l in enumerate(content[pl['POINT_DATA']:]) if l.split()[0] in ['SCALARS', 'VECTORS', 'TENSORS']})

    # not used in regular mesh (implicit node position)
    #if('POINTS' in pl):
        #nl.update({'POINTS': int(content[pl['POINTS']].split()[1])})
        #keys_found.update({'POINTS': [pl['POINTS'], 'VECTORS', 'POINTS']})

    if('CELL_DATA' in pl):
        nl.update({'CELL_DATA': int(content[pl['CELL_DATA']].split()[1])})
        keys_found.update({l.split()[1]: [pl['CELL_DATA']+i, content[pl['CELL_DATA']+i].split()[0], 'CELL_DATA'] for i, l in enumerate(content[pl['CELL_DATA']:]) if l.split()[0] in ['SCALARS', 'VECTORS', 'TENSORS']})

    # not used in regular mesh (implicit connectivity)
    #if('CELLS' in pl):
        #nl.update({'CELLS': int(content[pl['CELLS']].split()[1])})
        #keys_found.update({'CELLS': [pl['CELLS'], 'TETRA', 'CELLS']})

    # get relevent keys
    if fieldAsked is None:
        keys_valid = keys_found
    elif isinstance(fieldAsked, list):
        keys_valid = {k: keys_found[k] for k in fieldAsked if k in keys_found}
    elif isinstance(fieldAsked, str) and fieldAsked in keys_found:
        keys_valid = {fieldAsked: keys_found[fieldAsked]}
    else:
        keys_valid = {}

    # fill output
    fields = {}
    for l in keys_valid.items():
        dict_skip = {
            'CELLS':      {'TETRA':  1},
            'POINTS':     {'VECTORS': 1},
            'CELL_DATA':  {'SCALARS': 2, 'VECTORS': 1, 'TENSORS': 1},
            'POINT_DATA': {'SCALARS': 2, 'VECTORS': 1, 'TENSORS': 1}
            }
        l_skip = dict_skip[l[1][2]][l[1][1]]
        l_start = l_skip+l[1][0]
        l_end = l_start+nl[l[1][2]]
        # hack for the scalar case to avoir list of single element lists
        if l[1][1] == 'SCALARS':
            fields.update({l[0]: numpy.array([float(r) for r in content[l_start:l_end]])})
        else:
            if zFirst is True:
                fields.update({l[0]: numpy.array([[float(c) for c in reversed(r.split())] for r in content[l_start:l_end]])})
            else:
                fields.update({l[0]: numpy.array([[float(c) for c in (r.split())] for r in content[l_start:l_end]])})

    return fields


def writeStructuredVTK(aspectRatio=[1.0, 1.0, 1.0],
                       origin=[0.0, 0.0, 0.0],
                       cellData={},
                       pointData={},
                       fileName='spam.vtk'):
    """Write a plain text regular grid vtk from:

         * 3D arrays for 3D scalar fields
         * 4D arrays for 3D vector fields

    Parameters
    ----------
        aspectRatio : size 3 array float, default=[1, 1, 1]
            Length between two nodes in every direction e.g. size of a cell.
        origin : size 3 array float, default=[0, 0, 0]
            Origin of the grid.
        cellData : dict ``{'field1name':field1,'field2name':field2, ...}``
            Cell fields, not interpolated by paraview.
            The field values are reshaped into a flat array in the lexicographic order.
            ``field1`` and ``field2`` are ndimensional array (3D arrays are scalar fields and 4D array are vector valued fields).
        pointData : dict ``{'field1name':field1,'field2name':field2, ...}``
            Nodal fields, interpolated by paraview. ``pointData`` has the same shape as ``cellData``.
        fileName : string, default='spam.vtk'
            Name of the output file.

    WARNING
    -------
        This function deals with structured mesh thus ``x`` and ``z`` axis are swapped **in python**.
    """

    # check dimensions

    dimensions = []

    if len(cellData)+len(pointData) == 0:
        print('Empty files. Not writing {}'.format(fileName))
        return 0

    if len(cellData):
        dimensionsCell = cellData.values()[0].shape[:3]
        for k, v in cellData.iteritems():
            if set(dimensionsCell) != set(v.shape[:3]):
                print('Unconsistent cell field sizes {} != {}'.format(dimensionsCell, v.shape[:3]))
                return 0
        dimensions = [n+1 for n in dimensionsCell]

    if len(pointData):
        dimensionsPoint = pointData.values()[0].shape[:3]
        for k, v in pointData.iteritems():
            if set(dimensionsPoint) != set(v.shape[:3]):
                print('Unconsistent point field sizes {} != {}'.format(dimensionsPoint, v.shape[:3]))
                return 0
        dimensions = dimensionsPoint

    if len(cellData) and len(pointData):
        if set([n+1 for n in dimensionsCell]) != set(dimensionsPoint):
            print('Unconsistent point VS cell field sizes. Point size should be +1 for each axis.')

    with open(fileName, 'w') as f:
        # header
        f.write('# vtk DataFile Version 2.0\n')
        f.write('VTK file from spam: {}\n'.format(fileName))
        f.write('ASCII\n\n')
        f.write('DATASET STRUCTURED_POINTS\n')
        f.write('DIMENSIONS {} {} {}\n'.format(*reversed(dimensions)))
        f.write('ASPECT_RATIO {} {} {}\n'.format(*reversed(aspectRatio)))
        f.write('ORIGIN {} {} {}\n\n'.format(*reversed(origin)))

        # pointData
        if len(pointData) == 1:
            f.write('POINT_DATA {}\n\n'.format(dimensions[0] * dimensions[1] * dimensions[2]))
            _writeFieldInVtk(pointData, f)
        elif len(pointData) > 1:
            f.write('POINT_DATA {}\n\n'.format(dimensions[0] * dimensions[1] * dimensions[2]))
            for k in pointData:
                _writeFieldInVtk({k: pointData[k]}, f)

        # cellData
        if len(cellData) == 1:
            f.write('CELL_DATA {}\n\n'.format((dimensions[0]-1) * (dimensions[1]-1) * (dimensions[2]-1)))
            _writeFieldInVtk(cellData, f)
        elif len(cellData) > 1:
            f.write('CELL_DATA {}\n\n'.format((dimensions[0]-1) * (dimensions[1]-1) * (dimensions[2]-1)))
            for k in cellData:
                _writeFieldInVtk({k: cellData[k]}, f)

        f.write('\n')

def writeGlyphsVTK(coordinates,
                   pointData,
                   fileName='spam.vtk'):
    """Write a plain text glyphs vtk.

    Parameters
    ----------
        coordinates : ``n`` by 3 array of float
            Coordinates of the centre of all ``n`` glyphs
        pointData : dict ``{'field1name':field1,'field2name':field2, ...}``
            Value attached to each glyph.
            ``field1`` and ``field2`` are ``n`` by 1 arrays for scalar values and ``n`` by 3 for vector values.
        fileName : string, default='spam.vtk'
            Name of the output file.

    WARNING
    -------
        This function deals with structured mesh thus ``x`` and ``z`` axis are swapped **in python**.
    """

    # check dimensions

    dimension = coordinates.shape[0]

    if len(pointData):
        for k, v in pointData.iteritems():
            if dimension != v.shape[0]:
                print('Unconsistent point field sizes {} != {}'.format(dimension, v.shape[0]))
                return 0
    else:
        print('Empty files. Not writing {}'.format(fileName))
        return

    with open(fileName, 'w') as f:
        # header
        f.write('# vtk DataFile Version 2.0\n')
        # f.write('VTK file from spam: {}\n'.format(fileName))
        f.write('Unstructured grid legacy vtk file with point scalar data\n')
        f.write('ASCII\n\n')

        # coordinates
        f.write('DATASET UNSTRUCTURED_GRID\n')
        f.write('POINTS {:.0f} float\n'.format(dimension))
        for coord in coordinates:
            f.write('    {} {} {}\n'.format(*reversed(coord)))
        f.write('\n')

        # pointData
        if len(pointData) == 1:
            f.write('POINT_DATA {}\n\n'.format(dimension))
            _writeFieldInVtk(pointData, f, flat=True)
        elif len(pointData) > 1:
            f.write('POINT_DATA {}\n\n'.format(dimension))
            for k in pointData:
                _writeFieldInVtk({k: pointData[k]}, f, flat=True)

        f.write('\n')

def _writeFieldInVtk(data, f, flat=False):
    """Private helper function for writing vtk fields
    """

    for key in data:
        field = data[key]


        if flat:
            # SCALAR flatten (n by 1)
            if(len(field.shape) == 1):
                f.write('SCALARS {} float\n'.format(key.replace(" ", "_")))
                f.write('LOOKUP_TABLE default\n')
                for item in field:
                    f.write('    {}\n'.format(item))
                f.write('\n')

            # VECTORS flatten (n by 3)
            elif(len(field.shape) == 2 and field.shape[1] == 3):
                f.write('VECTORS {} float\n'.format(key.replace(" ", "_")))
                for item in field:
                    f.write('    {} {} {}\n'.format(*reversed(item)))
                f.write('\n')

        else:
            # SCALAR not flatten (n1 by n2 by n3)
            if(len(field.shape) == 3):
                f.write('SCALARS {} float\n'.format(key.replace(" ", "_")))
                f.write('LOOKUP_TABLE default\n')
                for item in field.reshape(-1):
                    f.write('    {}\n'.format(item))
                f.write('\n')

            # VECTORS (n1 by n2 by n3 by 3)
            elif(len(field.shape) == 4 and field.shape[3] == 3):
                f.write('VECTORS {} float\n'.format(key.replace(" ", "_")))
                for item in field.reshape((field.shape[0]*field.shape[1]*field.shape[2], field.shape[3])):
                    f.write('    {} {} {}\n'.format(*reversed(item)))
                f.write('\n')

            # TENSORS (n1 by n2 by n3 by 3 by 3)
            elif(len(field.shape) == 5 and field.shape[3]*field.shape[4] == 9):
                f.write('TENSORS {} float\n'.format(key.replace(" ", "_")))
                for item in field.reshape((field.shape[0]*field.shape[1]*field.shape[2], field.shape[3]*field.shape[4])):
                    f.write('    {} {} {}\n    {} {} {}\n    {} {} {}\n\n'.format(*reversed(item)))
                f.write('\n')


# Untructured meshes

def writeUnstructuredVTK(points,
                         connectivity,
                         elementType='tetra',
                         pointData={},
                         cellData={},
                         fileFormat='vtk-binary',
                         fileName='spam.vtk'):
    """Write a binary VTK using ``meshio`` selecting only the tetrahedra.

    Parameters
    ----------
        points : array
            The list of node coordinates.
        connectivity : array
            The connectivity matrix (cell id starts at 0).
        elementType : string, optional default='tetra'
            The type of element used for the mesh.
        cellData : dict
            Cell fields, not interpolated by paraview.

            .. code-block:: python

                cellData = { 'field1name':field1,'field2name':field2 ...}

            where field1 and field2 are 1D or 2D arrays. 1D arrays are scalar fields and 2D array are vector valued fields.
        pointData : dict
            Nodal fields, interpolated by paraview. ``pointData`` has the same shape as ``cellData``.

            .. code-block:: python

                pointData = { 'field1name':field1,'field2name':field2 ...}

        fileFormat : string, default=``vtk-binary``
            ``meshio`` file_format option. Use ``vtk-ascii`` for clear text and ``vtk-binary`` for binary files.
        fileName : string, default='spam.vtk'
            Name of the output file.

    """
    import meshio
    meshio.write_points_cells(fileName, points, {elementType: connectivity}, point_data=pointData, cell_data={elementType: cellData},
                              file_format=fileFormat)


def readUnstructuredVTK(fileName):
    """
    Read a binary VTK using ``meshio`` selecting only the tetrahedra.

    Parameters
    ----------
        fileName : string
            Name of the input file.

    Returns
    -------
        points : array
            The list of node coordinates.
        connectivity : array
            The connectivity matrix (cell id starts at 0).
        pointData : dict
            Nodal fields, interpolated by paraview.
        cellData : dict
            Cell fields, not interpolated by paraview.

    """
    import meshio
    mesh = meshio.read(fileName)
    connectivity = mesh.cells['tetra']
    cell_data = mesh.cell_data['tetra']
    return mesh.points, connectivity, mesh.point_data, cell_data
