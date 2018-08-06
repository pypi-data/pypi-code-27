"""
    General and more specific filters.

    Filters return unit scaled images. They have to be converted to whatever to
    your custom dynamics using move_dynamics()

"""
from scipy import signal
from scipy.ndimage.filters import gaussian_filter
import numpy as np


def move_dynamics(matrix, target_min_bound=0.0, target_max_bound=255.0, convert_uint=False):
    smin = np.min(matrix)
    smax = np.max(matrix)

    # TODO check target_max_bound > target_min_bound
    dyn_range = target_max_bound - target_min_bound

    matrix = ((matrix - smin) / (smax - smin)) * dyn_range + target_min_bound
    if convert_uint == True:
        return matrix.astype(np.uint8)

    return matrix


def isogradient(gdal_band, blur_radius=7):
    """
        Transform a raster band of a GDAL dataset containing DEM information
        into a slope map as a numpy array.

        :param gdal_band: GDAL dataset band (output of ds.GetRasterBand(i)
        :param blur_radius: Blurring radius in pixels, to blur out compression
                            effects and eventual artifacts.
                            if the radius == 0 then no blur is applied
        :return: numpy array image of the slope map scaled to one
    """

    k_1 = np.array([[-1, -1, -1],
                    [0, 0, 0],
                    [1, 1, 1]])
    k_2 = np.array([[-1, 0, 1],
                    [-1, 0, 1],
                    [-1, 0, 1]])
    k_3 = np.array([[-1, -1, 0],
                    [-1, 0, 1],
                    [0, 1, 1]])
    k_4 = np.array([[0, -1, -1],
                    [1, 0, -1],
                    [1, 1, 0]])

    arr = gdal_band.ReadAsArray()
    conv = np.abs(signal.convolve2d(arr, k_1, mode="same", boundary="symm"))
    for kernel in [k_2, k_3, k_4]:
        conv += np.abs(signal.convolve2d(arr, kernel, mode="same",
                                         boundary="symm"))

    conv = conv/4.0

    # --- Scaling the histogram [0 - 1.0]
    conv = move_dynamics(conv, target_min_bound=0.0, target_max_bound=1.0)

    # --- Blurring artifacts
    if blur_radius > 0:
        conv = gaussian_filter(conv, sigma=blur_radius)
        conv = move_dynamics(conv, target_min_bound=0.0, target_max_bound=1.0)

    return conv


def bands_average(mapy, bands, weights=[]):
    """ Mix bands with average

        EXAMPLE:
             shadow_mix = mapstery.filter.bands_average(M, [k+1 for k in range(168)])

        :param mapy: Mapstery Map
        :param bands: list of bands indexes to mix
        :param weights: weights to apply to their respective bands
        :param stop_at_index: index of bands to stop th
        :return: an array of the mix with real values of the weighted average
    """
    if len(bands) <= 1:
        print("No bands average has been done. Too few bands indicated for the mix.")
        return None

    if weights == [] or weights is None:
        weights = np.ones(len(bands))

    stop_at_index = len(weights)
    if stop_at_index <= 0:
        stop_at_index = len(weights)

    if stop_at_index > len(bands):
        stop_at_index = len(bands)

    print("Integrating band {}".format(bands[0]))
    band_mix = weights[0] * mapy.get_band(bands[0]).ReadAsArray()
    print("[+] Integrating band {} weighted {}".format(bands[0], weights[0]))

    w = 1
    for k in bands[1:stop_at_index]:
        print("[+] Integrating band {} weighted {}".format(k, weights[w]))
        band_mix += weights[w] * mapy.get_band(k).ReadAsArray()
        w += 1

    band_mix = band_mix / stop_at_index

    return band_mix


def integrate_shadows(mapy, bands, integration_horizon=5):
    """ Integrate shadows over the next bands as they represent the coming shadows

        :param bands: bands indexes to be associated, in chronological orders
        :param integration_horizon: how many steps ahead should be considered for shadow integration
        :param mapy: original dataset containing the sun-angle-computed shadows
    """
    integrated_list = []

    # Generate weights focussing on the first entries of the polynomial decrease
    weights = polynomial_decrease(np.int(integration_horizon*2), 2, 6)[:integration_horizon]

    # Cycle
    stop = len(bands) - len(weights)
    for start in [k for k in range(len(bands))]:
        bands_subset = []
        if start >= stop:
            # cycle the band subset to the beginning to have same size as weights
            bands_subset = bands[start:]
            bands_subset = np.append(bands_subset, bands[:(len(weights)-(len(bands)-start))])
        else:
            # entire slice is consecutive
            bands_subset = bands[start:start+len(weights)]

        new_shadow = bands_average(mapy, bands_subset, weights)
        integrated_list.append(new_shadow)

    return integrated_list


def polynomial_decrease(units, a_power=2.0, b_power=2.0):
    """ Return a polynomial decrease of the form (1-x^a)^b
    """
    if units < 3:
        units = 3
    x = np.linspace(0.0, 1.0, units)
    return np.power(1 - np.power(x, a_power), b_power)
