import csv
import json, re
from functools import reduce #for 3.x if needed

import googleapiclient.discovery
from googleapiclient.errors import HttpError
from httplib2 import ServerNotFoundError
from google.auth.exceptions import TransportError

from ..oauth import creds_helper

SPREADSHEET_MIMETYPES = ['application/vnd.google-apps.spreadsheet']


def build_service(credentials):
    sheet_service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)
    return sheet_service

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


class GSheets(object):

    def __init__(self, sheets_service, drive_service=None, **kwargs):
        if not isinstance(sheets_service, googleapiclient.discovery.Resource):
            raise TypeError('given service parameter is not googleapiclient.discovery.Resource object')

        self.sheets_service = sheets_service

        # drive-service is used for retrieving sheet's modification time, etc. which is not possible through sheets-api
        # drive-service is not mandatory. if it is not given, then only functionality related to it will be disabled.
        if isinstance(drive_service, googleapiclient.discovery.Resource):
            self.drive_service = drive_service
            self.enable_drive_service_linking = True
        else:
            self.drive_service = None
            self.enable_drive_service_linking = False

        self.EXPOSE_BACKEND_ERRORS = kwargs.get('expose_backend_errors', True)

    @classmethod
    def from_credentials(cls, credentials, **kwargs):
        service = build_service(credentials)
        return cls(service, drive_service=None, **kwargs)

    @classmethod
    def from_creds_file(cls, creds_file, scopes, auth_through_service_account=False, **kwargs):
        credentials = creds_helper.credentials_from_file(creds_file, scopes, auth_through_service_account=auth_through_service_account)
        return cls.from_credentials(credentials, **kwargs)

    @classmethod
    def from_creds_string(cls, creds_string, scopes, auth_through_service_account=False, **kwargs):
        credentials = creds_helper.credentials_from_string(creds_string, scopes, auth_through_service_account=auth_through_service_account)
        return cls.from_credentials(credentials, **kwargs)

    #TODO give helper factory method, which includes gdrive_functionality also.

    def spreadsheet_details_for(self, spreadsheet_id, pargs=None):
        pargs = {} if pargs is None else pargs
        include_sheet_header_details = pargs.get('includeSheetHeaderDetails', 1)
        sheets_list = []
        try:
            sheets_response_table = self.sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        except HttpError as err:
            return error_response(message='error in getting details of requested spreadsheet',
                                  inherited_error_table=json.loads(err.content))
        except (ServerNotFoundError, TransportError) as err:
            return error_response(
                message='cannot connect to googleapis server to get spreadsheet details - ServerNotFoundError' if self.EXPOSE_BACKEND_ERRORS else 'cannot retrieve spreadsheet details')

        if self.enable_drive_service_linking:
            try:
                drive_meta_response_table = self.drive_service.files().get(fileId=spreadsheet_id, fields='id, name, mimeType, createdTime, modifiedTime').execute()
            except HttpError as err:
                return error_response(message='error in getting meta details of requested spreadsheet',
                                      inherited_error_table=json.loads(err.content))
            except (ServerNotFoundError, TransportError) as err:
                return error_response(
                    message='cannot connect to googleapis server to get spreadsheet meta information from drive - ServerNotFoundError' if self.EXPOSE_BACKEND_ERRORS else 'cannot retrieve meta details of spreadsheet')

        response_sheets_list = sheets_response_table.get('sheets', [])

        if include_sheet_header_details:
            try:
                sheets_headers_table = self.sheets_service.spreadsheets().values().batchGet(
                    spreadsheetId=spreadsheet_id,
                    ranges=[s['properties']['title'] + '!1:1' for s in response_sheets_list]
                ).execute()
            except HttpError as err:
                return error_response(message='error in getting sheet header fields details in requested spreadsheet',
                                      inherited_error_table=json.loads(err.content))
            except (ServerNotFoundError, TransportError) as err:
                return error_response(
                    message='cannot connect to googleapis server to get spreadsheet sheet header fields - ServerNotFoundError' if self.EXPOSE_BACKEND_ERRORS else 'cannot retrieve spreadsheet header fields')

        for count, sheet in enumerate(response_sheets_list):
            new_sheet = {}
            new_sheet['sheetGId'] = sheet.get('properties').get('sheetId')
            new_sheet['sheetTitle'] = sheet.get('properties').get('title')
            new_sheet['gridProperties'] = sheet.get('properties').get('gridProperties')

            if include_sheet_header_details:
                sheet_headers_table = sheets_headers_table['valueRanges'][count]
                headers_row = [s.lstrip() for s in sheet_headers_table['values'][0]]
                hdr_split = [e.split(' ', 1) if ' ' in e else [e, ''] for e in headers_row]
                (cols, coldescs) = zip(*hdr_split)
                new_sheet['fields'] = list(cols)
                new_sheet['fieldDescs'] = list(coldescs)

            sheets_list.append(new_sheet)

        our_response_table = {'kind': 'spreadsheetDetails', 'spreadsheetId': spreadsheet_id}
        our_response_table['spreadsheetUrl'] = sheets_response_table.get('spreadsheetUrl')
        our_response_table['spreadsheetName'] = sheets_response_table.get('properties').get('title')

        if self.enable_drive_service_linking:
            #fallowing details are only details we get from drive-service
            our_response_table['createdTime'] = drive_meta_response_table.get('createdTime')
            our_response_table['modifiedTime'] = drive_meta_response_table.get('modifiedTime')

        our_response_table['sheets'] = sheets_list

        return (our_response_table), 200


    def sheet_values_for(self, spreadsheet_id, sheet_id, pargs=None):
        pargs = {} if pargs is None else pargs
        id_type = pargs.get('idType', 'gid')
        values_format = pargs.get('valuesFormat', 'maps')
        reqd_fields = pargs.get('fields', None)
        reqd_range_str = pargs.get('range', None)
        value_render_option = pargs.get('valueRenderOption', 'FORMATTED_VALUE')
        date_time_render_option = pargs.get('dateTimeRenderOption', 'SERIAL_NUMBER')

        if reqd_range_str:
            reqd_range_match = re.compile(r'^(\d+):(\d+)$').match(reqd_range_str)
            if reqd_range_match is None or int(reqd_range_match.group(1)) < 1:
                return error_response(code=400, message='illegal range')

        if id_type not in ['gid', 'title']:
            return error_response(code=400, message='invalid idType parameter')

        if values_format not in ['rows', 'columns', 'maps']:
            return error_response(code=400, message='invalid valuesFormat parameter')

        if value_render_option not in ['FORMATTED_VALUE', 'UNFORMATTED_VALUE', 'FORMULA']:
            return error_response(code=400, message='invalid valueRenderOption parameter')

        if date_time_render_option not in ['SERIAL_NUMBER', 'FORMATTED_STRING']:
            return error_response(code=400, message='invalid dateTimeRenderOption parameter')

        sheet_id = int(sheet_id) if id_type == 'gid' else sheet_id

        try:
            sheets_response_table = self.sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        except HttpError as err:
            return error_response(message='error in getting sheets details in requested spreadsheet',
                                  inherited_error_table=json.loads(err.content) if self.EXPOSE_BACKEND_ERRORS else {})
        except (ServerNotFoundError, TransportError) as err:
            return error_response(
                message='cannot connect to googleapis server to get sheets details in requested spreadsheet - ServerNotFoundError' if self.EXPOSE_BACKEND_ERRORS else 'cannot retrieve sheets details in requested spreadsheet')

        response_sheets_list = sheets_response_table.get('sheets', [])
        sheet_gid_title_map = {}
        for sheet in response_sheets_list:
            _sheet_gid = sheet.get('properties').get('sheetId')
            _sheet_title = sheet.get('properties').get('title')
            sheet_gid_title_map[_sheet_gid] = _sheet_title

        is_sheet_in_spreadsheet = (sheet_id in sheet_gid_title_map.keys()) if (id_type == 'gid') else (
                    sheet_id in sheet_gid_title_map.values())

        if not is_sheet_in_spreadsheet:
            return error_response(code=404, message='requested sheet is not there in parent spreadsheet')

        sheet_title = (sheet_id) if id_type == 'title' else sheet_gid_title_map.get(sheet_id)
        sheet_gid = sheet_id if id_type == 'gid' else reduce(
            (lambda x, y: x if (sheet_gid_title_map.get(x) == sheet_id) else y), sheet_gid_title_map.keys())

        reqd_range = (sheet_title + '!' + '{fr}:{tr}'.format(fr=int(reqd_range_match.group(1)) + 1, tr=int(
            reqd_range_match.group(2)) + 1)) if reqd_range_str else sheet_title + '!2:2000000'
        request_ranges = [sheet_title + '!1:1', reqd_range]

        try:
            response_table = self.sheets_service.spreadsheets().values().batchGet(
                spreadsheetId=spreadsheet_id,
                ranges=request_ranges,
                valueRenderOption=value_render_option,
                dateTimeRenderOption=date_time_render_option
            ).execute()
        except HttpError as err:
            return error_response(message='error in getting sheet values in requested spreadsheet',
                                  inherited_error_table=json.loads(err.content))
        except (ServerNotFoundError, TransportError) as err:
            return error_response(
                message='cannot connect to googleapis server to get values in requested spreadsheet - ServerNotFoundError' if self.EXPOSE_BACKEND_ERRORS else 'cannot retrieve sheet values in requested spreadsheet')

        table = {'sheetTitle': sheet_title}

        headers_range_values = response_table.get('valueRanges')[0].get('values')
        if not len(headers_range_values):
            return error_response(code=404, message='requested sheet is empty')
        headers_row = [s.lstrip() for s in headers_range_values[0]]
        hdr_split = [e.split(' ', 1) if ' ' in e else [e, ''] for e in headers_row]
        (cols, coldescs) = zip(*hdr_split)
        idx = dict(zip(cols, range(len(cols))))
        table['fields'] = list(cols)
        table['descs'] = list(coldescs)
        table['values'] = []

        for row in response_table.get('valueRanges')[1].get('values'):
            if not len(row):
                continue

            if row[0].startswith('#'):
                continue

            if (not True in [not (re.match(r'^[\s\-]*$', e)) for e in row]):
                # TODO provide option to give filler charcters to be filtered.
                # should check a way to escape regex components in a string
                continue

            values_row = row
            if len(values_row) < len(table.get('fields')):
                values_row += [''] * (len(table.get('fields')) - len(values_row))

            table['values'].append(values_row)

        reqd_fields = table.get('fields') if (reqd_fields is None) else reqd_fields
        fields_not_existed = [rf for rf in reqd_fields if rf not in table.get('fields')]

        if len(fields_not_existed):
            return error_response(code=404, message='fields ' + reduce((lambda x, y: x + ',' + y), fields_not_existed)[
                                                                :] + ' doesn\'t exist in requested sheet.')

        reqd_field_indices = [idx[field] for field in reqd_fields]
        final_table = {'sheetTitle': sheet_title}
        final_table['fields'] = [table['fields'][i] for i in reqd_field_indices]
        final_table['descs'] = [table['descs'][i] for i in reqd_field_indices]
        final_table['values'] = [[table['values'][i][j] for j in reqd_field_indices] for i in
                                 range(len(table['values']))]

        our_response_table = {
            'spreadsheetId': spreadsheet_id,
            'sheetGId': sheet_gid,
            'sheetTitle': sheet_title,
            'valuesFormat': values_format,
            'fields': final_table['fields'],
            'fieldDescs': final_table['descs']
        }

        our_response_table['values'] = {
            'rows': final_table['values'],
            'columns': [[final_table['values'][i][j] for i in range(len(final_table['values']))] for j in
                        range(len(final_table['fields']))],
            'maps': [dict(zip(final_table['fields'], valrow)) for valrow in final_table['values']]
        }.get(values_format)

        return our_response_table, 200

    def raw_get(self, spreadsheet_id, pargs=None):
        pargs = {} if pargs is None else pargs

        try:
            sheets_response_table = self.sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

        except HttpError as err:
            error_table = json.loads(err.content)
            return error_table, error_table.get('error', {}).get('code', 500)

        except (ServerNotFoundError, TransportError) as err:
            return error_response(
                message='cannot connect to googleapis server to get spreadsheet details - ServerNotFoundError' if self.EXPOSE_BACKEND_ERRORS else 'cannot retrieve spreadsheet details')

        return sheets_response_table, 200


    def raw_values_get(self, spreadsheet_id, range_string, pargs=None):
        pargs = {} if pargs is None else pargs

        try:
            response_table = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_string,
                majorDimension=pargs.get('majorDimension', 'ROWS'),
                valueRenderOption=pargs.get('valueRenderOption', 'FORMATTED_VALUE'),
                dateTimeRenderOption=pargs.get('dateTimeRenderOption', 'SERIAL_NUMBER')
            ).execute()

        except HttpError as err:
            error_table = json.loads(err.content)
            return error_table, error_table.get('error', {}).get('code', 500)

        except (ServerNotFoundError, TransportError) as err:
            return error_response(
                message='cannot connect to googleapis server to get spreadsheet values - ServerNotFoundError')

        return response_table, 200


    def raw_values_batch_get(self, spreadsheet_id, range_strings, pargs=None):
        pargs = {} if pargs is None else pargs

        try:
            response_table = self.sheets_service.spreadsheets().values().batchGet(
                spreadsheetId=spreadsheet_id,
                ranges=range_strings,
                majorDimension=pargs.get('majorDimension', 'ROWS'),
                valueRenderOption=pargs.get('valueRenderOption', 'FORMATTED_VALUE'),
                dateTimeRenderOption=pargs.get('dateTimeRenderOption', 'SERIAL_NUMBER')
            ).execute()

        except HttpError as err:
            error_table = json.loads(err.content)
            return error_table, error_table.get('error', {}).get('code', 500)

        except (ServerNotFoundError, TransportError) as err:
            return error_response(
                message='cannot connect to googleapis server to get values in requested spreadsheet - ServerNotFoundError')

        return response_table, 200


    ''' Some wrapper helper methods now on. which may help in some cases '''

    def sheets_dict_for(self, spreadsheet_id):
        '''
        just gives a dict mapping inner sheet ids to their titles in given spreadsheet.
        :method spreadsheet_details_for: gives much comprehensive result with all sheets list, and header fields. where as this one gives just small mapping from all gids to titles.

        :param spreadsheet_id: spreadsheetId
        :return: dict of sheet_gids to sheet titles in given spreadsheet. None if any error occurs
        '''
        sheets_response_table, code = self.spreadsheet_details_for(spreadsheet_id, pargs={"include_sheet_header_details":0})
        if 'error' in sheets_response_table:
            return None

        sheets_dict = {}
        for sheet in sheets_response_table['sheets']:
            sheets_dict[sheet['sheetGId']] = sheet['sheetTitle']

        return sheets_dict

    def to_csv(self, spreadsheet_id, sheet_id, csv_file, id_is_title=False, comment_out_first_row=True):
        sheets_dict = self.sheets_dict_for(spreadsheet_id);
        sheet_in_spreadsheet = sheet_id in list(sheets_dict.values()) if id_is_title else  sheet_id in list(sheets_dict.keys())
        if not sheet_in_spreadsheet:
            return
        sheet_title = sheet_id if id_is_title else sheets_dict[sheet_id]
        range = sheet_title

        sheet_values_table, code = self.raw_values_get(spreadsheet_id, range)
        if 'error' in sheet_values_table:
            return
        values = sheet_values_table['values']

        csv_writer = csv.writer(csv_file)
        gothdr = False
        for row in values:
            if not gothdr:
                gothdr = True
                row[0] = "#"+row[0] if comment_out_first_row else row[0]

            csv_writer.writerow(row)



def spreadsheet_id_from_url(url):
    found = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
    if not found:
        return None
    else:
        return found.groups()[0]

def spreadsheet_url_from_id(id):
    return 'https://docs.google.com/spreadsheets/d/{id}/edit'.format(id=id)


