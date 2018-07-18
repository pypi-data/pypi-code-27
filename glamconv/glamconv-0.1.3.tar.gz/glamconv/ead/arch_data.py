# -*- coding: utf-8 -*-
"""
Module containing actions for converting or moving XML elements and their
content because they don't exist anymore in Ape-EAD format.
"""

from lxml import etree
from copy import deepcopy
from glamconv.ead.utils import log_element, split_qname
from glamconv.ead.formats import EAD_2002
from glamconv.transformer.actions import TransformAction


class NumberedCConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"numbered-c-converter"
    name = u"Converting the <c01>...<c12> into <c>"
    category = u"Archive data"
    desc = (u"The <c01>, ... <c12> elements don't exist anymore in Ape-EAD. "
            u"This action converts these elements into <c> elements.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        names = (u"c01", u"c02", u"c03", u"c04", u"c05", u"c06", u"c07",
                 u"c08", u"c09", u"c10", u"c11", u"c12")
        xpath_req = u" | ".join([u'.//{0}'.format(eltname)
                                 for eltname in names])
        for elt in xml_root.xpath(xpath_req):
            elt.tag = u'c'
            if log_details:
                log_data.append(log_element(elt))
            count += 1
        if count > 0:
            logger.info(
                u"Converting numbered c (<c01>, ... <c12>) elements into "
                u"<c> elements. {0:d} elements have been converted"
                u"".format(count))
            if log_details:
                logger.info(u"The following elements have been converted:",
                            u"\n".join(log_data))
        return xml_root


def _move_hierarchical_elements_content(xml_elt, first_following_sibling,
                                        log_data):
    """
    Move the contents of xml_elt element before first_following_sibling
    element. The content of the sub-elements with the same name as xml_elt are
    also moved before new_loc.
    """
    count = 1
    if log_data is not None:
        log_data.append(log_element(xml_elt))
    elt_name = xml_elt.tag
    head = xml_elt.find(u"head")
    if head is not None:
        head.tag = u"p"
        if len(head) == 0:
            emph = etree.Element(u"emph", render=u"bold")
            emph.text = head.text
            head.text = None
            head.append(emph)
        first_following_sibling.addprevious(head)
    for child in xml_elt.xpath(u'*[not(self::head)]'):
        if child.tag == elt_name:
            count += _move_hierarchical_elements_content(
                child, first_following_sibling, log_data)
        else:
            first_following_sibling.addprevious(child)
    xml_elt.getparent().remove(xml_elt)
    return count


class HierarchicalArchEltsCollapser(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"hierarchical-arch-elts-collapser"
    name = (u"Collapsing the hierarchical structure of archive description "
            u"elements")
    category = u"Archive data"
    desc = (u"The <accessrestrict>, <accruals>, <acqinfo>, <altformavail>, "
            u"<appraisal>, <arrangement>, <bibliography>, <bioghist>, "
            u"<controlaccess>, <custodhist>, <fileplan>, <odd>, "
            u"<originalsloc>, <otherfindaid>, <phystech>, <prefercite>, "
            u"<processinfo>, <relatedmaterial>, <scopecontent>, "
            u"<separatedmaterial> and <userestrict> elements cannot contain "
            u"anymore child elements of their own type (with the same tag "
            u"name). This action moves all the content of these child "
            u"elements inside the highest level. The hierarchical structure "
            u"is therefore flattened.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        log_data = None
        if log_details:
            log_data = []
        names = (u"accessrestrict", u"accruals", u"acqinfo", u"altformavail",
                 u"appraisal", u"arrangement", u"bibliography", u"bioghist",
                 u"controlaccess", u"custodhist", u"fileplan", u"odd",
                 u"originalsloc", u"otherfindaid", u"phystech", u"prefercite",
                 u"relatedmaterial", u"processinfo", u"scopecontent",
                 u"separatedmaterial", u"userestrict")
        xpath_req = u" | ".join([u'.//{0}[not(ancestor::{0})]'.format(eltname)
                                 for eltname in names])
        for elt in xml_root.xpath(xpath_req):
            _, eltname = split_qname(elt.tag)
            for sub_elt in elt.xpath('{0}'.format(eltname)):
                count += _move_hierarchical_elements_content(sub_elt, sub_elt,
                                                             log_data)
        if count > 0:
            logger.warning(
                u"Collapsing hierarchical sub-elements for archive "
                u"description into the highest level element. {0:d} elements "
                u"have had their content moved in the highest level element."
                u"".format(count))
            if log_details:
                logger.warning(u"The following elements have been collapsed:",
                               u"\n".join(log_data))
        return xml_root


class ArchEltsLinksInPMover(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"arch-elts-links-in-p-mover"
    name = (u"Moving the links of <separatedmaterial> <relatedmaterial> "
            u"<otherfindaid> in paragraphs")
    category = u"Archive data"
    desc = (u"In Ape-EAD, the <otherfindaid>, <relatedmaterial> and "
            u"<separatedmaterial> elements cannot contain anymore child "
            u"elements that describe a link (<archref>, <bibref>, <extref>, "
            u"<ref>). This action moves these link elements inside a "
            u"paragraph (<p>)")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        names = (u"archref", u"bibref", u"extref", u"ref",)
        parents = (u"otherfindaid", u"relatedmaterial", u"separatedmaterial",)
        xpath_pred = u" or ".join([u'parent::{0}'.format(prtname)
                                   for prtname in parents])
        xpath_req = u" | ".join([u'.//{0}[{1}]'.format(eltname, xpath_pred)
                                 for eltname in names])
        for elt in xml_root.xpath(xpath_req):
            p = etree.Element(u"p")
            elt.addprevious(p)
            p.append(elt)
            if log_details:
                log_data.append(log_element(p, text_content=True))
            count += 1
        if count > 0:
            logger.info(
                u"Moving links into paragraphs. {0:d} <p> elements have been "
                u"created.".format(count))
            if log_details:
                logger.info(u"The following elements have been created:",
                            u"\n".join(log_data))
        return xml_root


class ArchdescCNoteInDidMover(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"archdesc-c-note-in-did-mover"
    name = u"Moving the <note> located in a <c> or an <archdesc> into a <did>"
    category = u"Archive data"
    desc = (u"In Ape-EAD, the <c> and the <archdesc> elements cannot contain "
            u"any <note> child element. If such a child element exist, this "
            u"action moves this <note> inside the <did> child of <c> or "
            u"<archdesc>.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        xpath = u' | '.join(u'.//{}/{}'.format(hostname, nodename)
                            for nodename in (u'note', 'origination')
                            for hostname in (u'c', u'archdesc'))
        for note in xml_root.xpath(xpath):
            parent = note.getparent()
            did = parent.find(u"did")
            if did is None:
                continue
            did.append(note)
            if log_details:
                log_data.append(log_element(note, text_content=True))
            count += 1
        if count > 0:
            logger.info(
                u"Moving <note> elements located in an <archdesc> or a <c> "
                u"element, into their sibling <did> (child of <archdesc> or "
                u"<c>). {0:d} elements have been moved.".format(count))
            if log_details:
                logger.info(u"The following elements have been moved:",
                            u"\n".join(log_data))
        return xml_root


class DidAbstractConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"did-abstract-converter"
    name = u"Converting the <abstract> in <did> into <note>"
    category = u"Archive data"
    desc = (u"In Ape-EAD, the <abstract> elements can't exist in the <did> "
            u"elements. This action converts these abstracts into <p> in "
            u"<note> elements. Further actions will convert the abstract "
            u"children in order to meet the constraints of Ape-EAD related "
            u"to <p> elements.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for elt in xml_root.xpath(u'.//did/abstract'):
            note = etree.Element(u"note")
            elt.addprevious(note)
            for attr in elt.attrib:
                note.set(attr, elt.attrib.pop(attr))
            elt.tag = u'p'
            note.append(elt)
            if "type" not in note.attrib:
                note.set(u"type", u"abstract")
            elif "label" not in note.attrib:
                note.set(u"label", u"abstract")
            if log_details:
                log_data.append(log_element(note, text_content=True))
            count += 1
        if count > 0:
            logger.warning(
                u"Converting <abstract> elements inside <did> into <p> "
                u"elements inserted in <note>. {0:d} elements have been "
                u"converted.".format(count))
            if log_details:
                logger.warning(u"The following elements have been converted:",
                               u"\n".join(log_data))
        return xml_root


class UnittitleUnitdateInDidCopier(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"unittitle-unitdate-in-did-copier"
    name = u"Copying <unitdate> located in a <unittitle> in parent <did>"
    category = u"Archive data"
    desc = (u"In Ape-EAD, the <unittitle> elements cannot contain <unitdate> "
            u"elements so these date markers will be suppressed by another "
            u"cleaning action. In order to keep the date marker, if a "
            u"<unitdate> occurs in a <unittitle> and this <unittitle> is "
            u"inside a <did> element, this action copies the <unitdate> "
            u"inside this <did> if it hasn't already got a <unitdate>.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for unitdate in xml_root.xpath(
                u'.//unitdate[parent::unittitle/parent::did[not(unitdate)]]'):
            unittitle = unitdate.getparent()
            did = unittitle.getparent()
            new_date = deepcopy(unitdate)
            new_date.tail = None
            did.append(new_date)
            if log_details:
                log_data.append(log_element(new_date, text_content=True))
            count += 1
        if count > 0:
            logger.info(
                u"Copying <unitdate> elements located in a <unittitle> "
                u"element, inside the upper-level <did> element that did not "
                u"have a <unitdate>. {0:d} elements have been copied."
                u"".format(count))
            if log_details:
                logger.info(u"The following elements have been copied:",
                            u"\n".join(log_data))
        return xml_root


class IncorrectNormalDateError(Exception):
    pass


# Dates can be: "21001231", "2100-12-31", "2100-12", "2100",
# "21001231/-19001201", "2100-12-31/-1900-12-01", "2100-12/-1900-12",
# ""2100/-1900" and all the mixed combinations around the "/".
#
# The regular expresssion engine of Python doesn't always give the same
# results as the one of XML Schema. So we're going back to actual Python code.
class IncorrectNormalDateEraser(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"incorrect-normal-date-eraser"
    name = u"Deleting incorrect normalized dates"
    category = u"Cleansing"
    desc = (u"This action deletes normalized values in the <unitdate> and "
            u"the <date> elements when they don't conform with the expected "
            u"format.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        xpath_req = './/unitdate[@normal] | .//date[@normal]'
        for date_elt in xml_root.xpath(xpath_req):
            norm_date = date_elt.attrib.get(u"normal", u"")
            try:
                if norm_date.strip() == u"" or norm_date.strip()[-1] == u"/":
                    raise IncorrectNormalDateError()
                parts = norm_date.split(u"/")
                if len(parts) > 2:
                    raise IncorrectNormalDateError()
                for part in parts:
                    if len(part) == 0:
                        raise IncorrectNormalDateError()
                    if part[0] == u"-":
                        part = part[1:]
                    if u"-" not in part:
                        if len(part) == 4:
                            elts = (part,)
                        elif len(part) == 8:
                            elts = (part[:4], part[4:6], part[6:])
                        else:
                            raise IncorrectNormalDateError()
                    else:
                        elts = part.split(u"-")
                    if len(elts) < 1 or len(elts) > 3:
                        raise IncorrectNormalDateError()
                    length = {0: 4, 1: 2, 2: 2}
                    valmin = {0: 0, 1: 1, 2: 1}
                    valmax = {0: 2999, 1: 12, 2: 31}
                    for idx, elt in enumerate(elts):
                        if u" " in elt or len(elt) != length[idx] \
                           or not elt.isdigit():
                            raise IncorrectNormalDateError()
                        if (int(elt) < valmin[idx] or int(elt) > valmax[idx]):
                            raise IncorrectNormalDateError()
            except IncorrectNormalDateError:
                date_elt.attrib.pop(u"normal")
                if log_details:
                    msg = u"    Deleted value: {0}".format(norm_date)
                    log_data.append(log_element(date_elt, msg=msg))
        if count > 0:
            logger.warning(
                u"Deleting the 'normal' attribute in the date elements "
                u"because its value doesn't conform with the expected format. "
                u"{0:d} elements have had their attribute deleted."
                u"".format(count))
            if log_details:
                logger.warning(u"The following elements have been modified:",
                               u"\n".join(log_data))
        return xml_root
