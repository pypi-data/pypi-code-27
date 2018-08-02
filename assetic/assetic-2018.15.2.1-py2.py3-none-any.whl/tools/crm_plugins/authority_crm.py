# coding: utf-8
"""
    Create Assetic requests from Authority CRM and Update Authority CRM
"""

import pyodbc  # connect to Informix
import datetime
from contextlib import contextmanager
from pprint import pformat
from six import iteritems
import logging

from assetic import CrmAsseticResolutionCodes
from ..crm_tools import CRMPluginBase
from ..crm_tools import WrCrmRepresentation
from ..maintenance_tools import MaintenanceTools
from ...models.assetic3_integration_representations_work_request_spatial_location\
    import  Assetic3IntegrationRepresentationsWorkRequestSpatialLocation
from ...models.assetic3_integration_representations_work_request\
    import Assetic3IntegrationRepresentationsWorkRequest
from ...models.assetic3_integration_representations_work_request_physical_location\
    import Assetic3IntegrationRepresentationsWorkRequestPhysicalLocation
from ...models.assetic3_integration_representations_custom_address\
    import Assetic3IntegrationRepresentationsCustomAddress
from ...models.assetic3_integration_representations_requestor_representation\
    import Assetic3IntegrationRepresentationsRequestorRepresentation
from ...models.assetic3_integration_representations_requestor_type_representation\
    import Assetic3IntegrationRepresentationsRequestorTypeRepresentation
from ..crm_tools import CrmAsseticResolutionCodes

class AuthorityCRM(CRMPluginBase):
    def __init__(self, **kwargs):
        """
        initialise object
        :param **kwargs: requires  3 keywords:
        'db_connection_string' with the connection string defined
        'db_type' one of 'informix' or 'sqlserver'
        'crm_query_filter' sql to filter the list of CRM requests.  Use full
        table name and column name
        """
        logger = logging.getLogger(__name__)
        self.logger = logger
        self._db_crm_select_filter = ""
        if "db_connection_string" in kwargs:
            try:
                self._db_connection = pyodbc.connect(
                    kwargs["db_connection_string"])
            except pyodbc.Error as ex:
                self.logger.error(
                    "Error connecting to database:\r\n{0}".format(
                        ex))
                raise
        else:
            msg = "'db_connection_string' not defined when initiating " \
                  "Authority CRM plugin"
            self.logger.error(msg)
            raise AttributeError(msg)
        if "db_crm_select_filter" in kwargs:
            self._db_crm_select_filter = kwargs["db_crm_select_filter"]

        self.maintenance_tools = MaintenanceTools()

        self._crm_db_query = "assetic_crm"

        self._classification_codes = list()
        self._resolution_codes = list()

        self._doctype = 2
        self._mduref = "DD"
        self._typind = "T"
        self._audmnote_num_typ = "D"

        self._resolution_code_representation = AuthorityAsseticResolutionCodes

    @property
    def classification_codes(self):
        return self._classification_codes

    @classification_codes.setter
    def classification_codes(self, classification_codes):
        if isinstance(classification_codes, list):
            self._classification_codes = classification_codes
        else:
            self.logger.error("classification_codes should be a list")

    @property
    def resolution_code_representation(self):
        return self._resolution_code_representation

    @property
    def resolution_codes(self):
        return self._resolution_codes

    @resolution_codes.setter
    def resolution_codes(self, value):
        if isinstance(value, list):
            self._resolution_codes = value
        else:
            self.logger.error("resolution_codes should be a list")

    @property
    def db_connection(self):
        """
        Get the ODBC database connection to Authority database
        """
        return self._db_connection

    @property
    def crm_db_query(self):
        """
        Get the query used to get CRM's from Authority.
        """
        return self._crm_db_query

    @crm_db_query.setter
    def crm_db_query(self, crm_db_query):
        """
        Define the query used to get CRM's from Authority.  Must follow a strict
        column order and return specific fields however the field name is not
        used, just column order
        """
        self._crm_db_query = crm_db_query

    @property
    def doctype(self):
        """
        Authority document type used when creating a task note
        """
        return self._doctype

    @doctype.setter
    def doctype(self, doctype):
        self._doctype = doctype

    @property
    def mduref(self):
        """
        Authority mduref code used when creating a task note
        """
        return self._mduref

    @mduref.setter
    def mduref(self, mduref):
        self._mduref = mduref

    @property
    def typind(self):
        """
        Authority typind code used when creating a task note
        """
        return self._typind

    @typind.setter
    def typind(self, typind):
        self._typind = typind

    @property
    def audmnote_num_typ(self):
        """
        Authority numtype code used when creating a crm note
        """
        return self._audmnote_num_typ

    @audmnote_num_typ.setter
    def audmnote_num_typ(self, audmnote_num_typ):
        self._audmnote_num_typ = audmnote_num_typ

    def update_crm_for_new_wr(self, wr_crm_obj, comment):
        """
        For the given Assetic work request update the crm
        :param wr_crm_obj: Work Request / CRM object
        :param comment: the comment to add to task
        :return: 0 = success, else error
        """
        wr = wr_crm_obj.assetic_wr_representation
        authority_obj = wr_crm_obj.crm_representation
        # Now update authority with Assetic guid
        sql = "UPDATE aualdocs SET ext_ref=? WHERE fmt_acc=?;"
        params = (wr.id, wr_crm_obj.crm_id)
        chk = self.run_query(sql, params)
        if chk != 0:
            # there was an error so exit
            return chk
        else:
            # now add a task note to authority indicating request created
            self.add_task_note_to_crm(comment, wr_crm_obj.crm_id)
            # could also add comment at the request level?
            # self.add_filenote_to_authority(comment,
            #    wr_crm_obj.crm_id)
        return 0

    def get_resolution_code_for_subtask(self, wr_subtype, crm_obj):
        """
        Get the resolution codes for task and CRM based on the work request
        subtype and Authority workflow
        remedy code/maintenance type?
        :param wr_subtype: the work request subtype entered by user
        :param crm_obj: the crm object
        :return resolution code object
        """
        for row in self.resolution_codes:
            if row.wr_subtype == wr_subtype and \
                    row.crm_workflow == crm_obj.crm_workflow:
                return row
                break

        # no definition found so return default
        return AuthorityAsseticResolutionCodes(crm_resolution_code="COMP"
                                               , crm_rejection_code="CRCA"
                                               , close_crm=True)

    def get_crm_requests(self, integrated=False):
        """
        Use a view on the Authority database to get a list of CRMs that satify
        the criteria for an Assetic Work Request
        :param integrated: boolean. If true then only get those with an assetic
        guid that are still active, else only get those without an assetic guid
        :returns a list of authority_crm_dto objects
        """
        if integrated:
            # get CRMs where there is no date closed but there is an Assetic id
            sqlwhere = "and d.ext_ref is not null and task.clo_dte is null"
        else:
            # get CRMs where there is no Assetic id
            sqlwhere = "and d.ext_ref is null and task.clo_dte is null"

        sql = """
        select distinct d.fmt_acc, d.wrk_typ, d.dda_cd1, d.dda_cd2, d.doc_num
        ,d.rec_dte, p.str_nme as prop_st, p.sbr_nme as prop_suburb
        ,trim(trim(nvl(p.pcl_unt,'')) || trim(nvl(p.unt_alp,'')) || decode(nvl(p.pcl_unt,'NULL'),'NULL','',
        decode(nvl(p.hou_num,'NULL'),'NULL','','/')) || trim(nvl(p.hou_num,'')) || trim(nvl(p.hou_alp,'')) ||
        decode(nvl(p.hou_end,"NULL"),"NULL",'','-') || trim(nvl(p.hou_end,' ')) || trim(nvl(p.end_alp,'')) || ' ' ||
        trim(nvl(p.str_nme,' ')) || ' ' || trim(nvl(p.str_typ,' ')) || ' ' || trim(nvl(p.sbr_nme,''))) as prop_addr
        ,task.key_num, task.rea_cde, task.det_cde, task.clo_dte
        ,trim(nvl(cn.nam_gv1,'')) as cust_firstname
        ,trim(nvl(cn.nam_fam,'')) as cust_famname
        ,cn.bus_phn as cust_busphn
        ,cn.hme_ph1 as cust_home_phn
        ,cn.mob_phn as cust_mob_phn
        ,trim(trim(nvl(cn.res_ad1,' ')) || ' ' || trim(nvl(cn.res_ad2,' ')) || ' ' || trim(nvl(cn.res_ad3,' ')) || ' ' || trim(nvl(cn.res_ad4,' ')) || ' ' || trim(nvl(cn.res_ad5,' '))) as cust_addr
        ,task.due_dte
        ,gps.gps_lat, gps.gps_lon
        ,d.cre_dte_tme, d.doc_pre, d.ext_ref, d.mod_opr
        ,trim(nvl(l.des_acc,'')) as node_num, trim(nvl(l.acc_dsc,'')) as node_desc
        ,emp.emp_num
		,trim(nvl(nar_ta.nam_gv1,'')) || ' ' || trim(nvl(nar_ta.nam_fam,'')) as actioning_officer
		,l2.alp_cd3 as contact_method
        from aualdocs d
        ,aualparm pm 
        ,outer auallnks l
        ,outer(auallnks l2, outer aunrmast cn, outer aupymast emp)
        ,outer(auprlink pl, outer auprstad p)
		,outer aunrmast nar_ta
        ,aualtask task
        ,outer aualgpsp gps
        ,outer(auprlink pr, outer auprparc pc)
        where
        d.doc_typ = pm.sml_no6
        and d.fmt_acc = task.mdu_fmt
        and nar_ta.nar_num = task.act_nar
        and d.fmt_acc = gps.mdu_acc
        and d.fmt_acc = pl.mdu_fmt
        and pl.pcl_num = p.pcl_num
        and d.fmt_acc = pr.mdu_fmt
        and pr.pcl_num  = pc.pcl_num
        and emp.nar_num = l2.des_num
        and d.fmt_acc = l.src_acc and l.des_mdu = 'AM'
        and d.fmt_acc = l2.src_acc and l2.des_mdu = 'NR'
        and l2.des_num = cn.nar_num
        and d.doc_yer >2017
        and pl.mdu_acc > 0
        and p.seq_num = 0
        {0}{1}
        """.format(self._db_crm_select_filter,sqlwhere)
        result = self.run_query(sql, return_many=True)
        if isinstance(result, int):
            # there was an error so exit
            return result

        # populate dto object with db results
        authority_crms = list()

        for row in result:
            # create new dto object to record raw data
            authority_obj = AuthorityCrmDTO()
            authority_obj.formatted_account = row[0]
            authority_obj.workflow = row[1]
            authority_obj.category1 = row[2]
            authority_obj.category2 = row[3]
            authority_obj.crm_number = row[4]
            authority_obj.received = row[5]
            authority_obj.prop_st = row[6]
            authority_obj.prop_sub = row[7]
            authority_obj.propertyref = row[8]
            authority_obj.task_key = row[9]
            authority_obj.task_cde = row[10]
            authority_obj.task_det = row[11]
            authority_obj.det_date = row[12]
            authority_obj.firstname = row[13]
            authority_obj.familyname = row[14]
            authority_obj.business_phone = row[15]
            authority_obj.home_phone = row[16]
            authority_obj.mobile_phone = row[17]
            authority_obj.address_comment = row[18]
            authority_obj.due_date = row[19]
            authority_obj.latitude = row[20]
            authority_obj.longitude = row[21]
            authority_obj.created = row[22]
            authority_obj.precis = row[23]
            authority_obj.assetic_wr_guid = row[24]
            authority_obj.mod_opr = row[25]
            authority_obj.crm_assetid = row[26]
            authority_obj.crm_assetdesc = row[27]
            authority_obj.assigned_to = row[29]
            authority_obj.contact_method = row[30]

            #create object to return wr and crm info
            wr_crm_obj = WrCrmRepresentation()
            wr = Assetic3IntegrationRepresentationsWorkRequest()
            # Get the note if new request and then build assetic wr object
            if integrated:
                wr.id = authority_obj.assetic_wr_guid
            else:
                authority_obj.description = self.get_file_note_from_crm(
                    authority_obj.formatted_account)
                wr = self._prepare_new_wr_object(authority_obj)
            wr_crm_obj.assetic_wr_representation = wr

            wr_crm_obj.crm_representation = authority_obj
            wr_crm_obj.crm_id = authority_obj.formatted_account
            # append dto to list
            authority_crms.append(wr_crm_obj)
        return authority_crms

    def _prepare_new_wr_object(self, authority_obj):
        """
        Take the raw authority data for a new Assetic WR and format for Assetic
        WR creation
        :param authority_obj: the raw Authority CRM data
        :return:
        """
        # create work request object
        wr = Assetic3IntegrationRepresentationsWorkRequest()
        # create address object
        wraddr = Assetic3IntegrationRepresentationsCustomAddress()
        # create spatial location object
        wrsl = Assetic3IntegrationRepresentationsWorkRequestSpatialLocation()

        # get the Assetic asset if there is a crm asset number
        if authority_obj.crm_assetid is not None:
            assetic_asset = self.get_asset_by_extid(
                authority_obj.crm_assetid)
            if assetic_asset is not None:
                # authority_obj.asset_id = assetic_asset["AssetId"]
                authority_obj.asset_guid = assetic_asset["Id"]

        if authority_obj.asset_guid is not None and \
                authority_obj.asset_guid != "":
            wr.asset_id = authority_obj.asset_id
            # we have an asset id, so use it's location and address
            wraddr, wrsl = self.maintenance_tools.get_location_by_assetguid(
                authority_obj.asset_guid)

        if authority_obj.latitude is not None and \
                authority_obj.longitude is not None:
            # location provided by authority
            wrsl.point_string = "POINT ({0} {1})".format(authority_obj.latitude,
                                                         authority_obj.longitude
                                                         )

        if wraddr.street_address is None or wraddr.street_address == "":
            # No address - use default values for address & spatial location
            wraddr.country = 'Australia'
        if wrsl.point_string is None:
            # no spatial - use default value
            wrsl.point_string = "POINT (145.7102081 -37.1905981)"

        # location is deprecated, but still required! Use a dummy value
        wr.location = "location"

        # Assign spatial location to work request
        wr.work_request_spatial_location = wrsl

        # create physical location object and assign address and then assign to
        # request object
        wrfl = Assetic3IntegrationRepresentationsWorkRequestPhysicalLocation()
        wrfl.address = wraddr
        wr.work_request_physical_location = wrfl

        # create object for person that lodged the request
        wrreq = Assetic3IntegrationRepresentationsRequestorRepresentation()
        wrreq.first_name = authority_obj.firstname
        wrreq.surname = authority_obj.familyname
        wrreq.mobile = authority_obj.mobile_phone
        wrreq.phone = authority_obj.home_phone
        wrreq.address_comment = authority_obj.address_comment
        reqtype = Assetic3IntegrationRepresentationsRequestorTypeRepresentation()
        reqtype.id = 4  # indicates 'customer'
        wrreq.types = [reqtype]
        # assign requestor to work request
        wr.requestor = wrreq

        wr.external_identifier = authority_obj.formatted_account
        wr.work_request_source_id = 3  # 3='External CRM'
        # contact customer?
        if authority_obj.contact_method == "NR":
            # no need to respond to customer, but may need to contact
            wr.feedback_required = 0
        else:
            wr.feedback_required = 1
        # contact method
        if authority_obj.contact_method.upper() == "T":
            # Telephone
            wr.feedback_method_id = 1
        elif authority_obj.contact_method.upper() == "F":
            # Fax - unsupported- use phone
            wr.feedback_method_id = 1
        elif authority_obj.contact_method.upper() == "L":
            # Letter
            wr.feedback_method_id = 5
        elif authority_obj.contact_method.upper() == "M":
            # Mobile - use text
            wr.feedback_method_id = 2
        elif authority_obj.contact_method.upper() == "S":
            # Social - email
            wr.feedback_method_id = 3
        else:
            # default to phone
            wr.feedback_method_id = 1
        wr.work_request_priority_id = 1  # default as 1
        wr.description = "Attention: {0}. {1}".format(
            authority_obj.assigned_to, authority_obj.precis.strip())[0:100]
        wr.supporting_information = authority_obj.description
        if authority_obj.due_date is not None:
            wr.resolution_due_date = authority_obj.due_date
            wr.acknowledge_due_date = authority_obj.due_date

        return wr

    def add_task_note_to_crm(self, comment, crm_obj):
        """
        Add a note to the task. Need to split in 70 char segments
        and append to prior notes using sequence number
        The task is the Assetic specific action (step) in the request document
        workflow.
        :param comment: the comment to apply
        :param crm_obj: thw work request/CRM object
        :returns: 0 unless error
        """
        # get some values from wr_crm object
        # the authority request id
        fmt_acc = crm_obj.formatted_account
        # the authority doc number
        doc_num = crm_obj.crm_number
        # mod_opr: the authority operator
        mod_opr = crm_obj.mod_opr

        # some constants
        doctype = self.doctype
        mduref = self.mduref
        typind = self.typind
        doc_prt = 1
        seq_num = 1
        now = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        sub_seq = self._get_last_task_note_sequence(doc_num)

        # calc some vals
        docyer = datetime.datetime.today().year

        sql = "insert into aualtnot (doc_typ,mdu_fmt,doc_num,com_txt," \
              "mdu_ref,typ_ind,doc_yer,doc_prt,sub_seq,cre_dte_tme,mod_dte_tme" \
              ",mod_opr,seq_num) values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
        # need to break comment into 70 char chunks
        for chunk in self.split_comment(comment, 70):
            sub_seq = sub_seq + 1
            params = [doctype, fmt_acc, doc_num, chunk, mduref, typind,
                      docyer, doc_prt, sub_seq, now, now, mod_opr, seq_num]
            chk = self.run_query(sql, params)
            if chk != 0:
                # there was an error so exit
                return chk
        return 0

    def _get_last_task_note_sequence(self, doc_num):
        """
        Get last sequence number for task note
        :param doc_num: the authority doc number
        :returns: integer sequence number
        """
        sql = "select max(sub_seq) from aualtnot where doc_num=?"
        param = [doc_num]
        row = self.run_query(sql, param, return_one=True)
        if isinstance(row, int):
            # there was an error, should be of type pyodbc.Row
            return row
        if row and row[0] != None:
            return row[0]
        else:
            # return zero indicating this is the first note for this doc.
            return 0

    def get_task_note_from_crm(self, mdu_fmt):
        """
        Get task note for given doc_num
        :param mdu_fmt: the authority formatted account number
        :returns: the comment for the task
        """
        sql = "select com_txt from aualtnot where mdu_fmt=? " \
              "order by sub_seq asc"
        param = [mdu_fmt]

        result = self.run_query(sql, param, return_many=True)
        if isinstance(result, int):
            # there was an error so exit
            return result
        if result is None:
            return ""
        else:
            # Join the result rows, put in a space if the stripped length of a
            # row is not 70 because it implies the text does not continue in the
            # new row
            return "".join([i[0] if len(i[0].strip()) == 70
                            else "{0} ".format(i[0].strip()) for i in result])

    def add_file_note_to_crm(self, comment, fmt_acc):
        """
        Add a note to the request.  Need to split in 70 char segments
        and append to prior notes using sequence number
        This note is at the 'parent' level
        :param comment: the comment to apply
        :param fmt_acc: the authority request id
        :returns: 0 unless error
        """

        ##some hardcodes
        num_typ = self.audmnote_num_typ
        seq_num = self.get_last_file_note_sequence(fmt_acc)

        sql = "insert into audmnote (num_typ,fil_num,seq_num,fil_not) values " \
              "(?,?,?,?)"
        # need to break comment into 70 char chunks
        for chunk in self.split_comment(comment, 70):
            seq_num = seq_num + 1
            params = [num_typ, fmt_acc, seq_num, chunk]
            chk = self.run_query(sql, params)
            if chk != 0:
                # there was an error so exit
                return chk
        return 0

    def get_file_note_from_crm(self, fmt_acc):
        """
        Get file/document note for given doc_num
        :param fmt_acc: the authority request id
        :returns: the comment for the request
        """
        # some hardcodes
        num_typ = self.audmnote_num_typ

        sql = "select fil_not from audmnote where fil_num=? and num_typ=?" \
              " order by seq_num asc"
        param = [fmt_acc, num_typ]

        result = self.run_query(sql, param, return_many=True)
        if isinstance(result, int):
            # there was an error so exit
            return result
        if result is None:
            return ""
        else:
            # Join the result rows, put in a space if the stripped length of a
            # row is not 70 becuase it implies the text does not continue in the
            # new row
            return "".join([i[0] if len(i[0].strip()) == 70
                            else "{0} ".format(i[0].strip()) for i in result])

    def get_last_file_note_sequence(self, fmt_acc):
        """
        Get last sequence number for request notes table
        :param fmt_acc: the authority doc number
        :returns: imteger sequence number
        """
        # fil_num is the fmt_acc from aualdocs
        sql = "select max(seq_num) from audmnote where fil_num=?"
        param = [fmt_acc]
        row = self.run_query(sql, param, return_one=True)
        if isinstance(row, int):
            # there was an error, should be of type pyodbc.Row
            return row
        if row and row[0] is not None:
            return row[0]
        else:
            # return zero indicating this is the first note for this doc.
            return 0

    def update_crm_task_status(self, crm_obj, code, statusdate):
        """
        For the given Authority task identifier update Authority task status
        using code and datetime
        :param crm_obj: The crm object
        :param code: determination code
        :param statusdate: the date the status change applies to
        :returns: 0 if success, else error
        """
        fmt_acc = crm_obj.formatted_account # the ID of the Authority Request
        key_num = crm_obj.task_key  # the ID of the task
        date = '{:%Y-%m-%d %H:%M:%S}'.format(statusdate)
        sql = "update aualtask set clo_dte=?,det_cde=?,mod_dte_tme=current " \
              "where key_num=? and mdu_fmt=?"
        param = [date, code, key_num, fmt_acc]
        chk = self.run_query(sql, param)
        if chk != 0:
            # there was an error so exit
            return chk
        return 0

    def update_crm_master_status(self, crm_obj, code, statusdate):
        """
        For the given Authority crm identifier update Authority request status
        using code and datetime.
        :param crm_obj: the crm object
        :param code: the close code
        :param statusdate: the datetime that the request is to be closed
        :returns: 0 if success, else error
        """
        fmt_acc =  crm_obj.formatted_account # the ID of the Authority Request
        date = '{:%Y-%m-%d %H:%M:%S}'.format(statusdate)
        sql = "update aualdocs set det_dte=?,det_cde=?,mod_dte_tme=current where fmt_acc=?"
        param = [date, code, fmt_acc]
        chk = self.run_query(sql, param)
        if chk != 0:
            ##there was an error so exit
            return chk
        return 0

    def split_comment(self, comment, size):
        """
        Split a comment into chunks
        :param comment: the comment to split
        :param size: the character size to split by
        :returns: iterable list of split comments
        """
        for start in range(0, len(comment), size):
            yield comment[start:start + size]

    def run_query(self, sql, params=None, return_one=False, return_many=False):
        """
        Run the provided query and return results
        :params sql: the SQL to execute, may be parameterised query
        :params params: the parameters for the sql as a list
        :params return_one: return first result (use if single record expected)
        boolean - default = False
        :params return_many: return all results. Boolean - default=False
        :returns: 0 if both return_one and return_many are False, else one or
        many records. If both return_one and return_many are True return_one
        takes precedence. If error then non-zero return.
        """
        cursor = self.db_connection.cursor()
        result = 0

        self.logger.debug("{0}; params {1}".format(sql, params))
        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            if return_one:
                result = cursor.fetchone()
            elif return_many:
                result = cursor.fetchall()
        except pyodbc.DatabaseError as err:
            self.logger.error("Error for SQL {0}\r\n{1}".format(sql, err))
            result = 1
        except Exception as ex:
            self.logger.error("Error for SQL {0}\r\n{1}".format(sql, ex))
            result = 1
        finally:
            try:
                self.db_connection.commit()
            except Exception as ex:
                self.logger.error("Error commiting SQL {0}\r\n{1}".format(
                    sql, ex))
                result = 1
            try:
                cursor.close()
            except Exception as ex:
                self.logger.error("Error closing cursor for SQL {0}\r\n{1}".
                                  format(sql, ex))
                result = 1
        return result

    @contextmanager
    def open_db_connection(self, db_connection_string, commit=False):
        """
        Use contextmanager to manage connections so we cleanup connection
        as we go to avoid database locking issues on exception
        Not in use, connection not closing fast enough in Informix

        """
        connection = pyodbc.connect(self.db_connection_string)
        cursor = connection.cursor()
        try:
            yield cursor
        except pyodbc.DatabaseError as err:
            raise err
        except Exception as ex:
            self.logger.error(ex)
        finally:
            if commit:
                try:
                    connection.commit()
                except:
                    pass
            try:
                cursor.close()
            except:
                pass
            try:
                connection.close()
            except:
                pass


class AuthorityAsseticClassificationCodes(object):
    types = {
        "wr_subcategory_id": "str",
        "crm_workflow": "str",
        "crm_category1": "str",
        "crm_category2": "str",
        "wr_risk": "str"
    }

    def __init__(self, wr_subcategory_id=None, crm_workflow=None, crm_category1=None, crm_category2=None, wr_risk=None):
        self._wr_subcategory_id = None
        self._crm_workflow = None
        self._crm_category1 = None
        self._crm_category2 = None
        self._wr_risk = None

        if wr_subcategory_id is not None:
            self._wr_subcategory_id = wr_subcategory_id
        if crm_workflow is not None:
            self._crm_workflow = crm_workflow
        if crm_category1 is not None:
            self._crm_category1 = crm_category1
        if crm_category2 is not None:
            self._crm_category2 = crm_category2
        if wr_risk is not None:
            self._wr_risk = wr_risk

    @property
    def wr_subcategory_id(self):
        return self._wr_subcategory_id

    @wr_subcategory_id.setter
    def wr_subcategory_id(self, wr_subcategory_id):
        self._wr_subcategory_id = wr_subcategory_id

    @property
    def crm_workflow(self):
        return self._crm_workflow

    @crm_workflow.setter
    def crm_workflow(self, crm_workflow):
        self._crm_workflow = crm_workflow

    @property
    def crm_category1(self):
        return self._crm_category1

    @crm_category1.setter
    def crm_category1(self, crm_category1):
        self._crm_category1 = crm_category1

    @property
    def crm_category2(self):
        return self._crm_category2

    @crm_category2.setter
    def crm_category2(self, crm_category2):
        self._crm_category2 = crm_category2

    @property
    def wr_risk(self):
        return self._wr_risk

    @wr_risk.setter
    def wr_risk(self, wr_risk):
        self._wr_risk = wr_risk

    def to_dict(self):
        "Returns the model properties as a dict"
        result = {}

        for attr, _ in iteritems(self.types):
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
        if not isinstance(other, AuthorityAsseticClassificationCodes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        "Returns true if both objects are not equal"
        return not self == other


class AuthorityAsseticResolutionCodes(CrmAsseticResolutionCodes):
    types = {
        "wr_subtype": "str",
        "wo_remedy_id": "str",
        "crm_workflow": "str",
        "crm_category1": "str",
        "crm_category2": "str",
        "crm_resolution_code": "str",
        "crm_rejection_code": "str",
        "close_crm": "bool"
    }

    def __init__(self, wr_subtype=None, wo_remedy_id=None, crm_workflow=None, crm_category1=None, crm_category2=None,
                 crm_resolution_code=None, crm_rejection_code=None, close_crm=None):
        self._wr_subtype = None
        self._wo_remedy_id = None
        self._crm_workflow = None
        self._crm_category1 = None
        self._crm_category2 = None
        self._crm_resolution_code = None
        self._crm_rejection_code = None
        self._close_crm = None

        if wr_subtype is not None:
            self._wr_subtype = wr_subtype
        if wo_remedy_id is not None:
            self._wo_remedy_id = wo_remedy_id
        if crm_workflow is not None:
            self._crm_workflow = crm_workflow
        if crm_category1 is not None:
            self._crm_category1 = crm_category1
        if crm_category2 is not None:
            self._crm_category2 = crm_category2
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
    def crm_workflow(self):
        return self._crm_workflow

    @crm_workflow.setter
    def crm_workflow(self, crm_workflow):
        self._crm_workflow = crm_workflow

    @property
    def crm_category1(self):
        return self._crm_category1

    @crm_category1.setter
    def crm_category1(self, crm_category1):
        self._crm_category1 = crm_category1

    @property
    def crm_category2(self):
        return self._crm_category2

    @crm_category2.setter
    def crm_category2(self, crm_category2):
        self._crm_category2 = crm_category2

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

        for attr, _ in iteritems(self.types):
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
        if not isinstance(other, AuthorityAsseticResolutionCodes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        "Returns true if both objects are not equal"
        return not self == other


class AuthorityCrmDTO(object):
    types = {
        "formatted_account": "str",
        "workflow": "str",
        "category1": "str",
        "category2": "str",
        "crm_number": "str",
        "received": "str",
        "prop_st": "str",
        "prop_sub": "str",
        "propertyref": "str",
        "road": "str",
        "road_type": "str",
        "road_sub": "str",
        "task_key": "str",
        "task_cde": "str",
        "task_det": "str",
        "det_date": "str",
        "firstname": "str",
        "familyname": "str",
        "business_phone": "str",
        "home_phone": "str",
        "mobile_phone": "str",
        "address_comment": "str",
        "description": "str",
        "due_date": "str",
        "latitude": "str",
        "longitude": "str",
        "created": "str",
        "precis": "str",
        "asseticguid": "str",
        "asset_guid": "str",
        "asset_id": "str",
        "mod_opr": "str",
        "crm_assetid": "str",
        "crm_assetdesc": "str",
        "assigned_to": "str",
        "contact_method": "str"
    }

    def __init__(self, formatted_account=None, workflow=None, category1=None, category2=None, crm_number=None,
                 received=None, prop_st=None, prop_sub=None, propertyref=None, road=None, road_type=None, road_sub=None,
                 task_key=None, task_cde=None, task_det=None, det_date=None, firstname=None, familyname=None,
                 business_phone=None, home_phone=None, mobile_phone=None, description=None, due_date=None,
                 latitude=None, longitude=None, created=None, precis=None, asseticguid=None, asset_guid=None,
                 asset_id=None, mod_opr=None, address_comment=None, crm_assetid=None, crm_assetdesc=None,
                 assigned_to=None, contact_method=None):

        self._formatted_account = None
        self._workflow = None
        self._category1 = None
        self._category2 = None
        self._crm_number = None
        self._received = None
        self._prop_st = None
        self._prop_sub = None
        self._propertyref = None
        self._road = None
        self._road_type = None
        self._road_sub = None
        self._task_key = None
        self._task_cde = None
        self._task_det = None
        self._det_date = None
        self._firstname = None
        self._familyname = None
        self._business_phone = None
        self._home_phone = None
        self._mobile_phone = None
        self._address_comment = None
        self._description = None
        self._due_date = None
        self._latitude = None
        self._longitude = None
        self._created = None
        self._precis = None
        self._asseticguid = None
        self._asset_guid = None
        self._asset_id = None
        self._mod_opr = None
        self._crm_assetid = None
        self._crm_assetdesc = None
        self._assigned_to = None
        self._contact_method = None

        if formatted_account is not None:
            self._formatted_account = formatted_account
        if workflow is not None:
            self._workflow = workflow
        if category1 is not None:
            self._category1 = category1
        if category2 is not None:
            self._category2 = category2
        if crm_number is not None:
            self._crm_number = crm_number
        if received is not None:
            self._received = received
        if prop_st is not None:
            self._prop_st = prop_st
        if prop_sub is not None:
            self._prop_sub = prop_sub
        if propertyref is not None:
            self._propertyref = propertyref
        if road is not None:
            self._road = road
        if road_type is not None:
            self._road_type = road_type
        if road_sub is not None:
            self._road_sub = road_sub
        if task_key is not None:
            self._task_key = task_key
        if task_cde is not None:
            self._task_cde = task_cde
        if task_det is not None:
            self._task_det = task_det
        if det_date is not None:
            self._det_date = det_date
        if firstname is not None:
            self._firstname = firstname
        if familyname is not None:
            self._familyname = familyname
        if business_phone is not None:
            self._business_phone = business_phone
        if home_phone is not None:
            self._home_phone = home_phone
        if address_comment is not None:
            self._address_comment = address_comment
        if mobile_phone is not None:
            self._mobile_phone = mobile_phone
        if description is not None:
            self._description = description
        if due_date is not None:
            self._due_date = due_date
        if latitude is not None:
            self._latitude = latitude
        if longitude is not None:
            self._longitude = longitude
        if created is not None:
            self._created = created
        if precis is not None:
            self._precis = precis
        if asseticguid is not None:
            self._asseticguid = asseticguid
        if asset_guid is not None:
            self._asset_guid = asset_guid
        if asset_id is not None:
            self._asset_id = asset_id
        if mod_opr is not None:
            self._mod_opr = mod_opr
        if crm_assetid is not None:
            self._crm_assetid = crm_assetid
        if crm_assetdesc is not None:
            self._crm_assetdesc = crm_assetdesc
        if assigned_to is not None:
            self._assigned_to = assigned_to
        if contact_method is not None:
            self._contact_method = contact_method

    @property
    def formatted_account(self):
        return self._formatted_account

    @formatted_account.setter
    def formatted_account(self, formatted_account):
        self._formatted_account = formatted_account

    @property
    def workflow(self):
        return self._workflow

    @workflow.setter
    def workflow(self, workflow):
        self._workflow = workflow

    @property
    def category1(self):
        return self._category1

    @category1.setter
    def category1(self, category1):
        self._category1 = category1

    @property
    def category2(self):
        return self._category2

    @category2.setter
    def category2(self, category2):
        self._category2 = category2

    @property
    def crm_number(self):
        return self._crm_number

    @crm_number.setter
    def crm_number(self, crm_number):
        self._crm_number = crm_number

    @property
    def received(self):
        return self._received

    @received.setter
    def received(self, received):
        self._received = received

    @property
    def prop_st(self):
        return self._prop_st

    @prop_st.setter
    def prop_st(self, prop_st):
        self._prop_st = prop_st

    @property
    def prop_sub(self):
        return self._prop_sub

    @prop_sub.setter
    def prop_sub(self, prop_sub):
        self._prop_sub = prop_sub

    @property
    def propertyref(self):
        return self._propertyref

    @propertyref.setter
    def propertyref(self, propertyref):
        self._propertyref = propertyref

    @property
    def road(self):
        return self._road

    @road.setter
    def road(self, road):
        self._road = road

    @property
    def road_type(self):
        return self._road_type

    @road_type.setter
    def road_type(self, road_type):
        self._road_type = road_type

    @property
    def road_sub(self):
        return self._road_sub

    @road_sub.setter
    def road_sub(self, road_sub):
        self._road_sub = road_sub

    @property
    def task_key(self):
        return self._task_key

    @task_key.setter
    def task_key(self, task_key):
        self._task_key = task_key

    @property
    def task_cde(self):
        return self._task_cde

    @task_cde.setter
    def task_cde(self, task_cde):
        self._task_cde = task_cde

    @property
    def task_det(self):
        return self._task_det

    @task_det.setter
    def task_det(self, task_det):
        self._task_det = task_det

    @property
    def det_date(self):
        return self._det_date

    @det_date.setter
    def det_date(self, det_date):
        self._det_date = det_date

    @property
    def firstname(self):
        return self._firstname

    @firstname.setter
    def firstname(self, firstname):
        self._firstname = firstname

    @property
    def familyname(self):
        return self._familyname

    @familyname.setter
    def familyname(self, familyname):
        self._familyname = familyname

    @property
    def business_phone(self):
        return self._business_phone

    @business_phone.setter
    def business_phone(self, business_phone):
        self._business_phone = business_phone

    @property
    def home_phone(self):
        return self._home_phone

    @home_phone.setter
    def home_phone(self, home_phone):
        self._home_phone = home_phone

    @property
    def mobile_phone(self):
        return self._mobile_phone

    @mobile_phone.setter
    def mobile_phone(self, mobile_phone):
        self._mobile_phone = mobile_phone

    @property
    def address_comment(self):
        return self._address_comment

    @address_comment.setter
    def address_comment(self, address_comment):
        self._address_comment = address_comment

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, due_date):
        self._due_date = due_date

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        self._latitude = latitude

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        self._longitude = longitude

    @property
    def created(self):
        return self._created

    @created.setter
    def created(self, created):
        self._created = created

    @property
    def precis(self):
        return self._precis

    @precis.setter
    def precis(self, precis):
        self._precis = precis

    @property
    def asseticguid(self):
        return self._asseticguid

    @asseticguid.setter
    def asseticguid(self, asseticguid):
        self._asseticguid = asseticguid

    @property
    def asset_guid(self):
        return self._asset_guid

    @asset_guid.setter
    def asset_guid(self, asset_guid):
        self._asset_guid = asset_guid

    @property
    def asset_id(self):
        return self._asset_id

    @asset_id.setter
    def asset_id(self, asset_id):
        self._asset_id = asset_id

    @property
    def mod_opr(self):
        return self._mod_opr

    @mod_opr.setter
    def mod_opr(self, mod_opr):
        self._mod_opr = mod_opr

    @property
    def crm_assetid(self):
        return self._crm_assetid

    @crm_assetid.setter
    def crm_assetid(self, crm_assetid):
        self._crm_assetid = crm_assetid

    @property
    def crm_assetdesc(self):
        return self._crm_assetdesc

    @crm_assetdesc.setter
    def crm_assetdesc(self, crm_assetdesc):
        self._crm_assetdesc = crm_assetdesc

    @property
    def assigned_to(self):
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, assigned_to):
        self._assigned_to = assigned_to

    @property
    def contact_method(self):
        return self._contact_method

    @contact_method.setter
    def contact_method(self, contact_method):
        self._contact_method = contact_method

    def to_dict(self):
        "Returns the model properties as a dict"
        result = {}

        for attr, _ in iteritems(self.types):
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
        if not isinstance(other, AuthorityCrmDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        "Returns true if both objects are not equal"
        return not self == other


class AuthorityCRMtest(CRMPluginBase):
    def __init__(self, **kwargs):
        """
        initialise object
        :param **kwargs: requires  3 keywords:
        'db_connection_string' with the connection string defined
        'db_type' one of 'informix' or 'sqlserver'
        'crm_query_filter' sql to filter the list of CRM requests.  Use full
        table name and column name
        """
        logger = logging.getLogger(__name__)
        self.logger = logger
        self._db_crm_select_filter = ""
        if "db_connection_string" in kwargs:
            self.logger.info("DB Connection: {0}".format(
                kwargs["db_connection_string"]))
        else:
            msg = "'db_connection_string' not defined when initiating " \
                  "Authority CRM plugin"
            self.logger.error(msg)
            raise AttributeError(msg)
        self._db_connection = ""
        if "db_crm_select_filter" in kwargs:
            self._db_crm_select_filter = kwargs["db_crm_select_filter"]

        self.maintenance_tools = MaintenanceTools()

        self._resolution_code_representation = AuthorityAsseticResolutionCodes
        self._crm_db_query = "assetic_crm"

        self._classification_codes = list()
        self._resolution_codes = list()

        self._doctype = 2
        self._mduref = "DD"
        self._typind = "T"
        self._audmnote_num_typ = "D"

    @property
    def classification_codes(self):
        return self._classification_codes

    @classification_codes.setter
    def classification_codes(self, classification_codes):
        if isinstance(classification_codes, list):
            self._classification_codes = classification_codes
        else:
            self.logger.error("classification_codes should be a list")

    @property
    def resolution_code_representation(self):
        return self._resolution_code_representation

    @property
    def resolution_codes(self):
        return self._resolution_codes

    @resolution_codes.setter
    def resolution_codes(self, value):
        if isinstance(value, list):
            self._resolution_codes = value
        else:
            self.logger.error("resolution_codes should be a list")

    @property
    def db_connection(self):
        """
        Get the ODBC database connection to Authority database
        """
        return self._db_connection

    @property
    def crm_db_query(self):
        """
        Get the query used to get CRM's from Authority.
        """
        return self._crm_db_query

    @crm_db_query.setter
    def crm_db_query(self, crm_db_query):
        """
        Define the query used to get CRM's from Authority.  Must follow a strict
        column order and return specific fields however the field name is not
        used, just column order
        """
        self._crm_db_query = crm_db_query

    @property
    def doctype(self):
        """
        Authority document type used when creating a task note
        """
        return self._doctype

    @doctype.setter
    def doctype(self, doctype):
        self._doctype = doctype

    @property
    def mduref(self):
        """
        Authority mduref code used when creating a task note
        """
        return self._mduref

    @mduref.setter
    def mduref(self, mduref):
        self._mduref = mduref

    @property
    def typind(self):
        """
        Authority typind code used when creating a task note
        """
        return self._typind

    @typind.setter
    def typind(self, typind):
        self._typind = typind

    @property
    def audmnote_num_typ(self):
        """
        Authority numtype code used when creating a crm note
        """
        return self._audmnote_num_typ

    @audmnote_num_typ.setter
    def audmnote_num_typ(self, audmnote_num_typ):
        self._audmnote_num_typ = audmnote_num_typ

    def get_crm_requests(self, integrated=False):
        """
        Use a query on the Authority database to get a list of CRMs that satisfy
        the criteria for an Assetic Work Request
        :param integrated: boolean. If true then only get those with an Assetic
        guid that are still active, else only get those without an Assetic guid
        :returns a list of authority_crm_dto objects
        """

        # return a dummy crm
        authority_crms = list()

        # create new dto object to record raw data
        authority_obj = AuthorityCrmDTO()
        authority_obj.formatted_account = "002.2018.01431333.001 "
        authority_obj.workflow = "BUIL"
        authority_obj.category1 = "MAJOR PROJ"
        authority_obj.category2 = "BUILDINGMA"
        authority_obj.crm_number = "1431333"
        authority_obj.received = "2018-07-20T14:07:37.845666"
        authority_obj.prop_st = None
        authority_obj.prop_sub = None
        authority_obj.propertyref = None
        authority_obj.task_key = None
        authority_obj.task_cde = None
        authority_obj.task_det = None
        authority_obj.det_date = None
        authority_obj.firstname = "Roger"
        authority_obj.familyname = "Federer"
        authority_obj.business_phone = "03 5634 5678"
        authority_obj.home_phone = None
        authority_obj.mobile_phone = "0417 456 670"
        authority_obj.address_comment = None
        authority_obj.due_date = "2018-07-22T14:07:37.845666"
        authority_obj.latitude = None
        authority_obj.longitude = None
        authority_obj.created = "2018-07-20T15:07:37.845666"
        authority_obj.precis = "TEST - Operations depot - External lock on the fire escape door"
        authority_obj.assetic_wr_guid = None
        authority_obj.mod_opr = 4406
        authority_obj.crm_assetid = "126330"
        authority_obj.crm_assetdesc = "Operations Depot"
        authority_obj.assigned_to = "12345"
        authority_obj.contact_method = "T"

        # create object to return wr and crm info
        wr_crm_obj = WrCrmRepresentation()
        wr = Assetic3IntegrationRepresentationsWorkRequest()
        # Get the note if new request and then build assetic wr object
        if integrated:
            wr.id = "a5a34605-606e-43b7-9c76-51dc290fbb6f"
        else:
            authority_obj.description = self.get_file_note_from_crm(
                authority_obj.formatted_account)
            wr = self._prepare_new_wr_object(authority_obj)
        wr_crm_obj.assetic_wr_representation = wr

        wr_crm_obj.crm_representation = authority_obj
        wr_crm_obj.crm_id = authority_obj.formatted_account
        # append dto to list
        authority_crms.append(wr_crm_obj)
        return authority_crms

    def update_crm_for_new_wr(self, wr_crm_obj, comment):
        """
        For the given Assetic work request update the crm
        :param wr_crm_obj: Work Request / CRM object
        :param comment: the comment to apply to the task
        :return: 0 = success, else error
        """
        self.logger.info("Update crm for new wr: {0} {1}".format(
            comment, wr_crm_obj))
        return 0

    def get_resolution_code_for_subtask(self, wr_subtype, crm_obj):
        """
        Get the resolution codes for task and CRM based on the work request
        subtype and Authority workflow
        remedy code/maintenance type?
        :param wr_subtype: the Assetic work request subtype entered by user
        :param crm_obj: the crm object
        :return resolution code object
        """
        self.logger.info("get_resolution_code_for_subtask: {0} {1}".format(
            wr_subtype, crm_obj))
        return 0

    def add_task_note_to_crm(self,note,crm_id):
        """
        Add a comment to the CRM 'task' using crm_id as the reference
        """
        self.logger.info("add_task_note_to_crm: {0} {1}".format(
            note, crm_id))
        return 0

    def get_task_note_from_crm(self,crm_id):
        """
        Get the comments from the CRM 'task' using crm_id as the reference
        """
        self.logger.info("get_task_note_from_crm: {0}".format(
            crm_id))
        return ""

    def add_file_note_to_crm(self,note,crm_id):
        """
        Add a comment to the CRM top level using crm_id as the reference
        """
        self.logger.info("add_file_note_to_crm: {0} {1}".format(
            note, crm_id))
        return 0

    def get_file_note_from_crm(self, crm_id):
        """
        Get the comments from the CRM top level using crm_id as the reference
        """
        self.logger.info("get_file_note_from_crm: {0}".format(crm_id))
        return ""

    def update_crm_task_status(self,crm_obj, code, statusdate):
        """
        For the given CRM task identifier update task status
        using code and datetime (e.g. reject, close)
        :param crm_obj: The crm object
        :param code: determination code
        :param statusdate: the date the status change applies to
        :returns: 0 if success, else error
        """
        self.logger.info("update_crm_task_status: {0} {1} {2}".format(
            crm_obj, code, statusdate))
        return 0

    def update_crm_master_status(self, crm_obj, code, statusdate):
        """
        For the given crm update request status (e.g. close, reject etc)
        using code and datetime.
        :param crm_obj: the crm object
        :param code: the close code
        :param statusdate: the datetime that the request is to be closed
        :returns: 0 if success, else error
        """
        self.logger.info("update_crm_master_status: {0} {1} {2}".format(
            crm_obj, code, statusdate))
        return 0

    def get_resolution_code_for_subtask(self, wr_subtype, crm_obj):
        """
        Get the resolution codes for task and CRM based on the work request
        subtype and Authority workflow
        remedy code/maintenance type?
        :param wr_subtype: the work request subtype entered by user
        :param crm_obj: the crm object
        :return resolution code object CRMAsseticResolutionCodes
        """
        self.logger.info("get_resolution_code_for_subtask: {0} {1}".format(
            wr_subtype, crm_obj))

        code = AuthorityAsseticResolutionCodes() # type: AuthorityAsseticResolutionCodes
        code.crm_rejection_code = "CRMA"
        code.crm_resolution_code = "COMP"
        code.close_crm = "TRUE"
        return code

    def _prepare_new_wr_object(self, authority_obj):
        """
        Take the raw authority data for a new Assetic WR and format for Assetic
        WR creation
        :param authority_obj: the raw Authority CRM data
        :return:
        """
        # create work request object
        wr = Assetic3IntegrationRepresentationsWorkRequest()
        # create address object
        wraddr = Assetic3IntegrationRepresentationsCustomAddress()
        # create spatial location object
        wrsl = Assetic3IntegrationRepresentationsWorkRequestSpatialLocation()

        # get the Assetic asset if there is a crm asset number
        # if authority_obj.crm_assetid is not None:
        #    assetic_asset = self.get_asset_by_extid(
        #        authority_obj.crm_assetid)
        #    if assetic_asset is not None:
        #        # authority_obj.asset_id = assetic_asset["AssetId"]
        #        authority_obj.asset_guid = assetic_asset["Id"]

        #if authority_obj.asset_guid is not None and \
        #        authority_obj.asset_guid != "":
        #    wr.asset_id = authority_obj.asset_id
        #    # we have an asset id, so use it's location and address
        #    wraddr, wrsl = self.maintenance_tools.get_location_by_assetguid(
        #        authority_obj.asset_guid)

        if authority_obj.latitude is not None and \
                authority_obj.longitude is not None:
            # location provided by authority
            wrsl.point_string = "POINT ({0} {1})".format(authority_obj.latitude,
                                                         authority_obj.longitude
                                                         )

        if wraddr.street_address is None or wraddr.street_address == "":
            # No address - use default values for address & spatial location
            wraddr.country = 'Australia'
        if wrsl.point_string is None:
            # no spatial - use default value
            wrsl.point_string = "POINT (145.7102081 -37.1905981)"

        # location is deprecated, but still required! Use a dummy value
        wr.location = "location"

        # Assign spatial location to work request
        wr.work_request_spatial_location = wrsl

        # create physical location object and assign address and then assign to
        # request object
        wrfl = Assetic3IntegrationRepresentationsWorkRequestPhysicalLocation()
        wrfl.address = wraddr
        wr.work_request_physical_location = wrfl

        # create object for person that lodged the request
        wrreq = Assetic3IntegrationRepresentationsRequestorRepresentation()
        wrreq.first_name = authority_obj.firstname
        wrreq.surname = authority_obj.familyname
        wrreq.mobile = authority_obj.mobile_phone
        wrreq.phone = authority_obj.home_phone
        wrreq.address_comment = authority_obj.address_comment
        reqtype = Assetic3IntegrationRepresentationsRequestorTypeRepresentation()
        reqtype.id = 4  # indicates 'customer'
        wrreq.types = [reqtype]
        # assign requestor to work request
        wr.requestor = wrreq

        wr.external_identifier = authority_obj.formatted_account
        wr.work_request_source_id = 3  # 3='External CRM'
        # contact customer?
        if authority_obj.contact_method == "NR":
            # no need to respond to customer, but may need to contact
            wr.feedback_required = 0
        else:
            wr.feedback_required = 1
        # contact method
        if authority_obj.contact_method.upper() == "T":
            # Telephone
            wr.feedback_method_id = 1
        elif authority_obj.contact_method.upper() == "F":
            # Fax - unsupported- use phone
            wr.feedback_method_id = 1
        elif authority_obj.contact_method.upper() == "L":
            # Letter
            wr.feedback_method_id = 5
        elif authority_obj.contact_method.upper() == "M":
            # Mobile - use text
            wr.feedback_method_id = 2
        elif authority_obj.contact_method.upper() == "S":
            # Social - email
            wr.feedback_method_id = 3
        else:
            # default to phone
            wr.feedback_method_id = 1
        wr.work_request_priority_id = 1  # default as 1
        wr.description = "Attention: {0}. {1}".format(
            authority_obj.assigned_to, authority_obj.precis.strip())[0:100]
        wr.supporting_information = authority_obj.description
        if authority_obj.due_date is not None:
            wr.resolution_due_date = authority_obj.due_date
            wr.acknowledge_due_date = authority_obj.due_date

        return wr
