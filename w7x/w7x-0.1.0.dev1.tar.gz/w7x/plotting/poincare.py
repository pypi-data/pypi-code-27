"""
specific methods for poincare plotting
"""
import tfields


def plot_poincare_surfaces(poincareSurfaces, **kwargs):
    """
    Args:
        poincareSurfaces (list of Points3D): each Points3D instance is one
            fieldLine followed around the torus
    """
    methodName = kwargs.pop('methodName', 'scatter')
    po = tfields.plotting.PlotOptions(kwargs)
    rMin = po.pop('rMin', 4.0)
    rMax = po.pop('rMax', 6.6)
    zMin = po.pop('zMin', -1.3)
    zMax = po.pop('zMax', +1.3)
    phiRad = po.pop('phiRad', None)

    po.setDefault('yAxis', 2)
    po.setDefault('labelList', ['r (m)', r'$\phi$ (rad)', 'z (m)'])
    if methodName is 'scatter':
        po.setDefault('marker', '.')
        po.setDefault('s', 1)
    po.setDefault('methodName', methodName)
    colorGiven = True
    if 'color' not in po.plotKwargs:
        colorGiven = False
        cmap, _, _ = po.getNormArgs()
        colorCycle = tfields.plotting.color_cycle(cmap, len(poincareSurfaces))
    artists = []
    for surfacePoints in poincareSurfaces:
        with surfacePoints.tmp_transform(tfields.bases.CYLINDER):
            phiSurface = surfacePoints[:, 1]
            if phiRad is None:
                phiRad = phiSurface[0]
            if bool((phiSurface != phiRad).any()):
                continue
            if not colorGiven:
                po.set('color', colorCycle.next())
            artists.append(surfacePoints.plot(axis=po.axis, **po.plotKwargs))
    tfields.plotting.set_aspect_equal(po.axis)
    po.axis.set_xlim(rMin, rMax)
    po.axis.set_ylim(zMin, zMax)
    return artists


def plot_poincare_geometries(geometries, **kwargs):
    po = tfields.plotting.PlotOptions(kwargs)
    po.setDefault('methodName', 'plot')
    po.setDefault('lw', 1)
    artists = []
    for p in range(len(geometries)):
        for g in range(len(geometries[p])):
            artists.extend(plot_poincare_surfaces(geometries[p][g], axis=po.axis,
                                                **po.plotKwargs)) 
    return artists
