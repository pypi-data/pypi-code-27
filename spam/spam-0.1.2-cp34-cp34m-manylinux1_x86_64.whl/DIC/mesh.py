from __future__ import print_function
import numpy
import tifffile
import pickle as pickleRick


def makeMesh(imSize=(100, 100, 100), meshPickleFile=None, outputFolder=".", tetVol="", meshPadding=0, debugFiles=False):
    """
        Define a grid of correlation points.

        Parameters
        ----------


        Returns
        -------
    """
    #import pygmsh as pg
    #import spam.label.toolkit as ltk

    # print "\tmesh.makeMesh(): Generating Mesh"
    #geom = pg.Geometry()
    # geom.add_box( 0+meshPadding, imSize[0]+1-meshPadding,
    #0+meshPadding, imSize[1]+1-meshPadding,
    # 0+meshPadding, imSize[2]+1-meshPadding, tetSize )
    ##points, cells = pg.generate_mesh( geom, optimize=True, verbose=False )
    #pgReturns = pg.generate_mesh( geom, optimize=True, verbose=False )

    import meshpy.tet
    import spam.label.toolkit as ltk

    print("\tmesh.makeMesh(): Generating Mesh with TetGen")

    mesh_info = meshpy.tet.MeshInfo()
    mesh_info.set_points([(0+meshPadding,          0+meshPadding,          0+meshPadding),
                          (imSize[0]+1-meshPadding, 0 +
                           meshPadding,          0+meshPadding),
                          (imSize[0]+1-meshPadding, imSize[1] +
                           1-meshPadding, 0+meshPadding),
                          (0+meshPadding,
                           imSize[1]+1-meshPadding, 0+meshPadding),
                          (0+meshPadding,          0+meshPadding,
                           imSize[2]+1-meshPadding),
                          (imSize[0]+1-meshPadding, 0+meshPadding,
                           imSize[2]+1-meshPadding),
                          (imSize[0]+1-meshPadding, imSize[1]+1 -
                           meshPadding, imSize[2]+1-meshPadding),
                          (0+meshPadding,          imSize[1]+1-meshPadding, imSize[2]+1-meshPadding)])
    mesh_info.set_facets([
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 4, 5, 1],
        [1, 5, 6, 2],
        [2, 6, 7, 3],
        [3, 7, 4, 0],
    ])
    meshObj = meshpy.tet.build(mesh_info, verbose=True, options=meshpy.tet.Options(
        switches='pqa{}'.format(tetVol)))

    points = numpy.array(meshObj.points)
    cells = numpy.array(meshObj.elements)

    if debugFiles:
        # Write mesh to file
        print("\t\tmesh.makeMesh(): Writing VTK mesh to file:")
        meshObj.write_vtk('{}/cube.vtk'.format(outputFolder))

    # overwrite cells with cells['tetra'] to keep only tetrahedral elements in the connectivity matrix
    # print cells
    # exit()
    #cells = cells['tetra'].astype('u4')

    print("\t\tmesh.makeMesh(): Image Size:", imSize)
    print("\t\tmesh.makeMesh(): TetrahedronVolume:", tetVol)
    print("\t\tmesh.makeMesh(): Padding:", meshPadding)
    print("\t\tmesh.makeMesh(): Points:", points.shape)
    print("\t\tmesh.makeMesh(): Cells:", cells.shape)

    imTetLabel = numpy.zeros(imSize).astype('u4')

    # Loop over tetrahedra
    print("\t\tmesh.makeMesh(): Allocating 3D data (labelled image)")
    print("\t\tmesh.makeMesh(): Looping over tetrahedra for pixel labelling")
    imTetLabel = ltk.getLabelledTetrahedra(imSize, cells, points)

    if debugFiles:
        print("\t\tmesh.makeMesh(): Saving labelled images")
        #iman.save_as_vtk( imTetLabel, o_name="labelled" )
        tifffile.imsave("{}/labelled.tiff".format(outputFolder), imTetLabel)

    mesh = {"points": points, "cells": cells,
            "lab": imTetLabel, "padding": meshPadding}

    if meshPickleFile is not None:
        print("\t\tmesh.makeMesh(): Pickling everything",)
        pickleRick.dump(mesh, open(
            "{}/{}".format(outputFolder, meshPickleFile), "wb"))

    return mesh, meshObj


if __name__ == "__main__":
    mesh = makeMesh(imSize=(100, 100, 100), meshPickleFile="mesh.p",
                    outputFolder="./", tetSize=10, meshPadding=0, debugFiles=True)
