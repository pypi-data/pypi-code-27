"""
This file contains the classes that can be used to import groundwater level
data from dinoloket.nl.

TODO: Get rid of filternummer en opmerking in self.series

"""

from io import StringIO
from os import path
from pathlib import Path
from zipfile import is_zipfile, ZipFile

import numpy as np
from pandas import Series, read_csv

from ..timeseries import TimeSeries

__all__ = ["read_dino", "read_dino2"]


def read_dino(fname, variable='Stand_cm_tov_NAP', factor=0.01):
    """This method can be used to import files from Dinoloket that contain
     groundwater level measurements (https://www.dinoloket.nl/)

    Parameters
    ----------
    fname: str
        Filename and path to a Dino file.

    Returns
    -------
    ts: pastas.TimeSeries
        returns a Pastas TimeSeries object or a list of objects.

    """

    # Read the file
    dino = DinoGrondwaterstand(fname)
    ts = []

    if variable not in dino.data.keys():
        raise (
            ValueError("variable %s is not in this dataset. Please use one of "
                       "the following keys: %s" % (
                           variable, dino.data.keys())))
    series = dino.data[variable] * factor  # To make it meters)
    if len(dino.meta) > 0:
        metadata = dino.meta[-1]
    else:
        metadata = None

    metadata['x'] = dino.x
    metadata['y'] = dino.y
    metadata['z'] = np.mean((dino.bovenkant_filter, dino.onderkant_filter))
    metadata['projection'] = 'epsg:28992'

    ts.append(TimeSeries(series,
                         name=dino.locatie + '_' + str(dino.filternummer),
                         metadata=metadata, settings='oseries'))
    if len(ts) == 1:
        ts = ts[0]
    return ts


class DinoGrondwaterstand:
    def __init__(self, fname):
        with open(fname, 'r') as f:
            # lees de header
            line = f.readline()
            header = dict()
            while line not in ['\n', '', '\r\n']:
                propval = line.split(',')
                prop = propval[0]
                prop = prop.replace(':', '')
                prop = prop.strip()
                val = propval[1]
                if propval[2] != '':
                    val = val + ' ' + propval[2].replace(':', '') + ' ' + \
                          propval[3]
                header[prop] = val
                line = f.readline()

            # lees gat
            while (line == '\n') or (line == '\r\n'):
                line = f.readline()

            # lees referentieniveaus
            ref = dict()
            while line not in ['\n', '', '\r\n']:
                propval = line.split(',')
                prop = propval[0]
                prop = prop.replace(':', '')
                prop = prop.strip()
                if len(propval) > 1:
                    val = propval[1]
                    ref[prop] = val
                line = f.readline()

            # lees gat
            while (line == '\n') or (line == '\r\n'):
                line = f.readline()

            # lees meta-informatie
            metaList = list()
            line = line.strip()
            properties = line.split(',')
            line = f.readline()
            while line not in ['\n', '', '\r\n']:
                meta = dict()
                line = line.strip()
                values = line.split(',')
                for i in range(0, len(values)):
                    meta[properties[i]] = values[i]
                metaList.append(meta)
                line = f.readline()

            # lees gat
            while (line == '\n') or (line == '\r\n'):
                line = f.readline()

            line = line.strip()
            titel = line.split(',')
            while '' in titel:
                titel.remove('')

            # lees reeksen
            if line != '':
                # Validate if titles are valid names
                validator = np.lib._iotools.NameValidator()
                titel = validator(titel)
                dtype = [np.float64] * (len(titel))
                dtype[0] = "S11"
                dtype[1] = np.int
                dtype[2] = "S10"
                dtype[titel.index('Bijzonderheid')] = object
                dtype[titel.index('Opmerking')] = object
                dtype = list(zip(titel, dtype))

                usecols = range(0, len(titel))
                # # usecols.remove(2)
                measurements = read_csv(f, header=None, names=titel,
                                        parse_dates=['Peildatum'],
                                        index_col='Peildatum',
                                        dayfirst=True,
                                        usecols=usecols)
                ts = measurements['Stand_cm_tov_NAP']

            else:
                measurements = None
                ts = Series()

            # %% kies welke invoer opgeslagen wordt
            self.meta = metaList
            if self.meta:
                self.locatie = self.meta[-1]['Locatie']
                self.filternummer = int(float(self.meta[-1]['Filternummer']))
                self.x = float(self.meta[-1]['X-coordinaat'])
                self.y = float(self.meta[-1]['Y-coordinaat'])
                meetpunt = self.meta[-1]['Meetpunt (cm t.o.v. NAP)']
                if meetpunt == '':
                    self.meetpunt = np.nan
                else:
                    self.meetpunt = float(meetpunt) / 100
                maaiveld = self.meta[-1]['Maaiveld (cm t.o.v. NAP)']
                if maaiveld == '':
                    self.maaiveld = np.nan
                else:
                    self.maaiveld = float(maaiveld) / 100
                bovenkant_filter = self.meta[-1][
                    'Bovenkant filter (cm t.o.v. NAP)']
                if bovenkant_filter == '':
                    self.bovenkant_filter = np.nan
                else:
                    self.bovenkant_filter = float(bovenkant_filter) / 100
                self.onderkant_filter = self.meta[-1][
                    'Onderkant filter (cm t.o.v. NAP)']
                if self.onderkant_filter == '':
                    self.onderkant_filter = np.nan
                else:
                    self.onderkant_filter = float(self.onderkant_filter) / 100
            else:
                # de metadata is leeg
                self.locatie = ''
                self.filternummer = np.nan
                self.x = np.nan
                self.y = np.nan
                self.meetpunt = np.nan
                self.maaiveld = np.nan
                self.bovenkant_filter = np.nan
                self.onderkant_filter = np.nan
            self.data = measurements
            self.stand = ts

        f.close()


def read_dino2(fname, variable='Stand_cm_tov_NAP', factor=0.01, **kwargs):
    """Method to import groundwater time series from Dinoloket.

    Parameters
    ----------
    fname: str
        path and file name. File can be a zip-file, unzipped-file, folder
        with groundwater observations or a csv-file for only one location.
    variable: str
        variable name to be imported.

    Returns
    -------
    data: dict or pastas.TimeSeries
        dictionary with the name of the

    Notes
    -----
    More information on DinoLoket can be found here:
    https://www.dinoloket.nl/

    """
    dir = "Grondwaterstanden_Put"
    # 1. Check if file is a zip-file
    if is_zipfile(fname):
        data = dict()
        with ZipFile(fname) as file:
            files = file.namelist()
            files = [name for name in files if Path(name).match(
                "Grondwaterstanden_Put\\*_1.csv")]
            for name in files:
                temp_file = StringIO(file.open(name, "r").read().decode())
                series = _read_file(temp_file, variable)
                if series is not None:
                    name = path.splitext(path.basename(name))[0].strip(
                        "_1")
                    data[name] = series
    # 2. Check if file is already unzipped
    elif list(Path(path.join(fname, dir)).glob("*_1.csv")):
        data = dict()
        files = Path(path.join(fname, dir)).glob("*_1.csv")
        for name in files:
            with open(name) as file:
                series = _read_file(file, variable)
                if series is not None:
                    name = path.splitext(path.basename(name))[0].strip(
                        "_1")
                    data[name] = series
    # 3. Check if file only contains the Grondwaterstanden
    elif list(Path(fname).glob("*_1.csv")):
        data = dict()
        files = Path(fname).glob("*_1.csv")
        for name in files:
            with open(name) as file:
                series = _read_file(file, variable)
                if series is not None:
                    name = path.splitext(path.basename(name))[0].strip(
                        "_1")
                    data[name] = series
    # 4. if dino-file is provided
    elif path.splitext(fname)[1] == ".csv":
        with open(fname) as file:
            data = _read_file(file, variable)
            if data is not None:
                name = path.splitext(path.basename(fname))[0].strip(
                    "_1")
                data.name = name
    # 5. Return Error
    else:
        data = NotImplementedError("Provided file-type is not supported.")

    return data


def _read_file(file, variable='Stand_cm_tov_NAP'):
    """Internal method to import groundwater levels from a single file.

    Parameters
    ----------
    file: io.StringIO
        StringIO object with seek and readlines methods.
    variable: list of str
        String or list of strings with the variables to retrieve from the
        file. Default is 'Stand_cm_tov_NAP'.


    Returns
    -------
    series: pandas.series
        Pandas Series or DataFrame with the data. The metadata from the file
        is stored in series.metadata. When copying this object, beware that
        this metadata might be lost.

    """
    lines = file.readlines()
    start = []
    for i, line in enumerate(lines):
        if "locatie" in line.lower():
            start.append(i)
            if len(start) == 2:
                line = line.strip("\n")
                columns = line.split(",")
                break

    if not start:
        return None

    # Read the header
    file.seek(0)
    metadata = read_csv(file, nrows=start[1] - start[0], skiprows=start[0],
                        skipinitialspace=True, quoting=3, doublequote=False,
                        infer_datetime_format=True, error_bad_lines=False,
                        skip_blank_lines=True, warn_bad_lines=False)

    # Validate if titles are valid names
    validator = np.lib._iotools.NameValidator()
    columns = validator(columns)

    # We have to import all because the file-format is wrong and has to many
    #  delimiters in the data by default :(
    file.seek(0)
    usecols = range(0, len(columns))
    series = read_csv(file, skiprows=start[1] + 1, header=None,
                      names=columns, parse_dates=['Peildatum'], quoting=3,
                      doublequote=False, skipinitialspace=True,
                      index_col='Peildatum', usecols=usecols, dayfirst=True,
                      infer_datetime_format=True, error_bad_lines=False,
                      skip_blank_lines=True, warn_bad_lines=False)

    if variable:
        series = series.loc[:, variable]

    # If no data is available return None
    if not series.first_valid_index():
        return None

    series.metadata = metadata

    return series
