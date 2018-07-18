# -*- coding: utf-8 -*-
"""
Module containing actions for deleting attributes or sub-elements from the XML
elements because they don't exist anymore in Ape-EAD format.
"""

from lxml import etree
from glamconv.ead.utils import log_element, split_qname
from glamconv.ead.formats import EAD_2002
from glamconv.transformer.actions import TransformAction


ATTR_TO_ERASE = {
    u"abbr": (u"altrender", u"audience", u"id",),
    u"abstract": (u"altrender", u"audience", u"id", u"langcode",),
    u"accessrestrict": (u"altrender", u"audience", u"id", u"type",),
    u"accruals": (u"altrender", u"audience", u"id",),
    u"acqinfo": (u"altrender", u"audience", u"id",),
    u"address": (u"altrender", u"audience", u"id",),
    u"addressline": (u"altrender", u"audience", u"id",),
    u"altformavail": (u"altrender", u"audience", u"id", u"type",),
    u"appraisal": (u"altrender", u"audience", u"id",),
    u"archdesc": (u"altrender", u"audience", u"id",),
    u"arrangement": (u"altrender", u"audience", u"id",),
    u"author": (u"altrender", u"audience", u"id",),
    u"bibliography": (u"altrender", u"audience", u"id",),
    u"bibref": (u"altrender", u"audience", u"encodinganalog", u"entityref",
                u"id", u"linktype",),
    u"bioghist": (u"altrender", u"audience", u"id",),
    u"blockquote": (u"altrender", u"audience", u"id",),
    u"c": (u"altrender", u"tpattern",),
    u"c01": (u"altrender", u"tpattern",),
    u"c02": (u"altrender", u"tpattern",),
    u"c03": (u"altrender", u"tpattern",),
    u"c04": (u"altrender", u"tpattern",),
    u"c05": (u"altrender", u"tpattern",),
    u"c06": (u"altrender", u"tpattern",),
    u"c07": (u"altrender", u"tpattern",),
    u"c08": (u"altrender", u"tpattern",),
    u"c09": (u"altrender", u"tpattern",),
    u"c10": (u"altrender", u"tpattern",),
    u"c11": (u"altrender", u"tpattern",),
    u"c12": (u"altrender", u"tpattern",),
    u"change": (u"altrender",),
    u"colspec": (u"align", u"char", u"charoff", u"colspec", u"colwidth",
                 u"rowsep",),
    u"container": (u"altrender", u"audience", u"encodinganalog", u"id",
                   u"label",),
    u"controlaccess": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"corpname": (u"altrender", u"audience", u"encodinganalog", u"id",
                  u"normal", u"role", u"rules", u"source"),
    u"creation": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"custodhist": (u"altrender", u"audience", u"id",),
    u"dao": (u"altrender", u"audience", u"entityref", u"id", u"linktype",),
    u"daoloc": (u"altrender", u"audience", u"entityref", u"id", u"linktype",),
    u"date": (u"altrender", u"audience", u"certainty", u"id", u"type",),
    u"descrules": (u"altrender",),
    u"did": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"dimensions": (u"altrender", u"audience", u"encodinganalog", u"id",
                    u"label",),
    u"dsc": (u"altrender", u"audience", u"encodinganalog", u"id", u"othertype",
             u"label", u"tpattern",),
    u"ead": (u"altrender", u"relatedencoding",),
    u"eadheader": (u"altrender", u"audience", u"encodinganalog",
                   u"findaidstatus", u"id",),
    u"eadid": (u"encodinganalog", u"publicid", u"urn",),
    u"emph": (u"altrender", u"id",),
    u"entry": (u"align", u"altrender", u"audience", u"char", u"charoff",
               u"colname", u"colsep", u"id", u"morerows", u"nameend",
               u"namest", u"rowsep", u"valign",),
    u"expan": (u"altrender", u"audience", u"id",),
    u"extent": (u"altrender", u"audience", u"encodinganalog", u"id",
                u"label", u"type",),
    u"extptr": (u"altrender", u"audience", u"entityref", u"id", u"linktype",),
    u"extref": (u"altrender", u"audience", u"entityref", u"id", u"linktype",),
    u"famname": (u"altrender", u"audience", u"encodinganalog", u"id",
                 u"normal", u"role", u"rules", u"source",),
    u"filedesc": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"fileplan": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"function": (u"altrender", u"audience", u"authfilenumber",
                  u"encodinganalog", u"id", u"normal", u"rules", u"source",),
    u"genreform": (u"altrender", u"audience", u"authfilenumber",
                   u"encodinganalog", u"id", u"normal", u"rules", u"source",
                   u"type",),
    u"geogname": (u"altrender", u"audience", u"authfilenumber",
                  u"encodinganalog", u"id", u"normal", u"role", u"rules",
                  u"source",),
    u"head": (u"althead", u"altrender", u"audience", u"id",),
    u"imprint": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"item": (u"altrender", u"audience", u"id",),
    u"label": (u"altrender", u"audience", u"id",),
    u"langmaterial": (u"altrender", u"audience", u"id", u"label",),
    u"language": (u"altrender", u"audience", u"id",),
    u"langusage": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"list": (u"altrender", u"audience", u"continuation", u"id", u"mark",),
    u"materialspec": (u"altrender", u"audience", u"encodinganalog", u"id",
                      u"label", u"type",),
    u"name": (u"altrender", u"audience", u"encodinganalog", u"id", u"normal",
              u"role", u"rules", u"source",),
    u"note": (u"actuate", u"altrender", u"audience", u"id", u"show",),
    u"occupation": (u"altrender", u"audience", u"authfilenumber",
                    u"encodinganalog", u"id", u"normal", u"rules", u"source",),
    u"odd": (u"altrender", u"audience", u"id", u"type",),
    u"originalsloc": (u"altrender", u"audience", u"id", u"type",),
    u"origination": (u"altrender", u"audience", u"id",),
    u"otherfindaid": (u"altrender", u"audience", u"id",),
    u"p": (u"altrender", u"audience", u"id",),
    u"persname": (u"altrender", u"audience", u"encodinganalog", u"id",
                  u"normal", u"role", u"rules", u"source"),
    u"physdesc": (u"altrender", u"audience", u"id", u"label", u"rules",
                  u"source",),
    u"physfacet": (u"altrender", u"audience", u"encodinganalog", u"id",
                   u"label", u"rules", u"source", u"unit",),
    u"physloc": (u"altrender", u"audience", u"encodinganalog", u"id",
                 u"parent", u"type",),
    u"phystech": (u"altrender", u"audience", u"id", u"type",),
    u"prefercite": (u"altrender", u"audience", u"id",),
    u"processinfo": (u"altrender", u"audience", u"id", u"type",),
    u"profiledesc": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"ptr": (u"altrender", u"audience", u"id", u"linktype",),
    u"publicationstmt": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"publisher": (u"altrender", u"audience", u"id",),
    u"ref": (u"altrender", u"audience", u"id", u"linktype",),
    u"relatedmaterial": (u"altrender", u"audience", u"id", u"type",),
    u"repository": (u"altrender", u"audience", u"encodinganalog", u"id",
                    u"label",),
    u"revisiondesc": (u"altrender",),
    u"row": (u"altrender", u"audience", u"id", u"rowsep", u"valign",),
    u"scopecontent": (u"altrender", u"audience", u"id",),
    u"separatedmaterial": (u"altrender", u"audience", u"id", u"type",),
    u"seriesstmt": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"sponsor": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"subject": (u"altrender", u"audience", u"authfilenumber",
                 u"encodinganalog", u"id", u"normal", u"rules", u"source",),
    u"subtitle": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"table": (u"altrender", u"audience", u"colspec", u"frame", u"id",
               u"pgwide", u"rowsep",),
    u"tbody": (u"altrender", u"audience", u"id", u"valign",),
    u"tgroup": (u"align", u"altrender", u"audience", u"colsep", u"id",
                u"rowsep",),
    u"thead": (u"altrender", u"audience", u"id", u"valign",),
    u"title": (u"actuate", u"altrender", u"arcrole", u"audience",
               u"authfilenumber", u"encodinganalog", u"entityref", u"href",
               u"id", u"linktype", u"normal", u"render", u"role", u"rules",
               u"show", u"source", u"title", u"type", u"xpointer",),
    u"titleproper": (u"altrender", u"audience", u"id", u"render",),
    u"titlestmt": (u"altrender", u"audience", u"encodinganalog", u"id",),
    u"unitdate": (u"altrender", u"audience", u"certainty", u"datechar", u"id",
                  u"label", u"type",),
    u"unitid": (u"altrender", u"audience", u"countrycode", u"id",
                u"identifier", u"label", u"repositorycode",),
    u"unittitle": (u"altrender", u"audience", u"id", u"label",),
    u"userrestrict": (u"altrender", u"audience", u"id",),
}


def _delete_attributes_and_log(xml_elt, attrs_to_delete, log_data):
    count_elts = 0
    count_atts = 0
    deleted = []
    for attname in xml_elt.attrib:
        if attname in attrs_to_delete:
            deleted.append(attname)
            xml_elt.attrib.pop(attname)
            count_elts = 1
            count_atts += 1
    if len(deleted) > 0:
        msg = u"    Deleted attributes: {0}".format(u" ".join(deleted))
        log_data.append(log_element(xml_elt, msg=msg))
    return count_elts, count_atts


def _delete_attributes(xml_elt, attrs_to_delete):
    count_elts = 0
    count_atts = 0
    for attname in xml_elt.attrib:
        if attname in attrs_to_delete:
            xml_elt.attrib.pop(attname)
            count_elts = 1
            count_atts += 1
    return count_elts, count_atts


class AttributesEraser(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"attributes-eraser"
    name = u"Erasing attributes that don't exist in Ape-EAD"
    category = u"Cleansing"
    desc = (
        u"Ape-EAD has more constraints than EAD-2002. Numerous elements "
        u"cannot contain some attributes that were authorized in EAD-2002. "
        u"This action deletes these attributes.")

    def _execute(self, xml_root, logger, log_details):
        count_elts, count_atts = 0, 0
        if log_details:
            log_data = []
            for elt in xml_root.iter(etree.Element):
                namespace, name = split_qname(elt.tag)
                if namespace is not None or len(elt.attrib) == 0:
                    continue
                cnt_e, cnt_a = _delete_attributes_and_log(
                    elt, ATTR_TO_ERASE.get(name, tuple()), log_data)
                count_elts += cnt_e
                count_atts += cnt_a
        else:
            for elt in xml_root.iter(etree.Element):
                namespace, name = split_qname(elt.tag)
                if namespace is not None or len(elt.attrib) == 0:
                    continue
                cnt_e, cnt_a = _delete_attributes(
                    elt, ATTR_TO_ERASE.get(name, tuple()))
                count_elts += cnt_e
                count_atts += cnt_a
        if count_elts > 0:
            logger.warning(
                u"Deleting non-legit attributes from the elements. {0:d} "
                u"attributes have been deleted from {1:d} elements."
                u"".format(count_elts, count_atts))
            if log_details:
                logger.warning(u"The following elements have had some "
                               u"attributes deleted:", u"\n".join(log_data))
        return xml_root


def _descgrp_children_move(descgrp_elt, first_following_sibling, log_data):
    count = 1
    if log_data is not None:
        log_data.append(log_element(descgrp_elt))
    last_inserted_note = None
    for child in descgrp_elt.iterchildren(etree.Element):
        nsp, name = split_qname(child.tag)
        if nsp is None and name == u"head":
            last_inserted_note = None
        elif nsp is None and name == u"descgrp":
            last_inserted_note = None
            count += _descgrp_children_move(child, first_following_sibling)
        elif nsp is None and name == u"note":
            last_inserted_note = None
            did_elt = descgrp_elt.find(u"did")
            if did_elt is None:
                continue
            did_elt.append(child)
        elif nsp is None and name in (u"address", u"blockquote", u"chronlist",
                                      u"list", u"p", u"table"):
            if last_inserted_note is None:
                did_elt = descgrp_elt.find(u"did")
                if did_elt is None:
                    continue
                last_inserted_note = etree.SubElement(did_elt, u"note",
                                                      type="descgrp")
            last_inserted_note.append(child)
        else:
            first_following_sibling.addprevious(child)
    return count


class DescgrpRemover(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"descgrp-remover"
    name = u"Removing the <descgrp> elements"
    category = u"Cleansing"
    desc = (u"The <descgrp> elements don't exist any more in Ape-EAD. "
            u"This action moves their children either into their parent "
            u"(<c> or <archdesc>) or into the <did> that exists inside this "
            u"parent.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        log_data = None
        if log_details:
            log_data = []
        for elt in xml_root.xpath(u'.//descgrp[not(parent::descgrp)]'):
            count += _descgrp_children_move(elt, elt, log_data)
            elt.getparent().remove(elt)
        if count > 0:
            logger.warning(
                u"Removing <descgrp> elements from the <archdesc> and <c> "
                u"by moving their child elements inside these <archdesc> or "
                u"<c> elements or inside the <did> that exists in these "
                u"<archdesc> or <c>. Please note that the <head> from the "
                u"<descgrp> have not been moved. {0:d} <descgrp> elements "
                u"have been emptied and deleted.".format(count))
            if log_details:
                logger.warning(u"The following elements have been removed:",
                               u"\n".join(log_data))
        return xml_root


ELTS_TO_ERASE = {u'heritedcontrolaccess', u'runner', u'index', u'xmlvalue'}


class ElementsEraser(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"elements-eraser"
    name = u"Erasing the unknown elements"
    category = u"Cleansing"
    desc = (u"Some elements don't exist in Ape-EAD. "
            u"This action deletes them and their content.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for nodename in ELTS_TO_ERASE:
            for node_elt in xml_root.xpath('.//' + nodename):
                if log_details:
                    log_data.append(log_element(node_elt, text_content=True))
                node_elt.getparent().remove(node_elt)
                count += 1
        if count > 0:
            logger.warning(
                u"{0:d} <runner> elements have been deleted.".format(count))
            if log_details:
                logger.warning(
                    u"The following elements have been deleted:",
                    u"\n".join(log_data))
        return xml_root
