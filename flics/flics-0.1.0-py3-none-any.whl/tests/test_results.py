import math
import os
import pytest

from flics import flics
from .old_results_parser import parse_old_results

TEST_DATA_PATH = os.path.abspath('./flics/tests/test_data.tif')


@pytest.fixture(scope="module")
def analysis() -> flics.Analysis:
    """
    Runs the analysis on the test data so it can be accessed by tests.
    
    :return: Analysis class instance
    :rtype: flics.Analysis
    """
    return flics.Analysis(TEST_DATA_PATH)


@pytest.fixture(scope="module")
def old_results() -> dict:
    """
    Stores the parsed results as given by the original analysis code.
    
    :return: A dictionary of mean column-pair cross-correlation values by
    distance and direction.
    :rtype: dict
    """

    return parse_old_results()


def test_image_dimensions(analysis: flics.Analysis):
    """
    Tests the image data is extracted successfully by the Analysis instance.
    
    :param analysis: FLICS Analysis instance to be tested.
    :type analysis: flics.Analysis
    """
    assert analysis.image_data.shape == (1024, 1024), 'Wrong image dimensions'
    # TODO: Replace test image with one that has different dimension sizes


def test_results_length(analysis: flics.Analysis):
    """
    Tests the analysis ran over all the desired distances.
    
    :param analysis: FLICS Analysis instance to be tested.
    :type analysis: flics.Analysis
    """
    assert len(analysis.results) is len(
        analysis.distances), 'Analysis returned results with wrong length'


def test_results(analysis: flics.Analysis, old_results: dict):
    """
    Checks the FLICS Analysis instance results are same as origin.
    
    :param analysis: FLICS Analysis instance to be tested.
    :type analysis: flics.Analysis
    :param old_results: Parsed old results from original code.
    :type old_results: dict
    """

    y = analysis.image.height
    directions = 'rightleft', 'leftright'
    for direction in directions:
        for distance in old_results:
            for index, value in enumerate(old_results[distance][direction]):
                if direction == 'leftright' and index is not 0:
                    new_value = analysis.results[distance][y - index]
                else:
                    new_value = analysis.results[distance][index]
                assert math.isclose(
                    new_value, value
                ), f'Found unequal values!\nDirection\t=\t{direction}\n' \
                    'Distance\t=\t{distance}\nIndex\t\t=\t{index}\n' \
                    'Old\t\t=\t{value}\nNew\t\t=\t{new_value}'
