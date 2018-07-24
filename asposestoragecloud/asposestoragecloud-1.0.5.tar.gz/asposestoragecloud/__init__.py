# --------------------------------------------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="__init__.py">
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

# import models into sdk package
from .models.access_token_response import AccessTokenResponse
from .models.aspose_response import AsposeResponse
from .models.disc_usage import DiscUsage
from .models.file_exist import FileExist
from .models.file_response import FileResponse
from .models.copy_file_response import CopyFileResponse
from .models.create_folder_response import CreateFolderResponse
from .models.disc_usage_response import DiscUsageResponse
from .models.file_exist_response import FileExistResponse
from .models.file_version import FileVersion
from .models.file_versions_response import FileVersionsResponse
from .models.files_response import FilesResponse
from .models.move_file_response import MoveFileResponse
from .models.move_folder_response import MoveFolderResponse
from .models.remove_file_response import RemoveFileResponse
from .models.remove_folder_response import RemoveFolderResponse
from .models.storage_exist_response import StorageExistResponse
from .models.upload_response import UploadResponse

# import apis into sdk package
from .apis.storage_api import StorageApi

# import ApiClient
from .api_client import ApiClient

from .configuration import Configuration
