import csv
import glob
import numpy as np
import os
import re

OLD_RESULTS_DIR = os.path.abspath('./flics/tests/results')


def get_result_file_params(path: str) -> tuple:
    """
    Returns the distance and direction of a given result file according to the
    naming convention defined in the original code.
    
    :param path: Result file path.
    :type path: str
    :return: (distance, direction)
    :rtype: tuple
    """
    distance = int(re.sub('[^0-9]', '', path[-16:-13]))
    direction = path[-13:-4]
    return distance, direction


def get_result_file_length(path: str) -> int:
    """
    Check the number of values (lines) serialized in a given result file.
    
    :param path: Result file path.
    :type path: str
    :return: Number of values in the result file.
    :rtype: int
    """
    return sum(1 for line in open(path, newline=''))


def read_result_file(path: str) -> np.ndarray:
    """
    Returns the values serialized in a given result file.
    
    :param path: Result file path.
    :type path: str
    :return: Result file values.
    :rtype: np.ndarray
    """
    result = np.zeros(get_result_file_length(path))
    with open(path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            index, value = int(row[0]), float(row[1])
            result[index] = value
        return result


def parse_old_results(path: str = OLD_RESULTS_DIR) -> dict:
    """
    Returns a dictionary of the old analysis results as returned by the
    original code.
    
    :param path: Analysis results directory, defaults to OLD_RESULTS_DIR
    :param path: str, optional
    :return: Analyis results by distance and direction.
    :rtype: dict
    """
    paths = glob.glob(os.path.join(path, '*.txt'))
    old_results = dict()
    for path in paths:
        distance, direction = get_result_file_params(path)
        if distance not in old_results:
            old_results[distance] = dict()
        old_results[distance][direction] = read_result_file(path)
    return old_results
