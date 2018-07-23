"""Running network theory experiments."""

import os
import json


def run_experiment(filepath, output_dir=None):
    """Runs the experiment defined by the given file.

    Parameters
    ----------
    filepath : str
        The full path to experiment json definition file.
    output_dir : str, optional
        The full path to the output directory, where results are written to.
        If not given, the directory containing the experiment file is used.
    """
    if output_dir is not None:
        output_dir = os.path.dirname(filepath)
    with open(filepath, 'r') as efile:
        edict = json.load(efile)
