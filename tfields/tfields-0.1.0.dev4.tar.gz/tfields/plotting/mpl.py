"""
Matplotlib specific plotting
"""
import tfields

import numpy as np
import warnings
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d as plt3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.dates as dates
from itertools import cycle
import logging


def show():
    plt.show()


def gca(dim=None, **kwargs):
    """
    Forwarding to plt.gca but translating the dimension to projection
    correct dimension
    """
    if dim == 3:
        axis = plt.gca(projection='3d', **kwargs)
    else:
        axis = plt.gca(**kwargs)
        if dim != axis_dim(axis):
            if dim is not None:
                warnings.warn("You have another dimension set as gca."
                              "I will force the new dimension to return.")
                axis = plt.gcf().add_subplot(1, 1, 1, **kwargs)
    return axis


def upgrade_style(style, source, dest="~/.config/matplotlib/"):
    """
    Copy a style file at <origionalFilePath> to the <dest> which is the foreseen
    local matplotlib rc dir by default
    The style will be name <style>.mplstyle
    Args:
        style (str): name of style
        source (str): full path to mplstyle file to use
        dest (str): local directory to copy the file to. Matpotlib has to
            search this directory for mplstyle files!
    """
    styleExtension = 'mplstyle'
    path = tfields.lib.in_out.resolve(os.path.join(dest, style + '.' + styleExtension))
    source = tfields.lib.in_out.resolve(source)
    tfields.lib.in_out.cp(source, path)


def set_style(style='tfields', dest="~/.config/matplotlib/"):
    """
    Set the matplotlib style of name
    Important:
        Either you
    Args:
        style (str)
        dest (str): local directory to use file from. if None, use default maplotlib styles
    """
    if dest is None:
        path = style
    else:
        styleExtension = 'mplstyle'
        path = tfields.lib.in_out.resolve(os.path.join(dest, style + '.' + styleExtension))
    try:
        plt.style.use(path)
    except IOError:
        log = logging.getLogger()
        if style == 'tfields':
            log.warning("I will copy the default style to {dest}."
                        .format(**locals()))
            source = os.path.join(os.path.dirname(__file__),
                                  style + '.' + styleExtension)
            upgrade_style(style, source, dest)
            set_style(style)
        else:
            log.error("Could not set style {path}. Probably you would want to"
                      "call tfields.plotting.upgrade_style(<style>, "
                      "<path to mplstyle file that should be copied>)"
                      "once".format(**locals()))


def save(path, *fmts, **kwargs):
    """
    Args:
        path (str): path without extension to save to
        *fmts (str): format of the figure to save. If multiple are given, create
            that many files
        **kwargs:
            axis
            fig
    """
    log = logging.getLogger()

    # catch figure from axis or fig
    axis = kwargs.get('axis', None)
    if axis is None:
        fig_default = plt.gcf()
        axis = gca()
        if fig_default is None:
            raise ValueError("fig_default may not be None")
    else:
        fig_default = axis.figure
    fig = kwargs.get('fig', fig_default)

    # set current figure
    plt.figure(fig.number)

    # crop the plot down based on the extents of the artists in the plot
    kwargs['bbox_inches'] = kwargs.pop('bbox_inches', 'tight')
    if kwargs['bbox_inches'] == 'tight':
        extra_artists = None
        for ax in fig.get_axes():
            first_label = ax.get_legend_handles_labels()[0] or None
            if first_label:
                if not extra_artists:
                    extra_artists = []
                extra_artists.append(first_label)
        kwargs['bbox_extra_artists'] = kwargs.pop('bbox_extra_artists',
                                                  extra_artists)

    if len(fmts) != 0:
        for fmt in fmts:
            if path.endswith('.'):
                new_file_path = path + fmt
            elif '{fmt}' in path:
                new_file_path = path.format(**locals())
            else:
                new_file_path = path + '.' + fmt
            save(new_file_path, **kwargs)
    else:
        path = tfields.lib.in_out.resolve(path)
        log.info("Saving figure as {0}".format(path))
        plt.savefig(path,
                    **kwargs)


def plot_array(array, **kwargs):
    """
    Points3D plotting method.

    Args:
        axis (matplotlib.Axis) object
        xAxis (int): coordinate index that should be on xAxis
        yAxis (int): coordinate index that should be on yAxis
        zAxis (int or None): coordinate index that should be on zAxis.
            If it evaluates to None, 2D plot will be done.
        methodName (str): method name to use for filling the axis

    Returns:
        Artist or list of Artists (imitating the axis.scatter/plot behaviour).
        Better Artist not list of Artists
    """
    tfields.plotting.set_default(kwargs, 'methodName', 'scatter')
    po = tfields.plotting.PlotOptions(kwargs)

    labelList = po.pop('labelList', ['x (m)', 'y (m)', 'z (m)'])
    xAxis, yAxis, zAxis = po.getXYZAxis()
    tfields.plotting.set_labels(po.axis, *po.getSortedLabels(labelList))
    if zAxis is None:
        args = [array[:, xAxis],
                array[:, yAxis]]
    else:
        args = [array[:, xAxis],
                array[:, yAxis],
                array[:, zAxis]]
    artist = po.method(*args,
                       **po.plotKwargs)
    return artist


def plot_mesh(vertices, faces, **kwargs):
    """
    Args:
        axis (matplotlib axis)
        xAxis (int)
        yAxis (int)
        zAxis (int)
        edgecolor (color)
        color (color): if given, use this color for faces in 2D
        cmap
        vmin
        vmax
    """
    if faces.shape[0] == 0:
        warnings.warn("No faces to plot")
        return None
    if max(faces.flat) > vertices.shape[0]:
        raise ValueError("Some faces point to non existing vertices.")
    po = tfields.plotting.PlotOptions(kwargs)
    if po.dim == 2:
        full = True
        mesh = tfields.Mesh3D(vertices, faces=faces)
        xAxis, yAxis, zAxis = po.getXYZAxis()
        facecolors = po.retrieveChain('facecolors', 'color',
                                      default=0,
                                      keep=False)
        if full:
            # implementation that will sort the triangles by zAxis
            centroids = mesh.centroids()
            axesIndices = [0, 1, 2]
            axesIndices.pop(axesIndices.index(xAxis))
            axesIndices.pop(axesIndices.index(yAxis))
            zAxis = axesIndices[0]
            zs = centroids[:, zAxis]
            zs, faces, facecolors = tfields.lib.util.multi_sort(zs, faces,
                                                                facecolors)
            nFacesInitial = len(faces)
        else:
            # cut away "back sides" implementation
            directionVector = np.array([1., 1., 1.])
            directionVector[xAxis] = 0.
            directionVector[yAxis] = 0.
            normVectors = mesh.triangles().norms()
            dotProduct = np.dot(normVectors, directionVector)
            nFacesInitial = len(faces)
            faces = faces[dotProduct > 0]

        vertices = mesh

        po.plotKwargs['methodName'] = 'tripcolor'
        po.plotKwargs['triangles'] = faces

        """
        sort out color arguments
        """
        facecolors = po.formatColors(facecolors,
                                     fmt='norm',
                                     length=nFacesInitial)
        if not full:
            facecolors = facecolors[dotProduct > 0]
        po.plotKwargs['facecolors'] = facecolors

        d = po.plotKwargs
        d['xAxis'] = xAxis
        d['yAxis'] = yAxis
        artist = plot_array(vertices, **d)
    elif po.dim == 3:
        label = po.pop('label', None)
        color = po.retrieveChain('color', 'c', 'facecolors',
                                 default='grey',
                                 keep=False)
        color = po.formatColors(color,
                                fmt='rgba',
                                length=len(faces))
        nanMask = np.isnan(color)
        if nanMask.any():
            warnings.warn("nan found in colors. Removing the corresponding faces!")
            color = color[~nanMask]
            faces = faces[~nanMask]

        edgecolor = po.pop('edgecolor', None)
        alpha = po.pop('alpha', None)
        po.delNormArgs()

        triangles = np.array([vertices[face] for face in faces])
        artist = plt3D.art3d.Poly3DCollection(triangles, **po.plotKwargs)
        po.axis.add_collection3d(artist)

        if edgecolor is not None:
            artist.set_edgecolor(edgecolor)
            artist.set_facecolors(color)
        else:
            artist.set_color(color)

        if alpha is not None:
            artist.set_alpha(alpha)

        # for some reason auto-scale does not work
        tfields.plotting.autoscale_3d(po.axis, array=vertices)

        # legend lables do not work at all as an argument
        if label:
            artist.set_label(label)

        # when plotting the legend edgecolors/facecolors2d are needed
        artist._edgecolors2d = None
        artist._facecolors2d = None

        labelList = ['x (m)', 'y (m)', 'z (m)']
        tfields.plotting.set_labels(po.axis, *po.getSortedLabels(labelList))

    else:
        raise NotImplementedError("Dimension != 2|3")

    return artist


def plot_tensor_field(points, vectors, **kwargs):
    """
    Args:
        points (array_like): base vectors
        vectors (array_like): direction vectors
    """
    po = tfields.plotting.PlotOptions(kwargs)
    if points is None:
        points = np.full(vectors.shape, 0.)
    artists = []
    xAxis, yAxis, zAxis = po.getXYZAxis()
    for point, vector in zip(points, vectors):
        if po.dim == 3:
            artists.append(po.axis.quiver(point[xAxis], point[yAxis], point[zAxis],
                                          vector[xAxis], vector[yAxis], vector[zAxis],
                                          **po.plotKwargs))
        elif po.dim == 2:
            artists.append(po.axis.quiver(point[xAxis], point[yAxis],
                                          vector[xAxis], vector[yAxis],
                                          **po.plotKwargs))
        else:
            raise NotImplementedError("Dimension != 2|3")
    return artists


def plot_plane(point, normal, **kwargs):

    def plot_vector(fig, orig, v, color='blue'):
        axis = fig.gca(projection='3d')
        orig = np.array(orig)
        v = np.array(v)
        axis.quiver(orig[0], orig[1], orig[2], v[0], v[1], v[2], color=color)
        axis.set_xlim(0, 10)
        axis.set_ylim(0, 10)
        axis.set_zlim(0, 10)
        axis = fig.gca(projection='3d')
        return fig

    def rotation_matrix(d):
        sin_angle = np.linalg.norm(d)
        if sin_angle == 0:
            return np.identity(3)
        d /= sin_angle
        eye = np.eye(3)
        ddt = np.outer(d, d)
        skew = np.array([[0, d[2], -d[1]],
                         [-d[2], 0, d[0]],
                         [d[1], -d[0], 0]],
                        dtype=np.float64)

        M = ddt + np.sqrt(1 - sin_angle**2) * (eye - ddt) + sin_angle * skew
        return M

    def pathpatch_2d_to_3d(pathpatch, z, normal):
        if type(normal) is str:  # Translate strings to normal vectors
            index = "xyz".index(normal)
            normal = np.roll((1.0, 0, 0), index)

        normal /= np.linalg.norm(normal)  # Make sure the vector is normalised
        path = pathpatch.get_path()  # Get the path and the associated transform
        trans = pathpatch.get_patch_transform()

        path = trans.transform_path(path)  # Apply the transform

        pathpatch.__class__ = plt3D.art3d.PathPatch3D  # Change the class
        pathpatch._code3d = path.codes  # Copy the codes
        pathpatch._facecolor3d = pathpatch.get_facecolor  # Get the face color

        verts = path.vertices  # Get the vertices in 2D

        d = np.cross(normal, (0, 0, 1))  # Obtain the rotation vector
        M = rotation_matrix(d)  # Get the rotation matrix

        pathpatch._segment3d = np.array([np.dot(M, (x, y, 0)) + (0, 0, z) for x, y in verts])

    def pathpatch_translate(pathpatch, delta):
        pathpatch._segment3d += delta

    kwargs['alpha'] = kwargs.pop('alpha', 0.5)
    po = tfields.plotting.PlotOptions(kwargs)
    patch = Circle((0, 0), **po.plotKwargs)
    po.axis.add_patch(patch)
    pathpatch_2d_to_3d(patch, z=0, normal=normal)
    pathpatch_translate(patch, (point[0], point[1], point[2]))


def plot_sphere(point, radius, **kwargs):
    po = tfields.plotting.PlotOptions(kwargs)
    # Make data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = point[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = point[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = point[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot the surface
    return po.axis.plot_surface(x, y, z, **po.plotKwargs)


def plot_function(fun, **kwargs):
    """
    Args:
        axis (matplotlib.Axis) object

    Returns:
        Artist or list of Artists (imitating the axis.scatter/plot behaviour).
        Better Artist not list of Artists
    """
    import numpy as np
    labelList = ['x', 'f(x)']
    po = tfields.plotting.PlotOptions(kwargs)
    tfields.plotting.set_labels(po.axis, *labelList)
    xMin, xMax = po.pop('xMin', 0), po.pop('xMax', 1)
    n = po.pop('n', 100)
    vals = np.linspace(xMin, xMax, n)
    args = (vals, map(fun, vals))
    artist = po.axis.plot(*args,
                          **po.plotKwargs)
    return artist


"""
Color section
"""


def to_colors(scalars, cmap=None, vmin=None, vmax=None):
    """
    retrieve the colors for a list of scalars
    """
    if not hasattr(scalars, '__iter__'):
        scalars = [scalars]
    if vmin is None:
        vmin = min(scalars)
    if vmax is None:
        vmax = max(scalars)
    color_map = plt.get_cmap(cmap)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    return color_map(map(norm, scalars))


def to_scalars(colors, cmap, vmin, vmax):
    """
    Inverse 'to_colors'
    Reconstruct the numeric values (0 - 1) of given
    Args:
        colors (list or rgba tuple)
        cmap (matplotlib colormap)
        vmin (float)
        vmax (float)
    """
    # colors = np.array(colors)/255.
    r = np.linspace(vmin, vmax, 256)
    norm = mpl.colors.Normalize(vmin, vmax)
    mapvals = cmap(norm(r))[:, :4]  # there are 4 channels: r,g,b,a
    scalars = []
    for color in colors:
        distance = np.sum((mapvals - color) ** 2, axis=1)
        scalars.append(r[np.argmin(distance)])
    return scalars


def colormap(seq):
    """
    Args:
        seq (iterable): a sequence of floats and RGB-tuples. The floats should be increasing
            and in the interval (0,1).
    Returns:
        LinearSegmentedColormap
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mpl.colors.LinearSegmentedColormap('CustomMap', cdict)


def color_cycle(cmap=None, n=None):
    """
    Args:
        cmap (matplotlib colormap): e.g. plt.cm.coolwarm
        n (int): needed for cmap argument
    """
    if cmap:
        color_rgb = to_colors(np.linspace(0, 1, n), cmap=cmap, vmin=0, vmax=1)
        colors = map(lambda rgb: '#%02x%02x%02x' % (rgb[0] * 255,
                                                    rgb[1] * 255,
                                                    rgb[2] * 255),
                     tuple(color_rgb[:, 0:-1]))
    else:
        colors = list([color['color'] for color in mpl.rcParams['axes.prop_cycle']])
    return cycle(colors)


"""
Display section
"""


def axis_dim(axis):
    """
    Returns int: axis dimension
    """
    if hasattr(axis, 'get_zlim'):
        return 3
    else:
        return 2


def set_aspect_equal(axis):
    """Fix equal aspect bug for 3D plots."""

    if axis_dim(axis) == 2:
        axis.set_aspect('equal')
        return

    xlim = axis.get_xlim3d()
    ylim = axis.get_ylim3d()
    zlim = axis.get_zlim3d()

    from numpy import mean
    xmean = mean(xlim)
    ymean = mean(ylim)
    zmean = mean(zlim)

    plot_radius = max([abs(lim - mean_)
                       for lims, mean_ in ((xlim, xmean),
                                           (ylim, ymean),
                                           (zlim, zmean))
                       for lim in lims])

    axis.set_xlim3d([xmean - plot_radius, xmean + plot_radius])
    axis.set_ylim3d([ymean - plot_radius, ymean + plot_radius])
    axis.set_zlim3d([zmean - plot_radius, zmean + plot_radius])


def set_axis_off(axis):
    if axis_dim(axis) == 2:
        axis.set_axis_off()
    else:
        axis._axis3don = False


def autoscale_3d(axis, array=None, xLim=None, yLim=None, zLim=None):
    if array is not None:
        xMin, yMin, zMin = array.min(axis=0)
        xMax, yMax, zMax = array.max(axis=0)
        xLim = (xMin, xMax)
        yLim = (yMin, yMax)
        zLim = (zMin, zMax)
    xLimAxis = axis.get_xlim()
    yLimAxis = axis.get_ylim()
    zLimAxis = axis.get_zlim()

    if not False:
        # not empty axis
        xMin = min(xLimAxis[0], xLim[0])
        yMin = min(yLimAxis[0], yLim[0])
        zMin = min(zLimAxis[0], zLim[0])
        xMax = max(xLimAxis[1], xLim[1])
        yMax = max(yLimAxis[1], yLim[1])
        zMax = max(zLimAxis[1], zLim[1])
    axis.set_xlim([xMin, xMax])
    axis.set_ylim([yMin, yMax])
    axis.set_zlim([zMin, zMax])


def set_legend(axis, artists):
    """
    Convenience method to set a legend from multiple artists to an axis.
    """
    handles = []
    for artist in artists:
        if isinstance(artist, list):
            handles.append(artist[0])
        else:
            handles.append(artist)
    axis.legend(handles=handles)


def set_colorbar(axis, artist, label=None, divide=True, **kwargs):
    """
    Note:
        Bug found in matplotlib:
            when calling axis.clear(), the colorbar has to be removed by hand,
            since it will not be removed by clear.
        >> import tfields
        >> axis = tfields.plotting.gca()
        >> artist = ...
        >> cbar = tfields.plotting.set_colorbar(axis, artist)
        >> tfields.plotting.save(...)
        >> cbar.remove()  # THIS IS IMPORTANT. Otherwise you will have problems
        # at the next call of savefig.
        >> axis.clear()

    """
    # colorbar
    if divide:
        divider = make_axes_locatable(axis)
        axis = divider.append_axes("right", size="2%", pad=0.05)
    cbar = plt.colorbar(artist, cax=axis, **kwargs)

    # label
    if label is None:
        art_label = artist.get_label()
        if art_label:
            label = art_label
    if label is not None:
        labelpad = 30
        cbar.set_label(label, rotation=270, labelpad=labelpad)
    return cbar


def set_labels(axis, *labels):
    axis.set_xlabel(labels[0])
    axis.set_ylabel(labels[1])
    if axis_dim(axis) == 3:
        axis.set_zlabel(labels[2])


def set_formatter(sub_axis=None, formatter=dates.DateFormatter('%d-%m-%y')):
    if sub_axis is None:
        axis = gca()
        sub_axis = axis.xaxis
    sub_axis.set_major_formatter(formatter)


if __name__ == '__main__':
    m = tfields.Mesh3D.grid((0, 2, 2), (0, 1, 3), (0, 0, 1))
    m.maps[0].fields.append(tfields.Tensors(np.arange(m.faces.shape[0])))
    art1 = m.plot(dim=3, map_index=0, label='twenty')

    m = tfields.Mesh3D.grid((4, 7, 2), (3, 5, 3), (2, 2, 1))
    m.maps[0].fields.append(tfields.Tensors(np.arange(m.faces.shape[0])))
    art = m.plot(dim=3, map_index=0, edgecolor='k', vmin=-1, vmax=1, label="something")

    plot_sphere([7, 0, 1], 3)
