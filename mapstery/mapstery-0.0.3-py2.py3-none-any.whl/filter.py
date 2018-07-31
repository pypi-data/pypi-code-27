from scipy import signal
from scipy.ndimage.filters import gaussian_filter
import numpy as np


def isogradient(gdal_band, blur_radius=7):
    """
        Transform a raster band of a GDAL dataset containing DEM information
        into a slope map as a numpy array.

        :param gdal_band: GDAL dataset band (output of ds.GetRasterBand(i)
        :param blur_radius: blurring radius in pixels, to blur out compression effects and eventual artifacts.
                            if the radius == 0 then no blur is applied
        :return: numpy array image of the slope map
    """

    k1 = np.array([ [-1, -1, -1], [0, 0, 0], [1, 1, 1] ])
    k2 = np.array([ [-1, 0, 1],
                    [-1, 0, 1],
                    [-1, 0, 1] ])
    k3 = np.array([ [-1, -1, 0],
                    [-1,  0, 1],
                    [ 0,  1, 1] ])
    k4 = np.array([ [0, -1, -1],
                    [1,  0, -1],
                    [1,  1,  0] ])

    arr = gdal_band.ReadAsArray()
    conv = np.abs(signal.convolve2d(arr, k1, mode="same", boundary="symm"))
    for kernel in [k2, k3, k4]:
        conv += np.abs(signal.convolve2d(arr, kernel, mode="same", boundary="symm"))

    conv = conv/4.0

    # --- Scaling the histogram [0 - 1.0]
    arr_min = np.min(conv)
    conv = (conv-arr_min) * 1.0 / (np.max(conv)-arr_min)

    # --- Blurring artifacts
    if blur_radius > 0:
        conv = gaussian_filter(conv, sigma=blur_radius)
        arr_min = np.min(conv)
        conv = (conv-arr_min) * 1.0 / (np.max(conv)-arr_min)

    return conv
