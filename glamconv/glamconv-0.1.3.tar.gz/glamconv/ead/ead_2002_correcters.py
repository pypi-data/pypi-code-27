# -*- coding: utf-8 -*-
"""
Module containing actions for correcting XML elements that don't meet the
constraints described in EAD 2002 format.
"""

import re

from lxml import etree

from glamconv.ead.utils import log_element, split_qname
from glamconv.ead.formats import EAD_2002
from glamconv.transformer.actions import TransformAction


class ChangeChildrenOrderer(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"change-children-orderer"
    name = u"Ordering <change> children"
    category = u"EAD 2002 correction"
    desc = (u"In EAD, the children of <change> must occur in a given order "
            u"(first the <date>, then the <item> elements).")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        xpath_req = u".//change[date/preceding-sibling::*]"
        for change in xml_root.xpath(xpath_req):
            if log_details:
                log_data.append(log_element(change))
            count += 1
            # Puts the only <date> at beginning
            for date_elt in change.xpath(u"date[preceding-sibling::*]"):
                change.insert(0, date_elt)
        if count > 0:
            logger.info(
                u"Re-ordering children in <change> elements. {0:d} "
                u"elements have been corrected.".format(count))
            if log_details:
                logger.info(u"The following elements have been corrected:",
                            u"\n".join(log_data))
        return xml_root


class EadheaderChildrenOrderer(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"eadheader-children-orderer"
    name = u"Ordering <eadheader> children"
    category = u"EAD 2002 correction"
    desc = (u"In EAD, the children of <eadheader> must occur in a given order "
            u"(first the <eadid>, then <filedesc>, then <profiledesc>?, "
            u"then <revisiondesc>?).")

    def _execute(self, xml_root, logger, log_details):
        eadheader = xml_root.find('eadheader')
        if eadheader is None:
            return xml_root
        for nodename in ('revisiondesc', 'profiledesc', 'filedesc', 'eadid'):
            node = eadheader.find(nodename)
            if node is not None:
                eadheader.insert(0, node)
        return xml_root


class ArchdescChildrenOrderer(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"archdesc-children-orderer"
    name = u"Ordering <archdesc> children"
    category = u"EAD 2002 correction"
    desc = (
        u"In EAD, the children of <archdesc> must occur in a given order "
        u"(first the <did>, then the archive descriptive elements and then "
        u"the <dsc>). This action puts the children in the expected order. "
        u"This action can be applied to correct EAD trees that are not "
        u"valid against the EAD-2002 standard.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        xpath_req = (u".//archdesc[ "
                     u"  did/preceding-sibling::* or "
                     u"  dsc/following-sibling::*[not(self::dsc)]"
                     u"]")
        for elt in xml_root.xpath(xpath_req):
            if log_details:
                log_data.append(log_element(elt))
            count += 1
            # Puts the only <did> at beginning
            for did in elt.xpath(u"did[preceding-sibling::*]"):
                elt.insert(0, did)
            # Puts last elements before all <dsc>
            dsc = elt.find(u'dsc')
            for subelt in elt.xpath(
                    u"*[not(self::dsc) and preceding-sibling::dsc]"):
                dsc.addprevious(subelt)
        if count > 0:
            logger.info(
                u"Re-ordering children in <archdesc> elements. {0:d} "
                u"elements have been corrected.".format(count))
            if log_details:
                logger.info(u"The following elements have been corrected:",
                            u"\n".join(log_data))
        return xml_root


class CChildrenOrderer(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"c-children-orderer"
    name = u"Ordering <c> children"
    category = u"EAD 2002 correction"
    desc = (u"In EAD, the children of <c> must occur in a given order (first "
            u"the <did>, then the elements for archive description and then "
            u"the <c>). This action puts the children in the expected order."
            u"This action can be applied to correct EAD trees that are not "
            u"valid against the EAD-2002 standard.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        xpath_req = (u".//c["
                     u"  did/preceding-sibling::* or "
                     u"  c/following-sibling::*[not(self::c)]"
                     u"]")
        for elt in xml_root.xpath(xpath_req):
            count += 1
            if log_details:
                log_data.append(log_element(elt))
            # Puts the only <did> at beginning
            for did in elt.xpath(u"did[preceding-sibling::*]"):
                elt.insert(0, did)
            # Puts last elements before all <c>
            c = elt.find(u'c')
            for subelt in elt.xpath(
                    u"*[not(self::c) and preceding-sibling::c]"):
                c.addprevious(subelt)
        if count > 0:
            logger.info(
                u"Re-ordering children in <c> elements. {0:d} "
                u"elements have been corrected.".format(count))
            if log_details:
                logger.info(u"The following elements have been corrected:",
                            u"\n".join(log_data))
        return xml_root


EMPTY_ELTS_TO_ERASE = (
    u"accessrestrict", u"accruals", u"acqinfo", u"address", u"altformavail",
    u"appraisal", u"arrangement", u"bibliography", u"bioghist", u"c",
    u"change", u"controlaccess", u"custodhist", u"descgrp", u"did", u"dsc",
    u"fileplan", u"list", u"note", u"notestmt", u"odd", u"originalsloc",
    u"otherfindaid", u"profiledesc", u"publicationstmt", u"phystech",
    u"prefercite", u"processinfo", u"relatedmaterial", u"revisiondesc",
    u"scopecontent", u"separatedmaterial", u"seriesstmt", u"table",
    u"userestrict",)


class EmptyEltsEraser(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"empty-elts-eraser"
    name = u"Erasing empty elements"
    category = u"EAD 2002 correction"
    desc = (u"In EAD, numerous elements must have at least one child. This "
            u"action erases those elements that don't have any child element. "
            u"This action can be applied to correct EAD trees that are not "
            u"valid against the EAD-2002 format.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        xpath_req = u" | ".join([u".//{0}[not(*)]".format(eltname)
                                 for eltname in EMPTY_ELTS_TO_ERASE])
        for elt in xml_root.xpath(xpath_req):
            count += 1
            if log_details:
                log_data.append(log_element(elt))
            elt.getparent().remove(elt)
        if count > 0:
            logger.warning(u"{0:d} empty elements have been deleted."
                           u"".format(count))
            if log_details:
                logger.warning(u"The following empty elements have been"
                               u"deleted:", u"\n".join(log_data))
        return xml_root


ONE_CONTENT_CHILD_ELTS = (
    u"accessrestrict", u"accruals", u"acqinfo", u"altformavail",
    u"appraisal", u"arrangement", u"bibliography", u"bioghist",
    u"controlaccess", u"custodhist", u"descgrp", u"dsc",
    u"fileplan", u"odd", u"originalsloc", u"otherfindaid", u"phystech",
    u"prefercite", u"processinfo", u"relatedmaterial", u"scopecontent",
    u"separatedmaterial", u"seriesstmt", u"userestrict",)


class ParagraphAdder(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"paragraph-adder"
    name = u"Adding paragraph in elements with only a <head>"
    category = u"EAD 2002 correction"
    desc = (u"In EAD, numerous elements must have at least one child element "
            u"other than <head>. This action adds an empty paragraph (<p>) "
            u"in the elements that don't have such a child element. "
            u"This action can be applied to correct EAD trees that are not "
            u"valid against the EAD-2002 standard.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        xpath_req = u" | ".join(
            [u".//{0}[not(*[not(self::head)])]".format(name)
             for name in ONE_CONTENT_CHILD_ELTS])
        for elt in xml_root.xpath(xpath_req):
            count += 1
            if log_details:
                log_data.append(log_element(elt, text_content=True))
            etree.SubElement(elt, u"p")
        if count > 0:
            logger.warning(u"In {0:d} elements, an empty paragraph has been "
                           u"added in order to have at least one \"content\" "
                           u"child.".format(count))
            if log_details:
                logger.warning(u"The following elements have been modified:",
                               u"\n".join(log_data))
        return xml_root


EMPTY_ATTRS_TO_ERASE = {
    u"c": (u"level",),
    u"c01": (u"level",),
    u"c02": (u"level",),
    u"c03": (u"level",),
    u"c04": (u"level",),
    u"c05": (u"level",),
    u"c06": (u"level",),
    u"c07": (u"level",),
    u"c08": (u"level",),
    u"c09": (u"level",),
    u"c10": (u"level",),
    u"c11": (u"level",),
    u"c12": (u"level",),
}


class EmptyAttrsEraser(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"empty-attrs-eraser"
    name = u"Erasing empty attributes"
    category = u"EAD 2002 correction"
    desc = (u"In EAD, some attributes must have a value taken from a "
            u"vocabulary. This action erases these attributes that are empty."
            u"This action can be applied to correct EAD trees that are not "
            u"valid against the EAD-2002 standard.")

    def _execute(self, xml_root, logger, log_details):
        count_atts = 0
        count_elts = 0
        if log_details:
            log_data = []
        xpath_reqs = []
        for eltname, attnames in EMPTY_ATTRS_TO_ERASE.items():
            xpath_pred = u" or ".join([u'@{0}[normalize-space(text())=""]'
                                       u''.format(name) for name in attnames])
            xpath_reqs.append(u'.//{0}[{1}]'.format(eltname, xpath_pred))
        for elt in xml_root.xpath(u"|".join(xpath_reqs)):
            count_elts += 1
            if log_details:
                deleted = []
            for attname in EMPTY_ATTRS_TO_ERASE[split_qname(elt.tag)[1]]:
                value = elt.attrib.pop(attname, None)
                if value is not None:
                    count_atts += 1
                    if log_details:
                        deleted.append(attname)
            if log_details:
                msg = u"    Deleted attributes: {0}".format(u" ".join(deleted))
                log_data.append(log_element(elt, msg=msg))
        if count_elts > 0:
            logger.warning(u"{0:d} empty attributes have been deleted from "
                           u"{1:d} elements.".format(count_atts, count_elts))
            if log_details:
                logger.warning(u"The following elements have had some "
                               u"attributes deleted:", u"\n".join(log_data))
        return xml_root


class IdentifierConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"identifier-converter"
    name = u"Converting identifier attributes"
    category = u"EAD 2002 correction"
    desc = (u"In EAD, except in <eadid> and <unitid>, the identifier must be "
            u"defined in an 'id' attribute. In <eadid> and <unitid>, it must "
            u"be defined in an 'identifier' attribute. Depending on the "
            u"element, this action renames the 'identifier' attribute in 'id' "
            u"(if there is not already an 'id' attribute) and the 'id' "
            u"attribute in 'identifier' (if there is not already an "
            u"'identifier' attribute). This action can be applied to correct "
            u"EAD trees that are not valid against the EAD-2002 standard.")

    def _execute(self, xml_root, logger, log_details):
        # identifier to id
        count1 = 0
        count2 = 0
        if log_details:
            log_data1 = []
            log_data2 = []
        for elt in xml_root.xpath(u'.//*[namespace-uri() = "" '
                                  u'     and not(self::unitid|self::eadid) '
                                  u'     and @identifier]'):
            if u"id" not in elt.attrib:
                elt.set(u"id", elt.attrib.pop(u"identifier"))
                count1 += 1
                if log_details:
                    log_data1.append(log_element(elt, attributes=(u"id",)))
            else:
                count2 += 1
                if log_details:
                    log_data2.append(
                        log_element(elt, attributes=(u"id", u"identifier",)))
                elt.attrib.pop(u"identifier")
        if count1 > 0:
            logger.warning(u"{0:d} elements have had an 'id' attribute "
                           u"defined from their 'identifier' attribute."
                           u"".format(count1))
            if log_details:
                logger.warning(u"The following elements have been corrected:",
                               u"\n".join(log_data1))
        if count2 > 0:
            logger.warning(u"{0:d} elements have had their 'identifier' "
                           u"attribute deleted because they already had an "
                           u"'id' attribute.".format(count2))
            if log_details:
                logger.warning(u"The following elements have been corrected:",
                               u"\n".join(log_data2))
        # id to identifier
        count1 = 0
        count2 = 0
        if log_details:
            log_data1 = []
            log_data2 = []
        for elt in xml_root.xpath(
                u".//*[(self::unitid|self::eadid) and @id]"):
            if u"identifier" not in elt.attrib:
                elt.set(u"identifier", elt.attrib.pop(u"id"))
                count1 += 1
                if log_details:
                    log_data1.append(
                        log_element(elt, attributes=(u"identifier",)))
            else:
                count2 += 1
                if log_details:
                    log_data2.append(
                        log_element(elt, attributes=(u"id", u"identifier",)))
                elt.attrib.pop(u"id")
        if count1 > 0:
            logger.warning(
                u"{0:d} elements have had an 'identifier' attribute "
                u"defined from their 'id' attribute."
                u"".format(count1))
            if log_details:
                logger.warning(u"The following elements have been corrected:",
                               u"\n".join(log_data1))
        if count2 > 0:
            logger.warning(u"{0:d} elements have had their 'id' attribute "
                           u"deleted because they already had an 'identifier' "
                           u"attribute.".format(count2))
            if log_details:
                logger.warning(u"The following elements have been corrected:",
                               u"\n".join(log_data2))
        return xml_root


class UnitdateCertainlyConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"unitdate-certainly-converter"
    name = u"Converting certainly attribute of <unitdate>"
    category = u"EAD 2002 correction"
    desc = (
        u"In EAD, the attribute for describing the certainty of a "
        u"<unitdate> is 'certainty'. This action corrects the name of this "
        u"attribute when it is mispelled 'certainly'. This action can be "
        u"applied to correct EAD trees that are not valid against the "
        u"EAD-2002 standard.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for elt in xml_root.xpath(u".//unitdate[@certainly]"):
            elt.set(u"certainty", elt.attrib.pop(u"certainly"))
            count += 1
            if log_details:
                log_data.append(log_element(elt, attributes=(u"certainty",),
                                            text_content=True))
        if count > 0:
            logger.warning(u"{0:d} elements have had a 'certainty' attribute "
                           u"defined from their 'certainly' attribute."
                           u"".format(count))
            if log_details:
                logger.warning(u"The following elements have been corrected:",
                               u"\n".join(log_data))
        return xml_root


class COTHERlevelConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"c-OTHERlevel-converter"
    name = u"Converting OTHERlevel attribute of <c>"
    category = u"EAD 2002 correction"
    desc = (u"In EAD, the attribute for describing the other level inside a "
            u"<c> is 'otherlevel'. This action corrects the name of this "
            u"attribute when it is mispelled 'OTHERlevel'. This action can be "
            u"applied to correct EAD trees that are not valid against the "
            u"EAD-2002 standard.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for elt in xml_root.xpath(u".//c[@OTHERlevel]"):
            elt.set(u"otherlevel", elt.attrib.pop(u"OTHERlevel"))
            count += 1
            if log_details:
                log_data.append(log_element(elt, attributes=(u"otherlevel",)))
        if count > 0:
            logger.warning(
                u"{0:d} elements have had an 'otherlevel' attribute "
                u"defined from their 'OTHERlevel' attribute."
                u"".format(count))
            if log_details:
                logger.warning(u"The following elements have been corrected:",
                               u"\n".join(log_data))
        return xml_root


class LowercaseElements(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"lowercase-elts"
    name = u"lowercase elements"
    category = u"EAD 2002 correction"
    desc = u"In EAD, all elements should be lowercase."

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for node in xml_root.getiterator():
            if node.tag is etree.Comment:
                continue
            if not node.tag.islower():
                count += 1
                if log_details:
                    log_data.append(log_element(node))
            node.tag = node.tag.lower()
        if count > 0:
            logger.warning(u"{0:d} elements got lowercased", u"".format(count))
            if log_details:
                logger.warning(u"The following elements have been corrected:",
                               u"\n".join(log_data))
        return xml_root


VALID_ID_RGX = re.compile('[_a-z][_a-z0-9.:-]*', re.I | re.U)


def normalize_xml_id(xml_id):
    """try to build a valid xml identifier out of ``xml_id``"""
    chunks = (x.strip() for x in xml_id.split())
    chunks = (x for x in chunks if x != u'-')
    xml_id = u'-'.join(chunks)
    if xml_id and xml_id[0].isdigit():
        xml_id = '_' + xml_id
    return xml_id


class NormalizeIdAttributes(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"normalize-id"
    name = u"normalize id attributes"
    category = u"EAD 2002 correction"
    desc = u"normalize id attributes."

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for node in xml_root.xpath('.//*[@id]'):
            current_id = node.get('id')
            if VALID_ID_RGX.match(current_id) is None:
                normalized_id = normalize_xml_id(current_id)
                if normalized_id:
                    node.attrib['id'] = normalized_id
                else:
                    node.attrib.pop('id')
                count += 1
                if log_details:
                    log_data.append(log_element(node))
            node.tag = node.tag.lower()
        if count > 0:
            logger.warning(u"{0:d} id attributes got normalized",
                           u"".format(count))
            if log_details:
                logger.warning(u"The following elements have been corrected:",
                               u"\n".join(log_data))
        return xml_root
