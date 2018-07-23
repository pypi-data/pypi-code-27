"""Running netprop experiments."""

import os


def _experiment_files_by_dir(directory, recursive=False):
    """Returns file names of netprop experiments in a given directory.

    Parameters
    ----------
    directory : str
        The path to the directory to look for experiments in.
    recursive : bool, default False
        If set to True, experiment discoverty recurses into subdirectories.
    """
    filepaths = []
    for root, subdirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                filepaths.append(file_path)
        if not recursive:
            break
    return filepaths


def run_experiments_by_dir(directory, recursive=False, silent=False):
    """Runs all discovered netprop experiments in the given directory.

    Parameters
    ----------
    directory : str
        The path to the directory to look for experiments in.
    recursive : bool, default False
        If set to True, experiment discoverty recurses into subdirectories.
    silent : bool, default False
        If set to True, no messages are printed to screen.
    """
    _print = print
    if silent:
        _print = lambda x: x  # noqa: E731
    _print("Starting to run experiments in directory {}".format(directory))
    _print("Discovering experiments{}...".format(
        " recursively" if recursive else ""))
    experiment_files = _experiment_files_by_dir(directory, recursive)
    _print("{} experiment files found:\n{}".format(
        len(experiment_files), experiment_files))
