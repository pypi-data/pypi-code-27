""" This module provides some utilty functions to work with dumpi traces. """
from pathlib import Path
from os import listdir


def read_meta_file(file_name):
    """ Read key-value pairs from a dumpi meta file.

    Returns
    -------
    dict
        A dictionary of key-value pairs.
    """
    with open(file_name) as meta_file:
        return dict([line.strip().split("=") for line in meta_file])


def trace_files_from_dir(directory):
    """ Get all binary traces in a folder according to the meta file.

    Returns
    -------
    list
        A list of pathes to the binary traces.

    Raises
    ------
    ValueError
        If there is no meta file in the given directory.
    ValueError
        If there are missing binary traces.
    """
    # find meta info
    file_names = listdir(directory)
    meta_file = [f for f in file_names if "meta" in f]

    if not meta_file:
        raise ValueError("Could not find a meta file in given directory.")

    meta_info = read_meta_file(Path(directory) / meta_file[0])
    
    # filter out any non-binary files
    prefix = meta_info["fileprefix"]
    traces = [f for f in file_names if f.startswith(prefix) and f.endswith(".bin")]

    # abort if there are files missing
    num_procs = int(meta_info["numprocs"])
    if len(traces) != num_procs:
        raise ValueError("Some binary traces are missing.")

    # sort by proc id and prepend directory
    traces = sorted(traces, key=lambda t: int(t[len(prefix)+1:len(t)-len(".bin")]))
    return [Path(directory) / trace for trace in traces]
