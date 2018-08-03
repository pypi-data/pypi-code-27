# ------------------------------------------------------------------------------
# Copyright IBM Corp. 2018
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
#

import logging
import pandas as pd
from io import BytesIO
from io import StringIO
from .connect import Connection
from .object_module import object_iterator

class Converter:
    """Class to Convert CSV to Parquet"""

    def __init__(self, connection, cos_bucket):
        """ initialize the class with the connection to COS and COS bucket """

        self.connection = connection
        self.cos_bucket = cos_bucket
        self.object_iterator = object_iterator(connection, cos_bucket)

    def _get_object(self, obj):
        """ get the body of an object """

        cos = self.connection
        cos_object = cos.get_object(Bucket=self.cos_bucket, Key=obj)
        body = cos_object['Body'].read().decode('utf-8')

        return body

    def _read_csv_to_df(self, obj):
        """ read the object contents and put them into a panda's dataframe """

        get_object = self._get_object(obj)
        buff = StringIO(get_object)

        try:
            df = pd.read_csv(buff)

            # replaces spaces in column names like `sample column` with `sample_column`
            cols = df.columns.str.strip().str.replace(' ', '_')
            df.columns = cols   

            return df

        except Exception:
            logging.error("Can't create panda's dataframe from object")

    def _convert_to_parquet(self, obj, new_obj_name):
        """ convert the pandas dataframe to Parquet """

        df = self._read_csv_to_df(obj)
        parquet_obj = BytesIO()
        df.to_parquet(parquet_obj, compression="gzip", engine="pyarrow")
        parquet_obj.seek(0)
            
        return self._save_object(new_obj_name, parquet_obj)
    
    def _save_object(self, new_obj_name, parquet_data):
        """ save the body of the object and rename with the .parquet file extension """

        cos = self.connection
        new_obj_name_parquet = "{}.parquet".format(new_obj_name)
        return cos.put_object(Body=parquet_data.getvalue(), Bucket=self.cos_bucket, Key=new_obj_name_parquet)

    def list_bucket_objects(self):
        """ list all the objects in a bucket """
        
        return self.object_iterator.list_all_objects()

    def list_csv_objects(self):
        """ list all the objects that are CSV objects in a bucket """

        return self.object_iterator.list_csv_objects()

    def list_csv_objects_names(self):
        """ list only the names of CSV objects """
        
        return self.object_iterator.list_csv_object_names()

    def convert_selected_objects(self, objs, names):
        """ convert selected objects to Parquet """

        for csv_name, new_parquet_name in zip(objs, names):
            self._convert_to_parquet(csv_name, new_parquet_name)
            
def convert_objects(api_key, service_endpoint, cos_bucket):
        """ a helper to create a convert object """

        connection = Connection(api_key, service_endpoint)
        return Converter(connection, cos_bucket)
