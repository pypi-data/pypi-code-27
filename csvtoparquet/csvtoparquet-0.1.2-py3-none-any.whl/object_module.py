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
from .helpers import json_formatter
from .helpers import loop_objects_names
from .helpers import find_csv_objects
from .connect import Connection

class ObjectIterator:
    
    def __init__(self, connection, cos_bucket):
        self.connection = connection
        self.cos_bucket = cos_bucket

    def _paginator_iterator(self):
        """ use the paginate function to iterate through all the objects in a bucket """

        cos = self.connection
        paginator = cos.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=self.cos_bucket)
                
        return page_iterator
    
    def _get_objects(self):
        """ get all the objects from the paginator and return as a list of objects """
        
        page_iterator = self._paginator_iterator()
        bucket_list = []
        for page in page_iterator:
            if "Contents" in page:
                if any(bucket_list) == False:
                    bucket_list = page["Contents"]
                else:
                    for key in page['Contents']:
                        bucket_list.append(key)
            else:
                logging.error("No objects are stored in the bucket!")

        return bucket_list
    
    def _get_csv_objects(self):
        """ get only the objects that are CSV object """
        objs = self._get_objects()

        return find_csv_objects(objs)

    def list_all_objects(self):
        """ pretty print all of the objects - even non-CSV types """
        try:
            objs = self._get_objects()

            return json_formatter(objs)

        except Exception as e:
            logging.error(e)

    def list_csv_objects(self):
        """ pretty print all of the CSV objects """
        try:
            csv_files = self._get_csv_objects()

            return json_formatter(csv_files)

        except Exception as e:
            logging.error(e)
    
    def list_csv_object_names(self):
        """ list only the names of the objects, not the other metadata """
        try:
            csv_files = self._get_csv_objects()

            return loop_objects_names(csv_files)
                
        except Exception as e:
            logging.error(e)

def object_iterator(connection, cos_bucket):
        """A helper to create a Bucket object."""

        return ObjectIterator(connection, cos_bucket)
