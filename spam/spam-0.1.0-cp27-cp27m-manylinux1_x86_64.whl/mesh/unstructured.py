"""This module offers a set of tools for unstructured 3D meshes made of tetrahedra.

>>> # import module
>>> import spam.mesh.unstructured as umesh


WARNING
-------
    System dependencies
        * ``gmsh``
    Python dependencies
        * ``pygmsh``
        * ``meshio``
"""


def createCuboid(lengths, lcar, gmshFile=None, vtkFile=None):
    """
    Create an unstructured mesh of tetrahedra inside a cuboid.

    Parameters
    ----------
        lengths: array
            The three lengths of the cube.
        lcar: float
             length of the mesh.
            The avarage distance between two nodes.
        gmshFile: string, default=None,
            If not None, save the clear text gmsh file with name ``gmshFile`` and suffix ``.msh``.
        vtkFile: string, default=None,
            If not None, save the clear text vtk file with name ``vtkFile`` and suffix ``.vtk``.

    Returns
    -------
        points: array
            The coordinates of all the points.
        connectivity: array
            The connectivity matrix of the tetrahedra

    Example
    -------
        >>> points, connectivity = umesh.createCuboid((1.0,1.5,2.0), 0.5)
        create a mesh in a cuboid of size 1,1.5,2 with a characteristic length of 0.5
    """

    import pygmsh
    import meshio

    # create geometry
    lx, ly, lz = lengths
    geom = pygmsh.built_in.Geometry()
    poly = geom.add_polygon([[0.,  ly, 0.],
                             [lx,  ly, 0.],
                             [lx,  0., 0.],
                             [0.,  0., 0.]], lcar=lcar)
    geom.extrude(poly, translation_axis=[0., 0., lz])

    # create mesh and get connectivity
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    connectivity = cells['tetra']

    # write gmsh/vtk file
    if gmshFile is not None:
        meshio.write_points_cells("{}.msh".format(gmshFile), points, cells, file_format='gmsh-ascii')
    if vtkFile is not None:
        meshio.write_points_cells("{}.vtk".format(vtkFile), points, {'tetra': connectivity}, file_format='vtk-ascii')

    return points, connectivity


def createCylinder(centre, radius, height, lcar, gmshFile=None, vtkFile=None):
    """
    Create an unstructured mesh of tetrahedra inside a cylinder.
    The height of the cylinder is along the z axis.

    Parameters
    ----------
        centre: array
            The two (y,x) coordinates of the centre of the base disk.
        radius: float
            The radius of the base disk.
        height: float
            The height of the cylindre of the z direction.
        lcar: float
             length of the mesh.
            The avarage distance between two nodes.
        gmshFile: string, default=None,
            If not None, save the clear text gmsh file with name ``gmshFile`` and suffix ``.msh``.
        vtkFile: string, default=None,
            If not None, save the clear text vtk file with name ``vtkFile`` and suffix ``.vtk``.

    Returns
    -------
        points: array
            The coordinates of all the points.
        connectivity: array
            The connectivity matrix of the tetrahedra

    Example
    -------
        >>> points, connectivity = umesh.createCylinder((0.0,0.0), 0.5, 2.0, 0.5)
        create a mesh in a cylindre of centre 0,0,0 radius, 0.5 and height 2.0 with a characteristic length of 0.5
    """

    import pygmsh

    # unpack
    cy, cx = centre
    r = radius

    # raw code
    code = []
    code.append("Point(1) = {{ {x}, {y},  0, {lcar} }};".format(x=cx,   y=cy,   lcar=lcar))
    code.append("Point(2) = {{ {x}, {y},  0, {lcar} }};".format(x=cx+r, y=cy,   lcar=lcar))
    code.append("Point(3) = {{ {x}, {y},  0, {lcar} }};".format(x=cx,   y=cy+r, lcar=lcar))
    code.append("Point(4) = {{ {x}, {y},  0, {lcar} }};".format(x=cx-r, y=cy,   lcar=lcar))
    code.append("Point(5) = {{ {x}, {y},  0, {lcar} }};".format(x=cx,   y=cy-r, lcar=lcar))
    code.append("Circle(1) = { 2, 1, 3 };")
    code.append("Circle(2) = { 3, 1, 4 };")
    code.append("Circle(3) = { 4, 1, 5 };")
    code.append("Circle(4) = { 5, 1, 2 };")
    code.append("Line Loop(5) = { 1, 2, 3, 4 };")
    code.append("Plane Surface(6) = { 5 };")
    code.append("Extrude {{ 0, 0, {h} }} {{ Surface{{ 6 }}; }}".format(h=height))

    # add raw code to geometry
    geom = pygmsh.built_in.Geometry()
    geom.add_raw_code(code)

    # mesh
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    connectivity = cells['tetra']

    # write gmsh/vtk file
    if gmshFile is not None:
        import meshio
        meshio.write_points_cells("{}.msh".format(gmshFile), points, cells, file_format='gmsh-ascii')
    if vtkFile is not None:
        meshio.write_points_cells("{}.vtk".format(vtkFile), points, {'tetra': connectivity}, file_format='vtk-ascii')

    return points, connectivity
