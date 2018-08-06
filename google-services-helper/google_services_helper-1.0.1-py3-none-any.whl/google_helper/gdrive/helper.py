
import json

import googleapiclient.discovery
from googleapiclient.errors import HttpError
from httplib2 import ServerNotFoundError
from google.auth.exceptions import TransportError

from ..oauth import creds_helper

SPREADSHEET_MIMETYPES = ['application/vnd.google-apps.spreadsheet']


def build_service(credentials):
    drive_service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
    return drive_service

def build_service_from_creds_file(creds_file, scopes, auth_through_service_account=False):
    credentials = creds_helper.credentials_from_file(creds_file, scopes, auth_through_service_account)
    return build_service(credentials)

def build_service_from_creds_string(creds_string, scopes, auth_through_service_account=False):
    credentials = creds_helper.credentials_from_string(creds_string, scopes, auth_through_service_account)
    return build_service(credentials)


def error_response(**kwargs):
    #print ('in error_response')
    response = {'error' : {}}
    is_error_inherited = 'inherited_error_table' in kwargs
    response_code = kwargs.get('code', kwargs['inherited_error_table']['error'].get('code', 500) if is_error_inherited else 500)
    response_message = kwargs.get('message', None)

    response['error']['code'] = response_code
    if response_message is not None :
        response['error']['message'] = response_message
    if is_error_inherited :
        response['error']['inherited_error'] = kwargs['inherited_error_table']['error']

    return (response), response_code

class GDrive(object):

    def __init__(self, drive_service, **kwargs):
        if not isinstance(drive_service, googleapiclient.discovery.Resource):
            raise TypeError('given service parameter is not googleapiclient.discovery.Resource object')

        self.drive_service = drive_service
        self.EXPOSE_BACKEND_ERRORS = kwargs.get('expose_backend_errors', True)


    @classmethod
    def from_credentials(cls, credentials, **kwargs):
        service = build_service(credentials)
        return cls(service, **kwargs)

    @classmethod
    def from_creds_file(cls, creds_file, scopes, auth_through_service_account=False, **kwargs):
        credentials = creds_helper.credentials_from_file(creds_file, scopes, auth_through_service_account=auth_through_service_account)
        return cls.from_credentials(credentials, **kwargs)

    @classmethod
    def from_creds_string(cls, creds_string, scopes, auth_through_service_account=False, **kwargs):
        credentials = creds_helper.credentials_from_string(creds_string, scopes, auth_through_service_account=auth_through_service_account)
        return cls.from_credentials(credentials, **kwargs)

    def list_of_files(self, pargs=None):
        '''
        this is generic function to retrieve list of files in all pages. you have to provide all query parameters like q string, orderBy etc.
        Note: see listOfFilesInFolder() method for listing files in a folder of desired type.

        :param pargs: query string parameters for google drive api 'list' method.
         see https://developers.google.com/drive/api/v3/reference/files/list for all avialable.
        :return: a tuple of (dictionary with 'files' key, and equivalent response http code).
        '''

        pargs = {} if pargs is None else pargs

        files_list = []
        page_token = None

        while True:
            try:
                present_page_response_table = self.drive_service.files().list(
                    pageToken=page_token,
                    **pargs
                ).execute()
            except HttpError as err:
                return error_response(message='error in retrieving list of files from gdrive directory',
                                      inherited_error_table=json.loads(err.content))
            except (ServerNotFoundError, TransportError) as err:
                return error_response(
                    message='cannot connect to googleapis server to get list of files from gdrive directory - ServerNotFoundError' if self.EXPOSE_BACKEND_ERRORS else 'cannot retrieve list of files from gdrive directory')

            present_page_files_list = present_page_response_table.get('files', [])

            files_list.extend(present_page_files_list)
            page_token = present_page_response_table.get('nextPageToken', None)
            if page_token is None:
                break

        our_response_table = {'kind': 'listOfFiles', 'files': files_list}
        return (our_response_table), 200

    def list_of_files_in_folder(self, folder_id, mime_types=None,
                                additional_pargs=None):
        '''
        returns an array of file objects, which have :param folderId: in their 'parent' attribute in google drive. note that, in gdrive, there is no concept of folders.
        it is just relations between differant files, like parent-child relation ships. a folder is also a file with proprietery mimeType. children files just have this folder-file id in their parent attribute.

        :param folder_id: id of the google drive folder
        :param mime_types: required mimeTypes in that folder.
        :param additional_pargs: any additional pargs, like orderBy.
        :return: a tuple of (dictionary with 'files' key, and equivalent http status code)
        '''
        # TODO should also accept custom mimeType expression including negations and all.

        additional_pargs = {} if additional_pargs is None else additional_pargs
        mime_types = mime_types if mime_types else SPREADSHEET_MIMETYPES

        mime_types_clause = '(' + (' or '.join(["mimeType='{}'".format(mt) for mt in mime_types])) + ')'

        q_parameter = "'" + folder_id + "'" + ' in parents' + ' and ' + mime_types_clause
        order_by_parameter = additional_pargs.get('orderBy', 'name_natural')
        fields_parameter = 'nextPageToken, files(id, name, mimeType, createdTime, modifiedTime)'

        pargs = {
            'orderBy': order_by_parameter,
            'q': q_parameter,
            'fields': fields_parameter
        }

        our_response_table, code = self.list_of_files(pargs=pargs)

        if 'error' in our_response_table:
            return (our_response_table), code

        our_response_table['kind'] = 'listOfFilesInFolder'
        our_response_table['folderId'] = folder_id

        return (our_response_table), code








