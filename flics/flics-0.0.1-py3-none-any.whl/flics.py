import numpy as np
import PIL.Image
import scipy
import scipy.fftpack


class Analysis:
    results = None

    def __init__(self,
                 image_path: str,
                 threshold: float = None,
                 max_distance: int = 320,
                 distance_step: int = 20,
                 autorun: bool = True):
        """
        Runs a flow image correlation spectroscopy (FLICS) analysis on a given
        .tif image file.
        
        :param image_path: .tif image file path.
        :type image_path: str
        :param threshold: Threshold to applied to the image, defaults to None.
        :param threshold: float, optional
        :param max_distance: Maximum column-pair distance to be calculated,
        defaults to 320.
        :param max_distance: int, optional
        :param distance_step: Step value for column-pair distances iteration,
        defaults to 20.
        :param distance_step: int, optional
        :param autorun: Run analysis on instantiation, defaults to True.
        :param autorun: bool, optional
        """

        # Set class parameters
        self.image = self.load_image(image_path)
        self.threshold = threshold
        self.max_distance = max_distance
        self.distance_step = distance_step

        # Create a range of the distances to be calculated
        self.distances = range(0, self.max_distance, self.distance_step)

        # Load image data and calculate column means and element-wise deviation
        self.image_data = self.get_image_data()
        self.column_means = self.image_data.mean(axis=0)
        self.deviation_from_column_mean = self.image_data - self.column_means

        if autorun:
            self.run()

    def load_image(self, path: str):
        """
        Returns the loaded image data.
        
        :param path: .tif image file path.
        :type path: str
        :raises FileNotFoundError: Failed to read image from file.
        :return: Loaded image data.
        :rtype: PIL.TiffImagePlugin.TiffImageFile
        """
        try:
            return PIL.Image.open(path)
        except (FileNotFoundError, OSError) as e:
            raise FileNotFoundError(f'Failed to load image file from {path}')

    def get_image_data(self) -> np.ndarray:
        """
        Returns image data as numpy array and applies the analysis threshold
        if defined.
        
        :return: Thresholded image data.
        :rtype: np.ndarray
        """
        data = np.array(self.image, dtype=float)
        if isinstance(self.threshold, float):
            data[data < self.threshold] = 0
        return data

    def calc_fft(self, i_column: int) -> np.ndarray:
        """
        Returns the discrete Fourier transform of a column's element-wise
        deviation from the (column) mean.
        
        :param i_column: Index of the chosen image column.
        :type i_column: int
        :return: A complex array with the tranform results.
        :rtype: np.ndarray
        """
        return scipy.fftpack.fft(self.deviation_from_column_mean[:, i_column])

    def calc_cross_corr(self, i_column: int, distance: int) -> np.ndarray:
        """
        Returns the cross-correlation function results for a given column and
        distance.
        
        :param i_column: Index of the chosen image column.
        :type i_column: int
        :param distance: Distance between the columns to cross-correlate.
        :type distance: int
        :return: Cross-correlation between the two columns.
        :rtype: np.ndarray
        """
        # TODO: This function should be refactored further with a better
        # understanding of the underlying algorithm
        column_transform = self.calc_fft(i_column)
        distant_column_transform = self.calc_fft(i_column + distance)
        distant_column_transform = np.ma.conjugate(distant_column_transform)

        inverse = scipy.fftpack.ifft(
            distant_column_transform * column_transform)
        divider = (self.column_means[i_column] *
                   self.column_means[i_column + distance] * self.image.height)
        crosscorr = np.real(inverse / divider)
        return crosscorr

    def calc_cross_corr_for_distance(self, distance: int) -> np.ndarray:
        """
        Returns all cross-correlations between two image columns with the given
        distance.

        :param distance: Distance between the columns to cross-correlate.
        :type distance: int
        :return: A stacked array of all column pairs cross-correlation results.
        :rtype: np.ndarray
        """
        n_column_pairs = self.image.width - distance
        return np.stack(
            [self.calc_cross_corr(x, distance) for x in range(n_column_pairs)])

    def run(self) -> None:
        """
        Returns the analysis results for all distances.
        
        :return: A dictionary of mean column-pair cross-correlations by
        distance.
        :rtype: dict
        """
        self.results = {}
        for distance in self.distances:
            cross_correlations = self.calc_cross_corr_for_distance(distance)
            self.results[distance] = cross_correlations.mean(axis=0)
