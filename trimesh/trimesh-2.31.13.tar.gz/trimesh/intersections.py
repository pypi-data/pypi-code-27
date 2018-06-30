"""
intersections.py
------------------

Primarily mesh-plane intersections (slicing).
"""
import numpy as np

from .constants import log, tol

from . import util
from . import geometry
from . import grouping
from . import transformations


def mesh_plane(mesh,
               plane_normal,
               plane_origin,
               return_faces=False,
               cached_dots=None):
    """
    Find a the intersections between a mesh and a plane,
    returning a set of line segments on that plane.

    Parameters
    ---------
    mesh : Trimesh object
        Source mesh to slice
    plane_normal : (3,) float
        Normal vector of plane to intersect with mesh
    plane_origin:  (3,) float
        Point on plane to intersect with mesh
    return_faces:  bool
        If True return face index each line is from
    cached_dots : (n, 3) float
        If an external function has stored dot
        products pass them here to avoid recomputing

    Returns
    ----------
    lines :  (m, 2, 3) float
        List of 3D line segments in space
    face_index : (m,) int
        Index of mesh.faces for each line
        Only returned if return_faces was True
    """

    def triangle_cases(signs):
        """
        Figure out which faces correspond to which intersection
        case from the signs of the dot product of each vertex.
        Does this by bitbang each row of signs into an 8 bit
        integer.

        code : signs      : intersects
        0    : [-1 -1 -1] : No
        2    : [-1 -1  0] : No
        4    : [-1 -1  1] : Yes; 2 on one side, 1 on the other
        6    : [-1  0  0] : Yes; one edge fully on plane
        8    : [-1  0  1] : Yes; one vertex on plane, 2 on different sides
        12   : [-1  1  1] : Yes; 2 on one side, 1 on the other
        14   : [0 0 0]    : No (on plane fully)
        16   : [0 0 1]    : Yes; one edge fully on plane
        20   : [0 1 1]    : No
        28   : [1 1 1]    : No

        Parameters
        ----------
        signs: (n,3) int, all values are -1,0, or 1
               Each row contains the dot product of all three vertices
               in a face with respect to the plane

        Returns
        ---------
        basic:      (n,) bool, which faces are in the basic intersection case
        one_vertex: (n,) bool, which faces are in the one vertex case
        one_edge:   (n,) bool, which faces are in the one edge case
        """

        signs_sorted = np.sort(signs, axis=1)
        coded = np.zeros(len(signs_sorted), dtype=np.int8) + 14
        for i in range(3):
            coded += signs_sorted[:, i] << 3 - i

        # one edge fully on the plane
        # note that we are only accepting *one* of the on- edge cases,
        # where the other vertex has a positive dot product (16) instead
        # of both on- edge cases ([6,16])
        # this is so that for regions that are co-planar with the the section plane
        # we don't end up with an invalid boundary
        key = np.zeros(29, dtype=np.bool)
        key[16] = True
        one_edge = key[coded]

        # one vertex on plane, other two on different sides
        key[:] = False
        key[8] = True
        one_vertex = key[coded]

        # one vertex on one side of the plane, two on the other
        key[:] = False
        key[[4, 12]] = True
        basic = key[coded]

        return basic, one_vertex, one_edge

    def handle_on_vertex(signs, faces, vertices):
        # case where one vertex is on plane, two are on different sides
        vertex_plane = faces[signs == 0]
        edge_thru = faces[signs != 0].reshape((-1, 2))
        point_intersect, valid = plane_lines(plane_origin,
                                             plane_normal,
                                             vertices[edge_thru.T],
                                             line_segments=False)
        lines = np.column_stack((vertices[vertex_plane[valid]],
                                 point_intersect)).reshape((-1, 2, 3))
        return lines

    def handle_on_edge(signs, faces, vertices):
        # case where two vertices are on the plane and one is off
        edges = faces[signs == 0].reshape((-1, 2))
        points = vertices[edges]
        return points

    def handle_basic(signs, faces, vertices):
        # case where one vertex is on one side and two are on the other
        unique_element = grouping.unique_value_in_row(
            signs, unique=[-1, 1])
        edges = np.column_stack(
            (faces[unique_element],
             faces[np.roll(unique_element, 1, axis=1)],
             faces[unique_element],
             faces[np.roll(unique_element, 2, axis=1)])).reshape(
            (-1, 2))
        intersections, valid = plane_lines(plane_origin,
                                           plane_normal,
                                           vertices[edges.T],
                                           line_segments=False)
        # since the data has been pre- culled, any invalid intersections at all
        # means the culling was done incorrectly and thus things are
        # mega-fucked
        assert valid.all()
        return intersections.reshape((-1, 2, 3))

    # check input plane
    plane_normal = np.asanyarray(plane_normal,
                                 dtype=np.float64)
    plane_origin = np.asanyarray(plane_origin,
                                 dtype=np.float64)
    if plane_origin.shape != (3,) or plane_normal.shape != (3,):
        raise ValueError('Plane origin and normal must be (3,)!')

    if cached_dots is not None:
        dots = cached_dots
    else:
        # dot product of each vertex with the plane normal indexed by face
        # so for each face the dot product of each vertex is a row
        # shape is the same as mesh.faces (n,3)
        dots = np.dot(plane_normal,
                      (mesh.vertices - plane_origin).T)[mesh.faces]

    # sign of the dot product is -1, 0, or 1
    # shape is the same as mesh.faces (n,3)
    signs = np.zeros(mesh.faces.shape, dtype=np.int8)
    signs[dots < -tol.merge] = -1
    signs[dots > tol.merge] = 1

    # figure out which triangles are in the cross section,
    # and which of the three intersection cases they are in
    cases = triangle_cases(signs)
    # handlers for each case
    handlers = (handle_basic,
                handle_on_vertex,
                handle_on_edge)

    # the (m, 2, 3) line segments
    lines = np.vstack([h(signs[c],
                         mesh.faces[c],
                         mesh.vertices)
                       for c, h in zip(cases, handlers)])

    log.debug('mesh_cross_section found %i intersections',
              len(lines))

    if return_faces:
        face_index = np.hstack([np.nonzero(c)[0] for c in cases])
        return lines, face_index
    return lines


def mesh_multiplane(mesh,
                    plane_origin,
                    plane_normal,
                    heights):
    """
    A utility function for slicing a mesh by multiple
    parallel planes, which caches the dot product operation.

    Parameters
    -------------
    mesh : trimesh.Trimesh
        Geometry to be sliced by planes
    plane_normal : (3,) float
        Normal vector of plane
    plane_origin : (3,) float
        Point on a plane
    heights : (m,) float
        Offset distances from plane to slice at

    Returns
    --------------
    lines : (m,) sequence of (n, 2, 2) float
        Lines in space for m planes
    to_3D : (m, 4, 4) float
        Transform to move each section back to 3D
    face_index : (m,) sequence of (n,) int
        Indexes of mesh.faces for each segment
    """
    # check input plane
    plane_normal = util.unitize(plane_normal)
    plane_origin = np.asanyarray(plane_origin,
                                 dtype=np.float64)
    heights = np.asanyarray(heights, dtype=np.float64)

    # dot product of every vertex with plane
    vertex_dots = np.dot(plane_normal,
                         (mesh.vertices - plane_origin).T)

    # reconstruct transforms for each 2D section
    base_transform = geometry.plane_transform(origin=plane_origin,
                                              normal=plane_normal)
    # alter translation Z inside loop
    translation = np.eye(4)

    # store results
    transforms = []
    face_index = []
    segments = []

    # loop through user specified heights
    for height in heights:
        # offset the origin by the height
        new_origin = plane_origin + (plane_normal * height)
        # offset the dot products by height and index by faces
        new_dots = (vertex_dots - height)[mesh.faces]
        # run the intersection with the cached dot products
        lines, index = mesh_plane(mesh=mesh,
                                  plane_origin=new_origin,
                                  plane_normal=plane_normal,
                                  return_faces=True,
                                  cached_dots=new_dots)

        # get the transforms to 3D space and back
        translation[2, 3] = height
        to_3D = np.dot(base_transform, translation)
        to_2D = np.linalg.inv(to_3D)
        transforms.append(to_3D)

        # transform points to 2D frame
        lines_2D = transformations.transform_points(
            lines.reshape((-1, 3)),
            to_2D)

        # if we didn't screw up the transform all
        # of the Z values should be zero
        assert np.allclose(lines_2D[:, 2], 0.0)

        # reshape back in to lines and discard Z
        lines_2D = lines_2D[:, :2].reshape((-1, 2, 2))
        # store (n, 2, 2) float lines
        segments.append(lines_2D)
        # store (n,) int indexes of mesh.faces
        face_index.append(face_index)

    # (n, 4, 4) transforms from 2D to 3D
    transforms = np.array(transforms, dtype=np.float64)

    return segments, transforms, face_index


def plane_lines(plane_origin,
                plane_normal,
                endpoints,
                line_segments=True):
    """
    Calculate plane-line intersections

    Parameters
    ---------
    plane_origin : (3,) float
        Point on plane
    plane_normal : (3,) float
        Plane normal vector
    endpoints : (2, n, 3) float
        Points defining lines to be tested
    line_segments : bool
        If True, only returns intersections as valid if
        vertices from endpoints are on different sides
        of the plane.

    Returns
    ---------
    intersections : (m, 3) float
        Cartesian intersection points
    valid : (n, 3) bool
        Indicate whether a valid intersection exists
        for each input line segment
    """
    endpoints = np.asanyarray(endpoints)
    plane_origin = np.asanyarray(plane_origin).reshape(3)
    line_dir = util.unitize(endpoints[1] - endpoints[0])
    plane_normal = util.unitize(np.asanyarray(plane_normal).reshape(3))

    t = np.dot(plane_normal, (plane_origin - endpoints[0]).T)
    b = np.dot(plane_normal, line_dir.T)

    # If the plane normal and line direction are perpendicular, it means
    # the vector is 'on plane', and there isn't a valid intersection.
    # We discard on-plane vectors by checking that the dot product is nonzero
    valid = np.abs(b) > tol.zero
    if line_segments:
        test = np.dot(plane_normal,
                      np.transpose(plane_origin - endpoints[1]))
        different_sides = np.sign(t) != np.sign(test)
        nonzero = np.logical_or(np.abs(t) > tol.zero,
                                np.abs(test) > tol.zero)
        valid = np.logical_and(valid, different_sides)
        valid = np.logical_and(valid, nonzero)

    d = np.divide(t[valid], b[valid])
    intersection = endpoints[0][valid]
    intersection += np.reshape(d, (-1, 1)) * line_dir[valid]

    return intersection, valid


def planes_lines(plane_origins,
                 plane_normals,
                 line_origins,
                 line_directions):
    """
    Given one line per plane, find the intersection points.

    Parameters
    -----------
    plane_origins : (n,3) float
        Point on each plane
    plane_normals : (n,3) float
        Normal vector of each plane
    line_origins : (n,3) float
        Point at origin of each line
    line_directions : (n,3) float
        Direction vector of each line

    Returns
    ----------
    on_plane : (n,3) float
        Points on specified planes
    valid : (n,) bool
        Did plane intersect line or not
    """

    # check input types
    plane_origins = np.asanyarray(plane_origins, dtype=np.float64)
    plane_normals = np.asanyarray(plane_normals, dtype=np.float64)
    line_origins = np.asanyarray(line_origins, dtype=np.float64)
    line_directions = np.asanyarray(line_directions, dtype=np.float64)

    # vector from line to plane
    origin_vectors = plane_origins - line_origins

    projection_ori = util.diagonal_dot(origin_vectors, plane_normals)
    projection_dir = util.diagonal_dot(line_directions, plane_normals)

    valid = np.abs(projection_dir) > tol.merge

    distance = np.divide(projection_ori[valid],
                         projection_dir[valid])

    on_plane = line_directions[valid] * distance.reshape((-1, 1))
    on_plane += line_origins[valid]

    return on_plane, valid
