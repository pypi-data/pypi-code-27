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
import datetime
import simplejson as json
import csv
import os
    
def datetime_helper(objs):
    """ helper function for datetime in JSON reponse """

    if isinstance(objs, datetime.datetime):
        return objs.isoformat()
    raise TypeError("Unknown Type")

def json_formatter(json_file):
    """ helper function to format JSON results """

    return json.dumps(json_file, default=datetime_helper, indent=4 * ' ')

def find_csv_objects(objs):
    """ helper function to find only CSV files """

    return [obj for obj in objs if '.csv' in obj.get('Key')]
    
def loop_objects_names(objs):
    """ helper function to loop through list of objects """

    return [obj['Key'] for obj in objs]

def object_convert_check():
    """ TODO """
    pass

def display_conversion():
    """ TODO """
    pass

# def _split_object_prefix_name(obj):
#     """ helper function that returns a tuple with the bucket prefix and object name """
    
#     return os.path.split(obj)

# def remove_objects_extensions(obj):
#     """ helper function to remove .csv from object name """

#     obj_name =  _split_object_prefix_name(obj)[1]
#     return os.path.splitext(obj_name)[0]

# def get_bucket_prefix(obj):
#     """ helper function to separate bucket prefix from object """

#     obj_prefix = _split_object_prefix_name(obj)[0]
#     return '/' if '' == obj_prefix else "{}/".format(obj_prefix)
