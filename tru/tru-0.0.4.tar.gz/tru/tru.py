import os
import glob
import json
import yaml
import pickle
import collections
import pandas as pd
import importlib

BASE_DIRECTORY = None


def load(input_string, header='infer', index_col=None, encoding=None):
    if input_string[0] == "/":
        file = input_string
    else:
        assert BASE_DIRECTORY is not None
        file = os.path.join(BASE_DIRECTORY, input_string)

    if input_string[-1] == "/":
        files = glob.glob(input_string + "*")
        loaded_files = [load(x) for x in files]
        return pd.concat(loaded_files)

    file_type = file.split(".")[-1]
    if file_type == "json":
        with open(file, 'r') as f:
            return json.load(f)
    if file_type == "yaml":
        with open(file, 'r') as f:
            return yaml.load(f)
    if file_type == "pkl":
        with open(file, 'rb') as f:
            return pickle.load(f)
    if file_type == "csv":
        return pd.read_csv(
            file,
            header=header,
            index_col=index_col,
            encoding=encoding
        )


def dump(input_object, input_string, encoding=None):

    if type(input_object) == collections.defaultdict:
        object_to_dump = dict(input_object)
    else:
        object_to_dump = input_object

    if input_string[0] == "/":
        file = input_string
    else:
        assert BASE_DIRECTORY is not None
        file = os.path.join(BASE_DIRECTORY, input_string)

    file_type = file.split(".")[-1]
    if file_type == "json":
        with open(file, 'w') as f:
            json.dump(object_to_dump, f)
    if file_type == "yaml":
        with open(file, 'w') as f:
            yaml.dump(object_to_dump, f)
    if file_type == "pkl":
        with open(file, 'wb') as f:
            pickle.dump(object_to_dump, f)
    if file_type == "csv":
        object_to_dump.to_csv(file, index=False, encoding=encoding)


def reload(package):
    importlib.reload(package)
