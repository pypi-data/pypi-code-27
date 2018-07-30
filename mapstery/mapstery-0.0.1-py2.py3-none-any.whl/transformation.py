import scipy




def dem_to_slope(gdal_band):
    """
        Transform a raster band of a GDAL dataset containing DEM information
        into a slope map as a numpy array.

        :param gdal_band: GDAL dataset band (output of ds.GetRasterBand(i)
        :return: numpy array image of the slope map
    """

    arr = gdal_band.ReadAsArray()
    k1 = np.zeros((3,3))
    scipy.signal.convolve2d(arr,)
