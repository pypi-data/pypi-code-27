# -*- coding: utf-8 -*-

from os import path as osp
from lxml import etree
from glamconv.transformer.actions import ValidateAction


DTD_DIR = osp.join(osp.abspath(osp.dirname(__file__)), "ead-2002-dtd")
EAD_DTD = etree.DTD(osp.join(DTD_DIR, "ead.dtd"))

SCHEMA_DIR = osp.join(osp.abspath(osp.dirname(__file__)), "ape-ead-schema")
EAD_SCHEMA_XML = etree.parse(osp.join(SCHEMA_DIR, "apeEAD.xsd"))
EAD_SCHEMA = etree.XMLSchema(EAD_SCHEMA_XML)


class Ead2002Validator(ValidateAction):
    uid = u"ead-2002-validator"
    name = u"Validating XML data in EAD-2002 format"
    desc = (u"This action validates XML data against the EAD-2002 DTD.")

    def _execute(self, xml_root, logger, log_details):
        result = EAD_DTD.validate(xml_root)
        if result is False:
            error_list = [u"Line {0}: {1}".format(err.line, err.message)
                          for err in EAD_DTD.error_log]
            err_num = len(error_list)
            if err_num > 100:
                error_list = error_list[:100]
                error_list.append(u"... and {0:d} more errors! ..."
                                  u"".format((err_num-100)))
            logger.error(
                u"The XML data doesn't comply with the constraints defined in "
                u"the EAD-2002 standard (DTD). The following validation "
                u"errors have been found:",
                u"\n".join(error_list))
        else:
            logger.info(u"The XML data complies with the EAD-2002 standard "
                        u"(DTD).")
        return result


class ApeEadValidator(ValidateAction):
    uid = u"ape-ead-validator"
    name = u"Validating XML data in Ape-EAD format"
    desc = (u"This action validates XML data against the Ae-EAD XML Schema.")

    def _execute(self, xml_root, logger, log_details):
        result = EAD_SCHEMA.validate(xml_root)
        if result is False:
            error_list = [u"Line {0}: {1}".format(err.line, err.message)
                          for err in EAD_SCHEMA.error_log]
            err_num = len(error_list)
            if err_num > 100:
                error_list = error_list[:100]
                error_list.append(u"... and {0:d} more errors! ..."
                                  u"".format((err_num-100)))
            logger.error(
                u"The XML data doesn't comply with the constraints defined in "
                u"the Ape-EAD standard (XML Schema). The following validation "
                u"errors have been found:",
                u"\n".join(error_list))
        else:
            logger.info(u"The XML data complies with the Ape-EAD standard "
                        u"(XML Schema).")
        return result
