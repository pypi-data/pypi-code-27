# -*- coding: utf-8 -*-
"""
Module containing actions for converting, moving or correcting XML elements
that occur inside the header or the front-matter.
"""

from six import text_type

from lxml import etree

from glamconv.ead.utils import log_element, insert_child_at_element_beginning
from glamconv.ead.formats import EAD_2002
from glamconv.transformer.actions import TransformAction
from glamconv.transformer.parameters import SingleParameter


class IdentifiersDefiner(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"identifiers-definer"
    name = u"Defining identifiers"
    category = u"Header"
    desc = (u"This action defines the identifiers inside the <eadid> element, "
            u"if they are not already defined.")
    params_def = (
        SingleParameter(
            u"country_code", u"Country code",
            u"Code of the country where dwells the organization that "
            u"publishes the EAD. Only some codes are allowed. They are in "
            u"upper case and contain two letters.", u"Text", text_type, u""),
        SingleParameter(
            u"agency_code", u"Agency code",
            u"Code of the organization that publishes the EAD. The codes are "
            u"actually in upper case and begin with the country code.",
            u"Text", text_type, u""),
        SingleParameter(
            u"document_id", u"Document identifier",
            u"Identifier of the document. The identifier usually starts with "
            u"the agency code.", u"Text", text_type, u""),
        SingleParameter(
            u"favour_xml_document_id",
            u"Favour XML data for document identifier",
            u"If the 'identifier' attribute of <eadid> element is not "
            u"defined, it is possible either to gather data from the XML to "
            u"build it (typically the text inside the <eadid> element) or to "
            u"use the value given in the \"Document indentifier\" parameter "
            u"of this action. When this parameter is set, this action will "
            u"first try to use the XML data to build the document identifier "
            u"and will only use the parameter value if no XML data can be "
            u"found. When this parameter is unset, this action will always "
            u"use the parameter value without using the XML data/.",
            u"Boolean", bool, False),
    )

    def _execute(self, xml_root, logger, log_details, country_code,
                 agency_code, document_id, favour_xml_document_id):
        for eadid in xml_root.xpath('.//eadid'):
            if country_code and country_code.upper() != 'FR':
                logger.info('ignoring specified country code %s',
                            country_code.upper())
            eadid.set(u"countrycode", 'FR')
            if agency_code != u"":
                eadid.set(u"mainagencycode", agency_code)
                logger.info(
                    u"Setting the 'mainagencycode' attribute in the <eadid> "
                    u"element", u"    New value: {0}".format(agency_code))
            xml_built_id = (eadid.text or u"").strip()
            if document_id != u"" \
               and (not(favour_xml_document_id) or len(xml_built_id) == 0):
                eadid.set(u"identifier", document_id)
                logger.info(
                    u"Setting the 'identifier' attribute in the <eadid> "
                    u"element from the document_id parameter",
                    u"    New value: {0}".format(document_id))
            elif (favour_xml_document_id and len(xml_built_id) > 0
                  and u"identifier" not in eadid.attrib):
                eadid.set(u"identifier", xml_built_id)
                logger.info(
                    u"Setting the 'identifier' attribute in the <eadid> "
                    u"element from the XML data read in <eadid>",
                    u"    New value: {0}".format(xml_built_id))
        return xml_root


def _add_content_to_odd_elt(xml_root, elements, title, log_data):
    count = 0
    odd_lst = xml_root.xpath(u".//archdesc[1]/odd")
    if len(odd_lst) > 0:
        odd = odd_lst[0]
    else:
        odd = etree.Element(u"odd")
        dsc_lst = xml_root.xpath(u".//archdesc[1]/dsc")
        if len(dsc_lst) > 0:
            dsc_lst[0].addprevious(odd)
        else:
            xml_root.xpath(u".//archdesc[1]")[0].append(odd)
    if title != u"":
        p = etree.SubElement(odd, u'p')
        emph = etree.SubElement(p, u'emph')
        emph.set(u"render", u"bold")
        emph.text = title
    for elt in elements:
        odd.append(elt)
        if log_data is not None:
            log_data.append(log_element(elt, text_content=True))
        count += 1
    return count


class EditionstmtConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"editionstmt-converter"
    name = u"Moving the content of <editionstmt> into <odd>"
    category = u"Header"
    desc = (u"The <editionstmt> element doesn't exist anymore. This action "
            u"moves its content into the <processinfo> element of the "
            u"<archdesc> element. The couples <edition> / <p> in <editionstmt>"
            u"are transformed into list items before being moved in <odd>.")
    params_def = (
        SingleParameter(
            u"title", u"Title",
            u"Title inserted in the <odd> element before the <editionstmt> "
            u"content.", u"Text", text_type, u"Editions"),
    )

    def _execute(self, xml_root, logger, log_details, title):
        count = 0
        log_data = None
        if log_details:
            log_data = []
        list_elt = etree.Element(u"list")
        for edt in xml_root.xpath(u'.//editionstmt/edition'):
            nxt = edt.xpath(u"following-sibling::*")
            if len(nxt) == 0 or nxt[0].tag != u"p":
                itm = etree.Element(u"item")
            else:
                itm = nxt[0]
                itm.tag = u"item"
            list_elt.append(itm)
            emph = etree.Element(u"emph", render=u"bold")
            emph.text = edt.text.strip()
            emph.tail = u": "
            insert_child_at_element_beginning(itm, emph)
        if len(list_elt) > 0:
            count += _add_content_to_odd_elt(xml_root, [list_elt], title,
                                             log_data)
            logger.warning(
                u"Moving the content of <editionstmt> elements into the <odd> "
                u"element in <archdesc>. {0:d} elements have been inserted in "
                u"<odd>".format(count))
            if log_details:
                logger.warning(u"The following elements have been inserted in "
                               u"<odd>:", u"\n".join(log_data))
        for stmt in xml_root.xpath(u'.//editionstmt'):
            stmt.getparent().remove(stmt)
        return xml_root


class NotestmtConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"notestmt-converter"
    name = u"Moving the content of <notestmt> into <odd>"
    category = u"Header"
    desc = (u"The <notestmt> element doesn't exist anymore. This action moves "
            u"its content into the <odd> element in <archdesc>. The <note> "
            u"elements inside <notestmt> are inserted into <p> and then moved "
            u"inside <odd> (as Ape-EAD doesn't allow the notes inside odd).")
    params_def = (
        SingleParameter(
            u"title", u"Title",
            u"Title inserted in the <odd> element before the <notestmt> "
            u"content.", u"Text", text_type, u"Notes"),
    )

    def _execute(self, xml_root, logger, log_details, title):
        count = 0
        log_data = None
        if log_details:
            log_data = []
        elts_to_move = []
        for note in xml_root.xpath(u'.//notestmt/note'):
            p = etree.Element(u"p")
            p.append(note)
            elts_to_move.append(p)
        if len(elts_to_move) > 0:
            count += _add_content_to_odd_elt(xml_root, elts_to_move, title,
                                             log_data)
            logger.warning(
                u"Moving the content of <notestmt> elements into the <odd> "
                u"element in <archdesc>. {0:d} elements have been inserted in "
                u"<odd>".format(count))
            if log_details:
                logger.warning(u"The following elements have been inserted in "
                               u"<odd>:", u"\n".join(log_data))
        for stmt in xml_root.xpath(u'.//notestmt'):
            stmt.getparent().remove(stmt)
        return xml_root


def _div_collapser(div_elt, elts_to_move, level=0):
    head = div_elt.find(u"head")
    if head is not None:
        head.text = (u"> "*level) + (head.text or u"")
        head.tag = u"p"
        if len(head) == 0:
            emph = etree.Element(u"emph", render=u"italic")
            emph.text = head.text
            head.text = None
            head.append(emph)
        elts_to_move.append(head)
    for child in div_elt.xpath(u"*[not(self::head)]"):
        if child.tag == u"div":
            _div_collapser(child, elts_to_move, level+1)
        else:
            elts_to_move.append(child)


class FrontmatterConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"frontmatter-converter"
    name = u"Moving the content of <frontmatter> into <odd>"
    category = u"Header"
    desc = (
        u"The <frontmatter> element doesn't exist anymore in Ape-EAD. This "
        u"action moves its content into the <odd> element in <archdesc> "
        u"element. Be aware that the <titlepage> sub-element is not moved "
        u"and thus is deleted.")
    params_def = (
        SingleParameter(
            u"title", u"Title",
            u"Title inserted in the <odd> element before the <frontmatter> "
            u"content.", u"Text", text_type, u"Prolegomena"),
    )

    def _execute(self, xml_root, logger, log_details, title):
        count = 0
        log_data = None
        if log_details:
            log_data = []
        elts_to_move = []
        for div in xml_root.xpath(u'.//frontmatter/div'):
            _div_collapser(div, elts_to_move)
        if len(elts_to_move) > 0:
            count += _add_content_to_odd_elt(xml_root, elts_to_move, title,
                                             log_data)
            logger.warning(
                u"Moving the content of <frontmatter> elements into the <odd> "
                u"element in <archdesc> (except <titlepage>). {0:d} elements "
                u"have been inserted in <odd>".format(count))
            if log_details:
                logger.warning(u"The following elements have been inserted in "
                               u"<odd>:", u"\n".join(log_data))
        if log_details:
            for ttpg in xml_root.xpath(u'.//frontmatter/titlepage'):
                logger.warning(
                    u"Deleting <titlepage> element inside <frontmatter>. The "
                    u"following sub-elements have been deleted:",
                    log_element(ttpg, text_content=True))
        for ftmtt in xml_root.xpath(u'.//frontmatter'):
            ftmtt.getparent().remove(ftmtt)
        return xml_root


class SponsorConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"sponsor-converter"
    name = u"Moving <sponsor> from <titlestmt> into <odd>"
    category = u"Header"
    desc = (u"In Ape-EAD, the <sponsor> element that could occur in "
            u"<titlestmt> doesn't exist anymore. This action transforms it "
            u"into a paragraph (<p>) and moves it into the <odd> element in "
            u"<archdesc> element.")
    params_def = (
        SingleParameter(
            u"title", u"Title",
            u"Title inserted in the <odd> element before the <sponsor> "
            u"content.", u"Text", text_type, u"Sponsor: "),
    )

    def _execute(self, xml_root, logger, log_details, title):
        count = 0
        log_data = None
        if log_details:
            log_data = []
        elts_to_move = []
        for spsr in xml_root.xpath(u'.//titlestmt/sponsor'):
            spsr.tag = u'p'
            emph = etree.Element(u'emph', render=u"bold")
            emph.text = title
            emph.tail = u" "
            insert_child_at_element_beginning(spsr, emph)
            elts_to_move.append(spsr)
        if len(elts_to_move) > 0:
            count += _add_content_to_odd_elt(xml_root, elts_to_move, title,
                                             log_data)
            logger.warning(
                u"{0:d} <sponsor> elements have been moved into the "
                u"<odd> element in <archdesc>.".format(count))
            if log_details:
                logger.warning(u"The following elements have been moved:",
                               u"\n".join(log_data))
        return xml_root


class StmtPNumEraser(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"stmt-p-num-eraser"
    name = u"Erasing <p>, <num> from <publicationstmt>, <seriesstmt> "
    category = u"Header"
    desc = (u"In Ape-EAD, <p> and <num> elements cannot occur inside "
            u"<publicationstmt> or <seriestmt> elements. This action deletes "
            u"these non-legit child elements.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        xpath_req = (u'.//publicationstmt/p | .//publicationstmt/num | '
                     u'.//seriesstmt/p | .//seriesstmt/num')
        for elt in xml_root.xpath(xpath_req):
            count += 1
            if log_details:
                log_data.append(log_element(elt, text_content=True))
            elt.getparent().remove(elt)
        if count > 0:
            logger.warning(
                u"{0:d} <p> and <num> elements have been deleted "
                u"from <publicationstmt> and <seriesstmt>.".format(count))
            if log_details:
                logger.warning(u"The following elements have been suppressed:",
                               u"\n".join(log_data))
        return xml_root
