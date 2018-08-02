"""
    Create Assetic requests from CRM and Update CRM with Assetic changes
"""

import datetime
import dateutil.parser
from pprint import pformat
import six
import os
import time
import abc
from ..api_client import ApiClient
from ..rest import ApiException
from ..api import WorkOrderApi
from ..api import WorkRequestApi
from ..api import AssetApi
from ..api import DocumentApi
from ..tools import AssetTools
from ..tools import OData
from ..models.assetic3_integration_representations_work_request\
    import Assetic3IntegrationRepresentationsWorkRequest
from ..models.assetic3_integration_representations_document_representation \
    import Assetic3IntegrationRepresentationsDocumentRepresentation

class CRMTools(object):
    """
    Class to provide Work Request integration processes
    """

    def __init__(self, crm, api_client=None, **kwargs):
        """
        initialise object
        :param crm: The CRM to integrated to. Currently support "Authority"
        :param api_client: sdk client object, optional
        :param **kwargs: provide any config specific to the CRM
        """
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        self.logger = api_client.configuration.packagelogger

        self.assettools = AssetTools()
        self.wrapi = WorkRequestApi()
        self.wkoapi = WorkOrderApi()
        self.assetapi = AssetApi()
        self.odata = OData()
        self.docapi = DocumentApi()

        self._crm_name = crm
        self._crm_tools = None
        if crm.lower() == "authority":
            self._crm_tools = self.init_authority_crm(**kwargs)
        elif crm.lower() == "authoritytest":
            self._crm_tools = self.init_authority_crm_test(**kwargs)
        else:
            self.logger.error("'{0}' is an unsupported CRM plugin.\nSupported"
                              " CRM plugins are 'Authority'".format(crm))

        self._wo_status_note = dict()
        self._wr_status_note = dict()

        # use Assetic documents to record last integration dates
        self._wr_last_date_doc_id = None
        self._wo_last_date_doc_id = None

    @property
    def crm_tools(self):
        """
        Reference to the instantiated CRM class
        """
        return self._crm_tools

    @property
    def wo_status_note(self):
        """
        A dictionary where key is wo status and value is what to use for note
        """
        return self._wo_status_note

    @wo_status_note.setter
    def wo_status_note(self, wo_status_note):
        self._wo_status_note = wo_status_note

    @property
    def wr_status_note(self):
        """
        A dictionary where key is wr status and value is what to use for note
        """
        return self._wr_status_note

    @wr_status_note.setter
    def wr_status_note(self, wr_status_note):
        self._wr_status_note = wr_status_note

    def init_authority_crm(self,**kwargs):
        """
        Initialise the plugin for Authority integration
        :param **kwargs: set of keyword arguments with Authority specific
        parameters
        :return: The plugin which implements class ECMSPluginBase
        """
        try:
            from .crm_plugins.authority_crm import AuthorityCRM
            from .crm_plugins.authority_crm import AuthorityAsseticResolutionCodes
            crm_plugin = AuthorityCRM(**kwargs)
            return crm_plugin
        except ImportError as ex:
            self.logger.error(str(ex))
            return None

    def init_authority_crm_test(self,**kwargs):
        """
        Initialise the test plugin for Authority integration
        :param **kwargs: set of keyword arguments with Authority specific
        parameters
        :return: The plugin which implements class ECMSPluginBase
        """
        try:
            from .crm_plugins.authority_crm import AuthorityCRMtest
            crm_plugin = AuthorityCRMtest(**kwargs)
            return crm_plugin
        except ImportError as ex:
            self.logger.error(str(ex))
            return None

    def process(self):
        # first process existing requests
        self.logger.info("Process Changed Work Requests - Start")
        chk = self.process_changed_work_requests()
        self.logger.info("Process Changed Work Requests - Complete")

        # next process new requests
        self.logger.info("Create Work Requests for new CRM - Start")
        chk = self.process_new_crms()
        self.logger.info("Create Work Requests for new CRM - Complete")

        return chk

    def process_new_crms(self):
        """
        Look for new customer requests and process them.
        Returned: 0=success, else error
        """
        crms = self.crm_tools.get_crm_requests(integrated=False)
        if isinstance(crms, int):
            # there was an error so exit
            return crms
        if crms is None:
            # expecting a list from plugin, empty list if no records
            self.logger.warning("Alter plugin to return an empty list if there"
                                "are no new requests.  Assuming there are no"
                                " new requests.")
            crms = list()
        self.logger.info("Found {0} new CRM's to create a Work Request for".
                         format(len(crms)))
        for wr_crm_obj in crms:
            wr = Assetic3IntegrationRepresentationsWorkRequest()
            # Double check to see if CRM ID already in Assetic
            # TODO return wr as Assetic3IntegrationRepresentationsWorkRequest
            wr_guid = self.get_wr_guid_for_crm_id(wr_crm_obj.crm_id)
            if isinstance(wr_guid, int):
                # there was an error
                return wr_guid
            if wr_guid is None:
                # CRM definitely not in Assetic yet.  So create it
                self.logger.info(
                    "Create new Work Request for CRM {0}".
                    format(wr_crm_obj.crm_id))
                wr_json = self.create_request(wr_crm_obj)
                if isinstance(wr_json, int):
                    # there was an error
                    return wr_json
            else:
                # there is an existing WR, so just update CRM.  May have
                # failed on last attempt to update
                self.logger.warning("Work Request [{0}] already exists for CRM "
                                    "[{1}]".format(wr_guid, wr_crm_obj.crm_id))
                wr_json = self.wrapi.work_request_get(wr_guid)
                if isinstance(wr_json, int):
                # there was an error
                    return wr_json

            ##set some of the key wr properties
            wr.id = wr_json["Id"]
            wr.friendly_id_str = wr_json["FriendlyIdStr"]

            # update CRM with AsseticID and note
            wr_crm_obj.assetic_wr_representation = wr
            friendly_id = wr.friendly_id_str
            comment = "[Created Request in Assetic: {0}]".format(friendly_id)
            chk = self.crm_tools.update_crm_for_new_wr(wr_crm_obj, comment)
            if chk != 0:
                # there was an error
                return chk
            self.logger.info("Created New Work Request {0}".format(
                wr.friendly_id_str))
        return 0

    def create_request(self, wr_crm_obj):
        """
        Create a new Work Request in Assetic that corresponds with a
        Customer Request task.
        This will update the crm with the new Assetic Work Request GUID
        :param wr_crm_obj: object with raw crm data and work request
        representation
        :return work request json object, else error code
        """

        # create request
        wr_guid = self.wrapi.work_request_post(
            wr_crm_obj.assetic_wr_representation)
        if isinstance(wr_guid, int):
            self.logger.warning("Work Request Not Created in Assetic")
            return wr_guid

        # get the the Assetic work request and return.  It has the generated Id
        return self.get_request(wr_guid)

    def process_changed_work_requests(self):
        """
        Get list of requests from CRM where the CRM is still
        active. Assumes CRM is not closed until Assetic request is closed
        Returned: 0=success, else error
        """
        # get CRM's from CRM that are still active
        crms = self.crm_tools.get_crm_requests(integrated=True)
        if isinstance(crms, int):
            ##there was an error so exit
            return crms

        # First Apply work order status changes and comments
        # because request may close CRM and so can't find crm
        chk = self.apply_wo_status_comment(crms)

        # get the last datetime the process ran
        lastdate = self.get_last_integration_datetime_from_doc_link(
            "workrequest")

        # seed max change date to last datetime
        maxdate = lastdate
        self.logger.info("Search for Assetic changes since {0}".format(
            lastdate))

        int_date = datetime.datetime.now()

        # get list of modified work requests from Assetic since last run check
        wrs = self.get_changed_wr_since_date(lastdate)
        if isinstance(wrs, int):
            # there was an error so exit
            return wrs
        if len(wrs) > 0:
            # search ordered by last_mod_date desc, so get max date
            # change datetime to local
            maxdate = self._get_datetime_from_utc_string(wrs[0]
                                                         ["WRLastModified"])
            self.logger.info("Most recent Assetic change was {0}".format(
                maxdate))
        else:
            self.logger.info(
                "No changes to Assetic Requests found since last check")

        for wr in wrs:
            new_note = None
            bclose_crm_task = False
            new_status = None

            # get status and supporting info unless newly created request
            if wr["WRCreatedDateTime"] != wr["WRLastModified"]:
                # something has changed in this work request since last check.
                # if status date is greater than lastdate then status
                # has changed.  status date is null if NEW request
                status_date = self._get_datetime_from_utc_string(
                    wr["WRStatusDateTime"])
                if status_date is not None and status_date > lastdate:
                    self.logger.debug("New status [{0}] for [{1}]".format(
                        wr["WRStatus"], wr["WorkRequestFID"]))
                    new_status = wr["WRStatus"]

                enddate = maxdate
                if wr["WRStatus"] == "Resolved" or wr["WRStatus"] == "Closed" \
                        or wr["WRStatus"] == "Rejected":
                    # all comments, including those after last mod date becuase
                    # we will be closing the task, so set end date in future
                    # (just in case) so that all remaining supporting info
                    # is returned
                    enddate = maxdate + datetime.timedelta(days=1)
                    # flag to update CRM Task as complete
                    bclose_crm_task = True
                # get WR comments in date range
                info = self.get_wr_comments_in_range(wr["WorkRequestId"],
                                                     lastdate, enddate)
                if isinstance(info, int):
                    # there was an error so exit
                    return wr

                if new_status or (info and len(info) > 0):
                    # get current CRM note to make sure we aren't
                    # doubling up
                    current_note = self.crm_tools.get_task_note_from_crm(
                        wr["WRExternalId"])
                    if isinstance(current_note, int):
                        # there was an error getting note
                        return current_note

                    if new_status in self.wr_status_note and \
                            self.wr_status_note[new_status] not in current_note:
                        # this status not in crm note so include
                        new_note = "{0} {1} {2}".format(
                            self._get_datetime_from_utc_string(wr["WRLastModified"]).
                                strftime("%d-%m-%Y %H:%M")
                            , wr["WorkRequestFID"]
                            ," Status: {0}".format(self.wr_status_note[new_status]))

                    if info and info not in current_note:
                        # also supporting info to add.
                        if new_note is None:
                            new_note = "{0} {1} {2}".format(
                                self._get_datetime_from_utc_string(wr["WRLastModified"]).
                                    strftime("%d-%m-%Y %H:%M")
                                , wr["WorkRequestFID"], info)
                        else:
                            new_note += "; " + info

            if new_note or bclose_crm_task:
                found_crm = False
                # add comment as a note to task in CRM
                # find the crm from the list of active crms
                for crm in crms:
                    if crm.assetic_wr_representation.id == wr["WorkRequestId"]:
                        found_crm = True
                        if new_note is not None:
                            new_note = "[{0}]".format(new_note)
                            self.crm_tools.add_task_note_to_crm(new_note,
                                                                crm.crm_representation)
                            # could also add comment at the request level?
                            # self.add_file_note_to_crm(new_note,crm.formatted_account)

                        if bclose_crm_task:
                            crm_code_obj = self.crm_tools. \
                                get_resolution_code_for_subtask(
                                wr["WRSubType"], crm.crm_representation)
                            if wr["WRStatus"] == "Rejected":
                                crm_code = crm_code_obj.crm_rejection_code
                            else:
                                crm_code = crm_code_obj.crm_resolution_code

                            close_date = status_date
                            # update task status as complete
                            chk = self.crm_tools.update_crm_task_status(
                                crm.crm_representation
                                , crm_code
                                , close_date)
                            # update entire CRM record status as complete
                            if crm_code_obj.close_crm:
                                chk = self.crm_tools.update_crm_master_status(
                                    crm.crm_representation,
                                    crm_code, close_date)
                        break
                if not found_crm:
                    # didn't find the crm in the list.  Just log a warning
                    msg = "Couldn't find an active {0} CRM task for " \
                          "Assetic Request {1}".format(self._crm_name,
                                                       wr["WorkRequestFID"])
                    self.logger.warning(msg)

        if maxdate == lastdate:
            maxdate = int_date
        # update sync date
        chk = self.set_last_integration_datetime_via_doc_link(
            "workrequest", maxdate)
        return chk

    def get_wr_comments_in_range(self, wrguid, startdate, enddate):
        """
        Given a work request object get comments in date range.
        :param wrguid: The id of the work request
        :param startdate: the minimum date
        :param enddate: the maximum date
        Returned: return formatted comment string
        """
        info_list = self.get_supporting_info(wrguid)
        if isinstance(info_list, int):
            # there was an error
            return info_list

        comment = None
        for h in info_list:
            # temp fix for datetime as bug
            hdate = dateutil.parser.parse(h["CreatedDateTime"])
            # if hdate.tzinfo!= startdate.tzinfo:
            #    hdate = hdate.replace(tzinfo = startdate.tzinfo)
            if hdate >= startdate and hdate <= enddate and h[
                "CreatedByDisplayName"] != "CRM Integration":
                # new = "{0} {1}".format(hdate.strftime("%d-%m-%Y %H:%M"),
                #                       h["Description"])
                new = h["Description"]
                if comment is None:
                    comment = new
                else:
                    comment = comment + ' ' + new
        return comment

    def apply_wo_status_comment(self, crms):
        """
        apply any work order comments or status changes since last check
        :param crms: a list of active crm objects from CRM
        :return 0=success, else error
        """

        # get the last datetime the process ran
        last_date = self.get_last_integration_datetime_from_doc_link(
            "workorder")

        # get a list of work orders where status has changed
        wos_new_status = self.get_wos_with_new_status(last_date)

        # comment_status
        comment_status = self._wo_status_note

        # Get a list of request related work orders where something has changed
        wos = self.get_changed_wo(last_date)
        if isinstance(wos, int):
            return wos
        max_date = last_date
        if len(wos) > 0:
            max_date = dateutil.parser.parse(wos[0]["LastModified"])
        if max_date == last_date:
            # no changes so return
            return 0
        for wo in wos:
            # get each linked work request and process for each
            for wr in wo["LinkedWorkRequests"]:
                new_comments = list()
                # are there new supporting info comments?
                for supp_info in wo["SupportingInformation"]:
                    if last_date < dateutil.parser.parse(
                            supp_info["CreatedDateTime"]) <= max_date:
                        # there is a comment in date range
                        new_comments.append(supp_info)

                # if there is either status or history then get CRM
                # so we can get current note and make sure not doubling up
                # and then add note to CRM
                if wo["Id"] in wos_new_status or len(new_comments) > 0:
                    current_note = ""
                    current_crm = None
                    for crm in crms:
                        if crm.assetic_wr_representation.id.strip() == wr["ID"]:
                            current_crm = crm
                            # get current comments in crm
                            current_note = self.crm_tools.get_task_note_from_crm(
                                crm.crm_id)
                            if isinstance(current_note, int):
                                # there was an error getting note
                                return current_note
                            # got the crm and current note so exit loop
                            break

                    if not current_crm:
                        # couldn't find crm.
                        msg = "Couldn't find an active {0} CRM task for " \
                              "Assetic Request {1}".format(
                            self._crm_name, wr["FriendlyID"])
                        self.logger.warning(msg)
                        # can't add note so break to next work request
                        break

                    new_note = None
                    if wo["Status"] in comment_status and \
                            comment_status[wo["Status"]] not in current_note:
                        # this status not already in crm note so include
                        new_note = "{0} {1} {2}".format(
                            dateutil.parser.parse(wo["LastModified"]).
                                strftime("%d-%m-%Y %H:%M")
                            , wo["FriendlyIdStr"]
                            , " Status: {0}".format(comment_status[wo["Status"]]))
                    for comment in new_comments:
                        if comment["Description"] not in current_note and new_note is None:
                        # add comment as a note to task in CRM
                        # could also add comment at the request level?
                        # self.add_file_note_to_crm(comment,current_crm.formatted_account)
                        # update sync date
                            new_note = "{0} {1} {2}".format(
                                dateutil.parser.parse(wo["LastModified"]).
                                    strftime("%d-%m-%Y %H:%M")
                                , wo["FriendlyIdStr"]
                                , comment["Description"])
                        else:
                            new_note += "; " + comment["Description"]
                    if new_note is not None:
                        # wrap in brackets to neaten appearance
                        new_note = "[{0}]".format(new_note)
                        self.crm_tools.add_task_note_to_crm(new_note.strip(),
                                                    current_crm.crm_representation)

                    self.set_last_integration_datetime_via_doc_link(
                        "workorder", max_date)
        return 0

    def get_request(self, wrguid):
        """
        Get the work request object for a given work request guid
        :param wrguid: work request guid
        :return: assetic.Assetic3IntegrationRepresentationsWorkRequest
        """
        try:
            wrget = self.wrapi.work_request_get(wrguid)
        except ApiException as e:
            self.logger.error("Status {0}, Reason: {1} {2}".format(
                e.status, e.reason, e.body))
            return e.status
        return wrget

    def get_supporting_info(self, wrguid):
        """
        Get the work request object for a given work request guid
        :param wrguid: work request guid
        :return: list of supporting information objects
        """
        try:
            wrinfo = self.wrapi.work_request_get_supporting_information_for_work_request(
                wrguid)
        except ApiException as e:
            self.logger.error("Status {0}, Reason: {1} {2}".format(
                e.status, e.reason, e.body))
            return e.status
        return wrinfo["ResourceList"]

    def get_asset_by_extid(self, extid):
        """
        Get the core asset fields for the external ref id
        :params extid: external ref id
        :returns: return the core attributes as a json object or None
        """
        ##define page size (no of records) and page number to get
        pagesize = 1
        qfilter = "ExternalIdentifier='{0}'".format(extid)
        pagenum = 1
        kwargs = {"request_params_page": pagenum,
                  "request_params_page_size": pagesize,
                  "request_params_filters": qfilter}
        attributes = list()

        ##now execute the request
        try:
            response = self.assetapi.asset_get_0(attributes, **kwargs)
        except ApiException as e:
            self.logger.error("Status {0}, Reason: {1} {2}".format(
                e.status, e.reason, e.body))
            return None

        if len(response["ResourceList"]) == 1:
            return response["ResourceList"][0]
        else:
            return None

    def get_changed_wr_since_date(self, min_date):
        """
        Get a list of Assetic requests that have status date greater than
        or equal to supplied date.  Filter not down to milliseconds so need to
        consider a change within the mindate second
        Uses OData as there is no filtered get for requests,plus statusdate
        is only available in OData search and not the API
        :param min_date: the date to filter by
        :returns: list of request id's and status as JSON from OData endpoint
        """
        # search require datetime with offset. Might be a bit awkward for the
        # couple of hours around daylight savings changeover
        date_filter = self._get_utc_string_with_offset(min_date)
        if date_filter is None:
            return 1
        fields = "WorkRequestId,WRStatus,WRStatusDateTime,WRLastModified," \
                 "WorkRequestFID,WRSupportingInformation,WRCreatedDateTime" \
                 ",WRType,WRSubType,WRExternalId"
        top = 10000
        skip = 0
        qfilter = "WRLastModified ge {0}".format(date_filter)
        orderby = "WRLastModified desc"
        try:
            wrs = self.odata.get_odata_data("workrequest", fields, qfilter,
                                            top, skip, orderby)
        except ApiException as e:
            self.logger.error("Status {0}, Reason: {1} {2}".format(
                e.status, e.reason, e.body))
            return e.status
        if not wrs:
            # no records found, but no error. Return empty list
            wrs = list()
        return wrs

    def get_wr_guid_for_crm_id(self, crm_id):
        """
        Get Assetic work request for given crm_id.  Filter on WRExternalId
        Uses OData as there is no filtered get for requests
        :param crm_id: the CRM id to filter by
        :returns: a single request id or None
        """

        fields = "WorkRequestId"
        top = 1
        skip = 0
        qfilter = "WRExternalId eq '{0}'".format(crm_id)
        orderby = None
        try:
            wrs = self.odata.get_odata_data("workrequest", fields, qfilter
                                            , top, skip, orderby)
        except ApiException as e:
            self.logger.error("Status {0}, Reason: {1} {2}".format(
                e.status, e.reason, e.body))
            return e.status
        if len(wrs) > 0:
            return wrs[0]["WorkRequestId"]
        else:
            return None

    def get_changed_wo(self, min_date):
        """
        Get a list of Assetic work orders that have last mod date greater than
        supplied date
        :param min_date: the min date to filter by
        :returns: list of work orders
        """
        if not isinstance(min_date, datetime.datetime):
            self.logger.error("Must provide a datetime object for date search")
            return 1

        kwargs = {'request_params_page': 1,
                  'request_params_page_size': 500,
                  'request_params_sorts': "LastModified-desc",
                  'request_params_filters': "LastModified~gt~'{0}'~and~ExternalId~neq~''".format(
                      min_date.strftime("%Y-%m-%dT%H:%M:%S"))
                  }
        try:
            wko = self.wkoapi.work_order_integration_api_get(**kwargs)
        except ApiException as e:
            self.logger.error("Status {0}, Reason: {1} {2}".format(
                e.status, e.reason, e.body))
            return e.status
        else:
            return wko.get('ResourceList')

    def get_wos_with_new_status(self, min_date):
        """
        Get a list of Assetic work orders that have status date greater than
        supplied date, or null status date where last_modified greater than
        supplied date
        Uses OData as status date is only available in OData search and not the API
        :param min_date: the date to filter by
        :returns: list of work order ids or error number (non zero)
        """

        fields = "Id,WOStatusDateTime"
        fields_no_status = "Id,WOLastModified"
        top = 10000
        skip = 0
        # search require datetime with offset. Might be a bit awkward for the
        # couple of hours around daylight savings changeover
        date_filter = self._get_utc_string_with_offset(min_date)
        if date_filter is None:
            return 1
        qfilter = "WOStatusDateTime ge {0}".format(date_filter)
        orderby = "WOStatusDateTime desc"
        qfilter_no_status = "WOLastModified ge {0}".format(date_filter)
        orderby_no_status = "WOLastModified desc"
        try:
            wos = self.odata.get_odata_data("workorder", fields, qfilter,
                                            top, skip, orderby)
        except ApiException as e:
            self.logger.error("Status {0}, Reason: {1} {2}".format(
                e.status, e.reason, e.body))
            return e.status
        # now get wos with no status date - could be new wko
        try:
            wos_no_status = self.odata.get_odata_data("workorder"
                                                      , fields_no_status
                                                      , qfilter_no_status
                                                      , top, skip
                                                      , orderby_no_status)
        except ApiException as e:
            self.logger.error("Status {0}, Reason: {1} {2}".format(
                e.status, e.reason, e.body))
            return e.status
        # The search currently works at the 'day' level, so time is ignored
        # will remove times earlier than requested time
        # and convert the json into a list with just wo ID
        wo_status = [x["Id"] for x in wos
                     if self._get_datetime_from_utc_string(
                x["WOStatusDateTime"]) >= min_date]
        wo_no_status = [x["Id"] for x in wos_no_status
                        if self._get_datetime_from_utc_string(
                x["WOLastModified"]) >= min_date]
        return wo_status + wo_no_status

    def set_last_integration_datetime(self, module, lastdate):
        """
        Record the datetime of the last integration to act as starting point
        for next integration
        Write date in a text file in %APPDATA%/Assetic
        :param module: 'workorder' or "workrequest"
        :param lastdate: the datetime to record
        :return 0=success, else error
        """
        appdata = os.environ.get("APPDATA")
        if module == "workorder":
            file = os.path.join(appdata, "Assetic", "crm_wo_last_process_date.txt")
        else:
            file = os.path.join(appdata, "Assetic", "crm_wr_last_process_date.txt")
        try:
            with open(file, "w+") as f:
                f.write(lastdate.isoformat())
        except Exception as e:
            msg = "Unable to write datetime file {0} with error: {1}".format(
                file, str(e))
            self.logger.error(msg)
            return 1
        else:
            return 0

    def set_last_integration_datetime_via_doc_link(self, module, lastdate):
        """
        Record the datetime of the last integration to act as starting point
        for next integration
        Write date in a text file in %APPDATA%/Assetic
        :param module: 'workorder' or "workrequest"
        :param lastdate: the datetime to record
        :return 0=success, else error
        """
        doc_id = None
        if module == "workorder":
            label = "crm_wo_last_process_date for crm integration"
            doc_id = self._wo_last_date_doc_id
        elif module == "workrequest":
            label = "crm_wr_last_process_date for crm integration"
            doc_id = self._wr_last_date_doc_id
        else:
            self.logger.warning("Unsupported module {0} for setting "
                              "integration date. Date cannot be recorded")
            return 1

        # Document categorisation - initialise document properties object
        # and populate
        document = Assetic3IntegrationRepresentationsDocumentRepresentation()
        docurl = "{0}/Maintenance/Operational/" \
                 "".format(self.api_client.configuration.host)
        #document.document_group = doc_group
        #document.document_category = doc_category
        #document.document_sub_category = doc_subcategory
        document.document_link = docurl
        document.external_id = lastdate.isoformat()
        document.label = label
        document.id = doc_id

        if not doc_id:
            # Perform upload of new doc
            try:
                doc = self.docapi.document_post(document)
            except ApiException as e:
                self.logger.error("Status {0}, Reason: {1} {2}".format(
                    e.status, e.reason, e.body))
                return 1
        else:
            # Perform update of existing doc
            try:
                doc = self.docapi.document_put(document.id, document)
            except ApiException as e:
                self.logger.error("Status {0}, Reason: {1} {2}".format(
                    e.status, e.reason, e.body))
                return 1
        return 0

    def get_last_integration_datetime(self, module, seed_date_if_null=None):
        """
        Record the datetime of the last integration to act as starting point
        for next integration
        Read date from a text file in %APPDATA%/Assetic. If not found then
        use seed date if provided, else current date less 1 week.
        :param module: workorder or workrequest
        :param seed_date_if_null: optional datetime to seed the process if no
        date file is found
        :return: date
        """
        appdata = os.environ.get("APPDATA")
        if module == "workorder":
            file = os.path.join(appdata, "Assetic", "crm_wo_last_process_date.txt")
        else:
            file = os.path.join(appdata, "Assetic", "crm_wr_last_process_date.txt")
        if seed_date_if_null is not None and \
                isinstance(seed_date_if_null, datetime.datetime) == False:
            self.logger.warning("Seed date is not a datetime, will use default")
            seed_date_if_null = None
        if seed_date_if_null is None:
            seed_date_if_null = datetime.datetime.now() - datetime.timedelta(
                days=7)
        return_date = seed_date_if_null
        if os.path.isfile(file):
            try:
                with open(file) as f:
                    read_data = f.read()
            except Exception as e:
                msg = "Unable to read datetime file {0} with error: {1}\n" \
                      "Will use date {2} instead".format(
                    file, str(e), str(return_date))
                self.logger.warning(msg)
                return return_date
            try:
                return_date = dateutil.parser.parse(read_data)
            except Exception as e:
                msg = "Unable to correctly read datetime from file {0}, " \
                      "value is {1}.  Using default of {2} instead" \
                      "\nError is: {3}".format(
                    file, read_data, str(seed_date_if_null), str(e))
                self.logger.warning(msg)
                return_date = seed_date_if_null
        return return_date

    def get_last_integration_datetime_from_doc_link(self, module,
                                                    seed_date_if_null=None):
        """
        Record the datetime of the last integration to act as starting point
        for next integration
        Read date from a document link record in Assetic. If not found then
        use seed date if provided, else current date less 1 week.
        :param module: workorder or workrequest
        :param seed_date_if_null: optional datetime to seed the process if no
        date file is found
        :return: date
        """
        if seed_date_if_null is not None and \
                isinstance(seed_date_if_null, datetime.datetime) == False:
            self.logger.warning("Seed date is not a datetime, will use default")
            seed_date_if_null = None
        if seed_date_if_null is None:
            seed_date_if_null = datetime.datetime.now() - datetime.timedelta(
                days=7)
        return_date = seed_date_if_null
        # set search criteria
        if module == "workorder":
            label = "crm_wo_last_process_date for crm integration"
        elif module == "workrequest":
            label = "crm_wr_last_process_date for crm integration"
        else:
            self.logger.warning("Unsupported module {0} for getting "
                              "integration date. Will use default")
            return return_date

        search_filter = "label~eq~'{0}'".format(label)
        kw = {"request_params_page": 1,
              "request_params_page_size": 1,
              "request_params_filters": search_filter}

        # Perform get
        try:
            docs = self.docapi.document_get(**kw)
        except ApiException as e:
            self.logger.error("Status {0}, Reason: {1} {2}".format(
                e.status, e.reason, e.body))
            return return_date
        if len(docs["ResourceList"]) > 0 and \
                docs["ResourceList"][0]["ExternalId"] != "":
            if module == "workorder":
                self._wo_last_date_doc_id = docs["ResourceList"][0]["Id"]
            elif module == "workrequest":
                self._wr_last_date_doc_id = docs["ResourceList"][0]["Id"]
            return_date = docs["ResourceList"][0]["ExternalId"]
            # convert the string to a date object
            try:
                return_date = dateutil.parser.parse(return_date)
            except Exception as e:
                msg = "Unable to correctly read datetime {0}.  "\
                      "Using default of {1} instead" \
                      "\nError is: {2}".format(return_date,
                                               str(seed_date_if_null), str(e))
                self.logger.warning(msg)
                return_date = seed_date_if_null

        return return_date

    def _get_datetime_from_utc_string(self, utc_string):
        """
        Convert UTC string to local datetime
        Assumes server time is local time
        :param utc_string: the string to convert to local datetime
        :returns: datetime, or None if error
        """
        if utc_string is None:
            return None
        if "+" in utc_string:
            tz_offset_hr = int(utc_string.split("+")[1].split(":")[0])
            tz_offset_min = int(utc_string.split("+")[1].split(":")[1])
            try:
                dt = dateutil.parser.parse(utc_string.split("+")[0])
                dt = dt + datetime.timedelta(hours=tz_offset_hr,
                                             minutes=tz_offset_min)
            except Exception as e:
                self.logger.error(
                    "Error converting datetime {0}".format(str(e)))
                return None
        else:
            try:
                dt = dateutil.parser.parse(utc_string)
            except Exception as e:
                self.logger.error(
                    "Error converting datetime {0}".format(str(e)))
                return None
        return dt

    def _get_utc_string_with_offset(self, dt):
        """
        Convert local datetime to str for use by odata search
        Assumes server time is local time
        :param dt: the datetime to convert
        :returns: datetime string including ofset from UTC, or None if error
        """
        if not isinstance(dt, datetime.datetime):
            self.logger.error("Must provide a datetime object for date conversion to UTC string")
            return 1
        # Get local time offset.  If daylight savings then will get alt
        tz_offset = time.timezone
        if time.localtime().tm_isdst != 0:
            tz_offset = time.altzone

        # Get UTC by applying offset
        dt = dt + datetime.timedelta(seconds=tz_offset)

        # Now build offset string
        offset = str(tz_offset / 60 / 60 * -1).split(".")
        if len(offset) > 1 and offset[1] != '0':
            # offset includes minutes
            offset[1] = str(int(offset[1]) * 6)
        else:
            offset[1] = "00"

        return dt.strftime("%Y-%m-%dT%H:%M:%S+{0}:{1}".format(
            offset[0], offset[1]))


class CRMPluginBase(object):
    """
    Base class for common CRM integration activities
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_crm_requests(self, integrated=False):
        """
        Get a list of CRMs that satisfy the criteria for an Assetic Work Request
        :param integrated: boolean. If true then only get those with an assetic
        guid that are still active, else only get those without an assetic guid
        :returns a list of wr_crm_dto objects
        """
        return []

    @abc.abstractmethod
    def update_crm_for_new_wr(self, wr_crm_obj, comment):
        """
        For the given Assetic work request update the crm
        :param wr_crm_obj: Work Request / CRM object
        :param comment: the comment to apply to the task
        :return: 0 = success, else error
        """
        return 0

    @abc.abstractmethod
    def add_task_note_to_crm(self, crm_id):
        """
        Add a comment to the CRM 'task' using crm_id as the reference
        """
        return 0

    @abc.abstractmethod
    def get_task_note_from_crm(self,note, crm_id):
        """
        Get the comments from the CRM 'task' using crm_id as the reference
        """
        return ""

    @abc.abstractmethod
    def add_file_note_to_crm(self,note,crm_id):
        """
        Add a comment to the CRM top level using crm_id as the reference
        """
        return 0

    @abc.abstractmethod
    def get_file_note_from_crm(self, crm_id):
        """
        Get the comments from the CRM top level using crm_id as the reference
        """
        return ""

    @abc.abstractmethod
    def update_crm_task_status(self,crm_obj, code, statusdate):
        """
        For the given CRM task identifier update task status
        using code and datetime (e.g. reject, close)
        :param crm_obj: The crm object
        :param code: determination code
        :param statusdate: the date the status change applies to
        :returns: 0 if success, else error
        """
        return 0

    @abc.abstractmethod
    def update_crm_master_status(self, crm_obj, code, statusdate):
        """
        For the given crm update request status (e.g. close, reject etc)
        using code and datetime.
        :param crm_obj: the crm object
        :param code: the close code
        :param statusdate: the datetime that the request is to be closed
        :returns: 0 if success, else error
        """
        return 0

    @abc.abstractmethod
    def get_resolution_code_for_subtask(self, wr_subtype, crm_obj):
        """
        Get the resolution codes for task and CRM based on the work request
        subtype and CRM Object
        remedy code/maintenance type?
        :param wr_subtype: the Assetic work request subtype entered by user
        :param crm_obj: the crm object
        :return resolution code object
        """
        return CrmAsseticResolutionCodes()


class WrCrmRepresentation(object):
    """
    A structure for document information to be passed between assetic
    and external enterprise content management system (ECMS)
    """

    def __init__(self, assetic_wr_representation=None, crm_representation=None
                 , crm_id=None):
        """"
        Initialise
        :param assetic_wr_representation: Assetic3IntegrationRepresentationsDocumentRepresentation
        :param crm_representation: a object unique to the particular crm
        :param: crm_id: unique reference id of the crm
        """
        self.fieldtypes = {
            "assetic_wr_representation":
                "Assetic3IntegrationRepresentationsDocumentRepresentation",
            "crm_representation": "str",
            "crm_id": "str"
        }

        self._assetic_wr_representation = assetic_wr_representation
        self._crm_representation = crm_representation
        self._crm_id = crm_id

        api_client = ApiClient()
        self.logger = api_client.configuration.packagelogger

    @property
    def assetic_wr_representation(self):
        return self._assetic_wr_representation

    @assetic_wr_representation.setter
    def assetic_wr_representation(self, assetic_wr_representation):
        ##check the type is correct
        if not isinstance(assetic_wr_representation,
                          Assetic3IntegrationRepresentationsWorkRequest):
            msg = "assetic_wr_representation is not the required type: '{0}'" \
                  "".format(
                "Assetic3IntegrationRepresentationsWorkRequest")
            self.logger.error(msg)
            self._assetic_wr_representation = None
        else:
            self._assetic_wr_representation = assetic_wr_representation

    @property
    def crm_representation(self):
        return self._crm_representation

    @crm_representation.setter
    def crm_representation(self, crm_representation):
        self._crm_representation = crm_representation

    @property
    def crm_id(self):
        return self._crm_id

    @crm_id.setter
    def crm_id(self, crm_id):
        self._crm_id = crm_id

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in six.iteritems(self.fieldtypes):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other


class CrmAsseticResolutionCodes(object):
    types = {
        "wr_subtype": "str",
        "wo_remedy_id": "str",
        "crm_resolution_code": "str",
        "crm_rejection_code": "str",
        "close_crm": "bool"
    }

    def __init__(self, wr_subtype=None, wo_remedy_id=None
                 , crm_resolution_code=None, crm_rejection_code=None
                 , close_crm=None):
        self._wr_subtype = None
        self._wo_remedy_id = None
        self._crm_resolution_code = None
        self._crm_rejection_code = None
        self._close_crm = None

        if wr_subtype is not None:
            self._wr_subtype = wr_subtype
        if wo_remedy_id is not None:
            self._wo_remedy_id = wo_remedy_id
        if crm_resolution_code is not None:
            self._crm_resolution_code = crm_resolution_code
        if crm_rejection_code is not None:
            self._crm_rejection_code = crm_rejection_code
        if close_crm is not None:
            self._close_crm = close_crm

    @property
    def wr_subtype(self):
        return self._wr_subtype

    @wr_subtype.setter
    def wr_subtype(self, wr_subtype):
        self._wr_subtype = wr_subtype

    @property
    def wo_remedy_id(self):
        return self._wo_remedy_id

    @wo_remedy_id.setter
    def wo_remedy_id(self, wo_remedy_id):
        self._wo_remedy_id = wo_remedy_id

    @property
    def crm_resolution_code(self):
        return self._crm_resolution_code

    @crm_resolution_code.setter
    def crm_resolution_code(self, crm_resolution_code):
        self._crm_resolution_code = crm_resolution_code

    @property
    def crm_rejection_code(self):
        return self._crm_rejection_code

    @crm_rejection_code.setter
    def crm_rejection_code(self, crm_rejection_code):
        self._crm_resolution_code = crm_rejection_code

    @property
    def close_crm(self):
        return self._close_crm

    @close_crm.setter
    def close_crm(self, close_crm):
        self._close_crm = close_crm

    def to_dict(self):
        "Returns the model properties as a dict"
        result = {}

        for attr, _ in six.iteritems(self.types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        "Returns the string representation of the model"
        return pformat(self.to_dict())

    def __repr__(self):
        "For `print` and `pprint`"
        return self.to_str()

    def __eq__(self, other):
        "Returns true if both objects are equal"
        if not isinstance(other, CrmAsseticResolutionCodes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        "Returns true if both objects are not equal"
        return not self == other

