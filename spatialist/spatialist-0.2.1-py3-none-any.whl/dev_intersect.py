from osgeo import ogr
from spatialist import Vector

shp1 = '/home/john/Desktop/test/subset.shp'

shp2 = '/home/john/Desktop/test/subset2.shp'

shp3 = '/home/john/Desktop/test/intersection.shp'

# with Vector(shp1) as vec1:
#     with Vector(shp2) as vec2:
#         union1 = ogr.Geometry(ogr.wkbMultiPolygon)
#         # union all the geometrical features of layer 1
#         for feat in vec1.layer:
#             union1.AddGeometry(feat.GetGeometryRef())
#         union1.Simplify(0)
#         # same for layer2
#         union2 = ogr.Geometry(ogr.wkbMultiPolygon)
#         for feat in vec2.layer:
#             union2.AddGeometry(feat.GetGeometryRef())
#         union2.Simplify(0)
#         # intersection
#         intersect = union1.Intersection(union2)
#         union1 = None
#         union2 = None
#         if intersect.GetArea() > 0:
#             with Vector(driver='Memory') as intersection:
#                 intersection.addlayer('intersect', vec1.srs, ogr.wkbPolygon)
#                 intersection.addfield('id', type=ogr.OFTInteger)
#                 intersection.addfeature(intersect, {'id': 1})
#                 intersection.write(shp3)


def intersect(obj1, obj2):
    """
    intersect two Vector objects
    Parameters
    ----------
    obj1: Vector
        the first vector geometry
    obj2: Vector
        the second vector geometry

    Returns
    -------
    Vector
        the intersect of obj1 and obj2
    """
    if not isinstance(obj1, Vector) or not isinstance(obj2, Vector):
        raise RuntimeError('both objects must be of type Vector')

    obj1.reproject(obj2.srs)

    #######################################################
    # create basic overlap
    union1 = ogr.Geometry(ogr.wkbMultiPolygon)
    # union all the geometrical features of layer 1
    for feat in obj1.layer:
        union1.AddGeometry(feat.GetGeometryRef())
    obj1.layer.ResetReading()
    union1.Simplify(0)
    # same for layer2
    union2 = ogr.Geometry(ogr.wkbMultiPolygon)
    for feat in obj2.layer:
        union2.AddGeometry(feat.GetGeometryRef())
    obj2.layer.ResetReading()
    union2.Simplify(0)
    # intersection
    intersect_base = union1.Intersection(union2)
    union1 = None
    union2 = None
    #######################################################
    # compute detailed per-geometry overlaps
    if intersect_base.GetArea() > 0:
        intersection = Vector(driver='Memory')
        intersection.addlayer('intersect', obj1.srs, ogr.wkbPolygon)
        fieldmap = []
        for index, fielddef in enumerate([obj1.fieldDefs, obj2.fieldDefs]):
            for field in fielddef:
                name = field.GetName()
                i = 2
                while name in intersection.fieldnames:
                    name = '{}_{}'.format(field.GetName(), i)
                    i += 1
                fieldmap.append((index, field.GetName(), name))
                print(name, field.GetTypeName(), field.GetWidth())
                intersection.addfield(name, type=field.GetType(), width=field.GetWidth())

        for feature1 in obj1.layer:
            geom1 = feature1.GetGeometryRef()
            if geom1.Intersects(intersect_base):
                for feature2 in obj2.layer:
                    geom2 = feature2.GetGeometryRef()
                    # select only the intersections
                    if geom2.Intersects(intersect_base):
                        intersect = geom2.Intersection(geom1)
                        fields = {}
                        for item in fieldmap:
                            if item[0] == 0:
                                fields[item[2]] = feature1.GetField(item[1])
                            else:
                                fields[item[2]] = feature2.GetField(item[1])
                        intersection.addfeature(intersect, fields)
                        print(fields)
        print(intersection.nfeatures)
        print(intersection.nfields)
        for name in intersection.fieldnames:
            print(name, intersection.getUniqueAttributes(name))
        return intersection
