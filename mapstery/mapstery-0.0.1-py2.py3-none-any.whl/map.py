import gdal
import json
import numpy as np
#import gdalconst

class Map():

    def __init__(self, rows=500, cols=500, file_path=""):
        self._dataset = None
        self._default_datatype = gdal.GDT_UInt32
        self._default_driver = "MEM"
        self._default_rows = rows
        self._default_cols = cols

    @property
    def datatype(self):
        return self._default_datatype

    @datatype.setter
    def datatype(self, new_default_datatype):
        self._default_datatype = new_default_datatype
        return self._default_datatype

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, data_path, json_input=False):
        """ Set the internal dataset to an existing one
            or create one by reading a file from data_path
            if that is a string. This file could be a JSON
            file with a dictionnary containing the different layers

            :param data_path: GDAL dataset object or filename
            :param json_input: True of the data_path is a path to a json file
            and not an image or product
        """

        # --- Setting a dataset directly
        if isinstance(data_path, gdal.Dataset):
            self._dataset = data_path
            return self._dataset

        if not isinstance(data_path, str):
            print("Dataset input type is not managed yet: {}".format(type(data_path)))
            return self._dataset

        # --- Reading a file path of an image
        if json_input == False:
            try:
                self._dataset = gdal.Open(data_path)
            except Exception as eee:
                # at this point _dataset is set to None
                print(eee)
            return self._dataset

        # --- Reading from a JSON file
        # 
        # {  "BAND_NAME1": "filepath1.png",
        #    "BAND_NAME2": "filepath2.jpg"
        # }
        #
        else:
            json_file = open(args[1])
            input_bands = json.load(json_file)

            for keys in input_bands:
                if not isinstance(input_bands[keys], str):
                    continue

                tmp_ds = gdal.Open(input_bands[key])

                if tmp_ds.GetRasterCount() == 1:
                    self.add_band(tmp_ds.GetRasterBand(1), key)
                else:
                    bands_indexes = [i for i in range(tmp_ds.GetRasterCount())]
                    for k in bands_indexes:
                        self.add_band(tmp_ds.GetRasterBand(k), key)

    def add_band(self, data_array, band_name, new_band=True):
        """ Add one band (channel or layer) to the dataset
        """
        # --- Create a new dataset if necessary
        if self._dataset is None:
            gdal_driver = gdal.GetDriverByName(self._default_driver)
            self._dataset = gdal_driver.Create("/tmp/mapstery.mem",
                            self._default_rows, self._default_cols,
                            0, self._default_datatype)

        # --- Adding or getting the new band with its meta data
        current_band = None
        if new_band == True:
            print(" -----NNNNN--- Number of Bands : "+str(self._dataset.RasterCount))
            B = self._dataset.AddBand(self._default_datatype)
            print(" ------------- Number of Bands : "+str(self._dataset.RasterCount))
            current_band = self._dataset.GetRasterBand(self._dataset.RasterCount)
            current_band.SetDescription(band_name)
        else:
            current_band = self._dataset.GetLayerByName(band_name)

        if current_band is None:
            return False

        # --- Writing the band
        if isinstance(data_array, gdal.Band):
            print("Dunno how to add a band directly, so I'll use an array")
            data_array = data_array.ReadAsArray()

        if isinstance(data_array, np.ndarray):
            current_band.WriteArray(data_array)

        return True

    def save(self, output_file, driver="GTiff"):
        dst_ds = gdal.GetDriverByName(driver).CreateCopy(output_file, self._dataset, 0)
        dst_ds.FlushCache()
        del dst_ds
