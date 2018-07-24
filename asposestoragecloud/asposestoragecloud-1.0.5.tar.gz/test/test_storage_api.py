# --------------------------------------------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="test_storage_api.py">
#   Copyright (c) 2015 Aspose.Storage for Cloud
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# --------------------------------------------------------------------------------------------------------------------
#

from __future__ import absolute_import

import os
import sys
import unittest
import warnings
from six import PY3

import asposestoragecloud
from asposestoragecloud.rest import ApiException
from asposestoragecloud.apis.storage_api import StorageApi
from asposestoragecloud.api_client import ApiClient

class TestStorageApi(unittest.TestCase):
    """ StorageApi unit test stubs """

    def setUp(self):
        ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)) + "/..")
        self.dataFolder = os.path.join(ABSPATH, "Data")
        
        self.apiClient = ApiClient(apiKey='xxxxx', appSid='xxxxx-xxxxx-xxxxx-xxxxx')

        self.api = asposestoragecloud.apis.storage_api.StorageApi(self.apiClient)

        if PY3:
            warnings.simplefilter("ignore", ResourceWarning)

    def tearDown(self):
        pass

    # File APIs Test Cases
    def test_put_create(self):
        """
        Test case for put_create

        Upload a specific file 
        """
        fileName = "testfile.txt"
        filePath = os.path.join(self.dataFolder, fileName)
        with open(filePath, 'rb') as fp:
            fileData = fp.read()
        response = self.api.put_create(fileName, fileData)
        self.assertTrue(response)

    def test_get_download(self):
        """
        Test case for get_download
        
        Download a specific file
        """
        fileName = 'testfile.txt'
        response = self.api.get_download(fileName)
        self.assertTrue(response)

    def test_post_move_file(self):
        """
        Test case for post_move_file
        
        Move a specific file
        """
        src = "testfile.txt"
        dest = os.path.join("Documents", "testfile.txt")
        response = self.api.post_move_file(src, dest)
        self.assertTrue(response)

    def test_delete_file(self):
        """
        Test case for delete_file
        
        Remove a specific file
        """
        fileName = 'testfile.txt'
        response = self.api.delete_file(fileName)
        self.assertTrue(response['Code'] == 200)


    # Folder APIs Test Cases
    def test_get_list_files(self):
        """
        Test case for get_list_files
        
        Get the file listing of a specific folder
        """
        response = self.api.get_list_files()
        self.assertTrue(response)

    def test_put_create_folder(self):
        """
        Test case for put_create_folder

        Create the folder 
        """
        folderName = "My Documents"
        response = self.api.put_create_folder(folderName)
        self.assertTrue(response)

    def test_post_move_folder(self):
        """
        Test case for post_move_folder
        
        Move a specific folder
        """
        srcFolder = "moveFrom"
        destFolder = "moveTo"
            
        response = self.api.post_move_folder(srcFolder, destFolder)
        self.assertTrue(response)

    def test_delete_folder(self):
        """
        Test case for delete_folder
        
        Remove a specific folder
        """
        folderName = 'Pictures'
        response = self.api.delete_folder(folderName)
        self.assertTrue(response['Code'] == 200)

    def test_put_copy(self):
        """
        Test case for put_copy
        
        Copy a specific file
        """
        path = "testfile.txt"
        newdest = os.path.join("My Documents", "testfile.txt")
        response = self.api.put_copy(path, newdest)
        self.assertTrue(response)

    def test_put_copy_folder(self):
        """
        Test case for put_copy_folder
        
        Copy a folder
        """
        path = "Word Documents"
        newdest = os.path.join("My Documents", "Word Documents")
        response = self.api.put_copy_folder(path, newdest)
        self.assertTrue(response)


    # Storage APIs Test Cases
    def test_get_is_storage_exist(self):
        """
        Test case for get_is_storage_exist
        
        Check if storage exists
        """
        storageName = "First Storage"
        response = self.api.get_is_storage_exist(storageName)
        self.assertTrue(response.is_exist)

    def test_get_is_exist(self):
        """
        Test case for get_is_exist

        Check if a specific file or folder exists
        """
        response = self.api.get_is_exist('testfile.txt')
        self.assertTrue(response.file_exist.is_exist)

    def test_get_disc_usage(self):
        """
        Test case for get_disc_usage
        
        Check the disk usage of the current account
        """
        response = self.api.get_disc_usage()
        self.assertTrue(response)

    def test_get_list_file_versions(self):
        """
        Test case for get_list_file_versions
        
        Get the file's versions list
        """
        fileName = 'testfile.txt'
        response = self.api.get_list_file_versions(fileName)
        self.assertTrue(response)

if __name__ == '__main__':
    unittest.main()
