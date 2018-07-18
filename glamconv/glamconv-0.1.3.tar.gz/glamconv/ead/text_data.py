# -*- coding: utf-8 -*-
"""
Module containing actions for converting, moving or correcting XML elements
that contain text data.
"""

import itertools
from lxml import etree
from glamconv.ead.utils import (log_element, write_hierarchy, split_qname,
                                insert_text_at_element_end,
                                insert_text_before_element,
                                adjust_content_in_mixed)
from glamconv.ead.formats import EAD_2002
from glamconv.transformer.actions import TransformAction


class AddressConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"address-converter"
    name = u"Converting <address> into <p> in non-legit parents"
    category = u"Text data"
    desc = (
        u"In Ape-EAD, <address> elements can only occur in a few elements. "
        u"This action converts the <address> that occur outside these "
        u"legit parents into paragraphs (<p>). If the parent element can "
        u"only contain text data, this action directly adds the text in "
        u"this parent, each line separated by a hyphen. Be aware that in "
        u"case of imbricated elements, this action can produce a result "
        u"that have imbricated paragraphs (<p>); be sure to execute the "
        u"action that removes non-legit paragraphs after this action.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        text_only_parents = (u"entry", u"event", u"extref", u"extrefloc",
                             u"ref", u"refloc")
        parents = (u"accessrestrict", u"accruals", u"acqinfo",
                   u"altformavail", u"appraisal", u"arrangement",
                   u"bibliography", u"bioghist", u"blockquote",
                   u"controlaccess", u"custodhist",
                   u"descgrp", u"div", u"dsc", u"entry",
                   u"event", u"extref", u"extrefloc", u"fileplan",
                   u"item", u"note", u"odd", u"originalsloc",
                   u"otherfindaid", u"p", u"phystech", u"prefercite",
                   u"processinfo", u"ref", u"refloc", u"relatedmaterial",
                   u"scopecontent", u"separatedmaterial", u"userestrict")
        xpath_req = u' | '.join([u'.//{0}/address'.format(name)
                                 for name in parents])
        for addr in xml_root.xpath(xpath_req):
            parent = addr.getparent()
            if split_qname(parent.tag)[1] in text_only_parents:
                texts = []
                for adln in addr.iterchildren(etree.Element):
                    adjust_content_in_mixed(adln, recursive=True)
                    texts.append(adln.text)
                insert_text_before_element(addr, u" - ".join(texts))
                log_elt = parent
            else:
                p = etree.Element(u"p")
                addr.addprevious(p)
                for adln in addr.iterchildren(etree.Element):
                    insert_text_at_element_end(p, adln.text)
                    p.extend(adln.getchildren())
                    etree.SubElement(p, u"lb")
                if len(p) > 0:
                    p.remove(p[-1])  # Removes last <lb>
                log_elt = p
            parent.remove(addr)
            count += 1
            if log_details:
                log_data.append(log_element(log_elt, text_content=True))
        if count > 0:
            logger.warning(u"{0:d} <address> elements have been converted in "
                           u"<p> elements.".format(count))
            if log_details:
                logger.warning(u"The following elements have been converted:",
                               u"\n".join(log_data))
        return xml_root


def _gather_children_to_move(elt, elts_to_move):
    for child in elt.iterchildren(etree.Element):
        if child.tag == elt.tag:
            _gather_children_to_move(child, elts_to_move)
        else:
            elts_to_move.append(child)


class BlockquoteRemover(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"blockquote-remover"
    name = u"Removing <blockquote> elements"
    category = u"Text data"
    desc = (
        u"The <blockquote> elements don't exist anymore in Ape-EAD. "
        u"This action moves their children into the blockquote parent. The "
        u"blockquote is therefore removed from the EAD tree but its "
        u"content still exits in the tree. When possible, the texts inside "
        u"the paragraphs that were in the blockquote are encapsulated "
        u"into an <emph render=\"italic\"> element. Be aware that in case "
        u"of imbricated elements, this action can produce a result that "
        u"have imbricated paragraphs (<p>); be sure to execute the action "
        u"that removes non-legit paragraphs after this action.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for blq in xml_root.xpath(u'.//blockquote[not(parent::blockquote)]'):
            count += 1
            if log_details:
                log_data.append(log_element(blq, text_content=True))
            # Moves the subelements (children) into the blockquote parent
            elts_to_move = []
            _gather_children_to_move(blq, elts_to_move)
            for subelt in elts_to_move:
                # If subelt is an empty paragraph (most of the cases),
                # adds an emph in the paragraph for italizing the text
                if subelt.tag == u"p" and len(subelt) == 0:
                    emph = etree.Element(u'emph', render=u"italic")
                    emph.text = subelt.text
                    subelt.text = None
                    subelt.append(emph)
                blq.addprevious(subelt)
            # If blockquote has a tail text, inserts it into a paragraph
            if blq.tail is not None and len(blq.tail.strip()) > 0:
                p = etree.Element(u'p')
                p.text = blq.tail
                blq.tail = None
                blq.addprevious(p)
            # Deletes blockquote
            blq.getparent().remove(blq)
        if count > 0:
            logger.warning(
                u"{0:d} <blockquote> elements have been removed by moving "
                u"their child elements into the blockquote parent."
                u"".format(count))
            if log_details:
                logger.warning(u"The following elements have been emptied and "
                               u"deleted:", u"\n".join(log_data))
        return xml_root


class NoteRemover(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"note-remover"
    name = u"Removing <note> elements in non-legit parents"
    category = u"Text data"
    desc = (
        u"In Ape-EAD, <note> elements can only occur in a few elements. "
        u"This action moves the content of the <note> that occur outside "
        u"these legit elements into the note parent. The note is therefore "
        u"removed from the EAD tree but its content still exists in the "
        u"tree. Be aware that in case of imbricated elements, this action "
        u"can produce a result that have imbricated paragraphs (<p>); be "
        u"sure to execute the action that removes non-legit paragraphs "
        u"after this action.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        parents = (u"accessrestrict", u"accruals", u"acqinfo",
                   u"altformavail", u"appraisal",
                   u"archref", u"arrangement", u"bibliography",
                   u"bioghist", u"blockquote", u"controlaccess",
                   u"custodhist", u"descgrp", u"div", u"dsc",
                   u"entry", u"event", u"extref", u"extrefloc",
                   u"fileplan", u"item", u"odd", u"originalsloc",
                   u"otherfindaid", u"phystech", u"prefercite",
                   u"processinfo", u"ref", u"refloc",
                   u"relatedmaterial", u"scopecontent",
                   u"separatedmaterial", u"userestrict")
        xpath_req = u' | '.join([u'.//{0}/note'.format(name)
                                 for name in parents])
        for note in xml_root.xpath(xpath_req):
            count += 1
            if log_details:
                log_data.append(log_element(note, text_content=True))
            # Moves the subelements (children) into the note parent
            elts_to_move = []
            _gather_children_to_move(note, elts_to_move)
            for subelt in elts_to_move:
                note.addprevious(subelt)
            # If note has a tail text, inserts it into a paragraph
            if note.tail is not None and len(note.tail.strip()) > 0:
                p = etree.Element(u'p')
                p.text = note.tail
                note.tail = None
                note.addprevious(p)
            # Deletes note
            note.getparent().remove(note)
        if count > 0:
            logger.warning(
                u"{0:d} <note> elements have been removed by moving their "
                u"child elements into the note parent.".format(count))
            if log_details:
                logger.warning(u"The following elements have been emptied "
                               u"and deleted:", u"\n".join(log_data))
        return xml_root


class ChronlistConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"chronlist-converter"
    name = u"Converting <chronlist> into regular lists"
    category = u"Text data"
    desc = (u"In Ape-EAD, the <chronlist> elements don't exist anymore. "
            u"This action converts these chronological lists into regular "
            u"lists, each item containing the date and the associated "
            u"events. If possible, the date is inserted in an "
            u"<emph render=\"bold\"> element.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for list_elt in xml_root.xpath(u'.//chronlist'):
            list_elt.tag = u"list"
            # Header
            lsthead = list_elt.find(u"listhead")
            if lsthead is not None:
                new_head = False
                head = list_elt.find(u"head")
                if head is None:
                    new_head = True
                    head = etree.Element(u"head")
                for hd_elt in lsthead.iterchildren(etree.Element):
                    if head.text or len(head) > 0:
                        insert_text_at_element_end(head, u" / ")
                    insert_text_at_element_end(head, hd_elt.text)
                    head.extend(hd_elt.getchildren())
                if new_head and (head.text or len(head) > 0):
                    list_elt.insert(0, head)
                list_elt.remove(lsthead)
            # Items
            for chritm in list_elt.xpath(u'chronitem'):
                item = etree.Element(u"item")
                chritm.addprevious(item)
                date = chritm.find(u"date")
                if date is None:
                    continue
                if len(date) == 0:
                    emph = etree.Element(u"emph", render=u"bold")
                    emph.text = date.text
                    date.text = None
                    date.append(emph)
                insert_text_at_element_end(item, date.text)
                item.extend(date.getchildren())
                for idx, evt in enumerate(
                        chritm.xpath(u'event|eventgrp/event')):
                    insert_text_at_element_end(item,
                                               u" : " if idx == 0 else u" ; ")
                    insert_text_at_element_end(item, evt.text)
                    item.extend(evt.getchildren())
                list_elt.remove(chritm)
            count += 1
            if log_details:
                log_data.append(log_element(list_elt))
        if count > 0:
            logger.warning(u"{0:d} <chronlist> elements have been converted "
                           u"into regular lists containing <item>."
                           u"".format(count))
            if log_details:
                logger.warning(u"The following elements have been converted:",
                               u"\n".join(log_data))
        return xml_root


class DefinitionListConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"def-list-converter"
    name = u"Converting <list> with <defitem> children into regular lists"
    category = u"Text data"
    desc = (u"In Ape-EAD, <list> elements can not have <defitem> children. "
            u"This action converts these lists into regular lists by "
            u"converting the <defitem> children into <item> children. "
            u"The content of the <label> child of <defitem> is inserted "
            u"at the begining of the <item> child of <defitem>. If possible, "
            u"the label is inserted in an <emph render=\"bold\"> element.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for list_elt in xml_root.xpath(u'.//list[defitem]'):
            # Header
            head = etree.Element(u"head")
            for hd_elt in list_elt.xpath(u'listhead/*'):
                if head.text or len(head) > 0:
                    insert_text_at_element_end(head, u" / ")
                insert_text_at_element_end(head, hd_elt.text)
                head.extend(hd_elt.getchildren())
            if head.text or len(head) > 0:
                list_elt.insert(0, head)
            lsth = list_elt.find(u"listhead")
            if lsth is not None:
                list_elt.remove(lsth)
            # Items
            for defitm in list_elt.xpath(u'defitem'):
                label = defitm.find(u"label")
                item = defitm.find(u"item")
                if item is None:
                    item = etree.Element(u"item")
                    defitm.append(item)
                if label is not None and len(label) == 0:
                    emph = etree.Element(u"emph", render=u"bold")
                    emph.text = label.text
                    label.text = None
                    label.append(emph)
                insert_text_at_element_end(label,
                                           (u" : " + (item.text or u"")))
                for child in reversed(list(label.getchildren())):
                    item.insert(0, child)
                item.text = label.text
                defitm.addprevious(item)
                list_elt.remove(defitm)
            count += 1
            if log_details:
                log_data.append(log_element(list_elt))
        if count > 0:
            logger.warning(u"{0:d} <list> elements containing <defitem> "
                           u"children have been converted into regular lists "
                           u"containing <item>.".format(count))
            if log_details:
                logger.warning(u"The following elements have been converted:",
                               u"\n".join(log_data))
        return xml_root


def _list_content_extractor(list_elt, extracted_elts, prefix=u"- ",
                            indent=u"  ", level=0):
    for child in list_elt.iterchildren(etree.Element):
        if child.tag == u"head":
            adjust_content_in_mixed(child, recursive=True)
            emph = etree.Element(u"emph", render=u"bold")
            emph.text = child.text
            child.text = indent*level
            child.append(emph)
            extracted_elts.append(child)
            continue
        if child.text or (len(child) > 0 and child[0].tag != u"list"):
            child.text = (indent*level) + prefix + (child.text or u"")
        sublist = child.find(u"list")
        while sublist is not None:
            itm = etree.Element(child.tag)
            itm.text = child.text
            child.text = None
            for subelt in reversed(list(sublist.itersiblings(preceding=True))):
                itm.append(subelt)
            if itm.text or len(itm) > 0:
                extracted_elts.append(itm)
            _list_content_extractor(sublist, extracted_elts,
                                    prefix, indent, level+1)
            child.remove(sublist)
            child.text = sublist.tail
            if child.text or(len(child) > 0 and child[0].tag != u"list"):
                child.text = (indent*level) + prefix + (child.text or u"")
            sublist = child.find(u"list")
        if child.text or len(child) > 0:
            extracted_elts.append(child)


class ListConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"list-converter"
    name = u"Removing <list> elements in non-legit parents"
    category = u"Text data"
    desc = (u"In Ape-EAD, <list> elements can not occur anymore in some "
            u"elements. This action converts each of these lists into a "
            u"paragraph (<p>); the items being separated by line breaks "
            u"(<lb>). If the parent element can't contain a paragraph, "
            u"this action directly adds the text in this parent and "
            u"separates each item by a semi-colon. Be aware that in case "
            u"of imbricated elements, this action can produce a result that "
            u"have imbricated paragraphs (<p>); be sure to execute the action "
            u"that removes non-legit paragraphs after this action.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        text_only_parents = (u"event", u"extref", u"extrefloc", u"ref",
                             u"refloc")
        parents = (u"controlaccess", u"descgrp", u"entry", u"event",
                   u"extref", u"extrefloc", u"note", u"p",
                   u"phystech", u"ref", u"refloc")
        xpath_req = u' | '.join([u'.//{0}/list'.format(name)
                                 for name in parents])
        for list_elt in xml_root.xpath(xpath_req):
            parent = list_elt.getparent()
            if split_qname(parent.tag)[1] in text_only_parents:
                texts = []
                extracted_elts = []
                _list_content_extractor(list_elt, extracted_elts, prefix=u"",
                                        indent=u"")
                for elt in extracted_elts:
                    adjust_content_in_mixed(elt, recursive=True)
                    texts.append(elt.text)
                insert_text_before_element(list_elt, u" ; ".join(texts))
                log_elt = parent
            else:
                p = etree.Element(u"p")
                list_elt.addprevious(p)
                extracted_elts = []
                _list_content_extractor(list_elt, extracted_elts)
                for idx, elt in enumerate(extracted_elts):
                    if idx != 0:
                        etree.SubElement(p, u"lb")
                    insert_text_at_element_end(p, elt.text)
                    p.extend(elt.getchildren())
                log_elt = p
            parent.remove(list_elt)
            count += 1
            if log_details:
                log_data.append(log_element(log_elt, text_content=True))
        if count > 0:
            logger.warning(u"{0:d} <list> elements have been converted into "
                           u"<p> elements.".format(count))
            if log_details:
                logger.warning(u"The following elements have been converted:",
                               u"\n".join(log_data))
        return xml_root


class LegalstatusConverter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"legalstatus-converter"
    name = u"Converting the <legalstatus> into <p>"
    category = u"Text data"
    desc = (u"The <legalstatus> elements don't exist in Ape-EAD. This action "
            u"converts these elements into paragraphs (<p>).")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for stat in xml_root.xpath(u'.//legalstatus'):
            stat.tag = u'p'
            count += 1
            if log_details:
                log_data.append(log_element(stat, text_content=True))
        if count > 0:
            logger.warning(u"{0:d} <legalstatus> elements have been converted "
                           u"into <p> elements.".format(count))
            if log_details:
                logger.warning(u"The following elements have been converted:",
                               u"\n".join(log_data))
        return xml_root


class ParagraphRemover(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"paragraph-remover"
    name = u"Removing <p> elements in non-legit parents"
    category = u"Text data"
    desc = (
        u"After executing the actions that removes blockquotes, addresses, "
        u"notes, lists or tables, the resulting tree can have paragraphs "
        u"that occur in non-legit parents (typically inside another "
        u"paragraph). This action removes these paragraphs but keeps their "
        u"content and adds a line break (<lb>) at the end of this content.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        for p_elt in xml_root.xpath(u'p[parent::p]'):
            insert_text_before_element(p_elt, p_elt.text)
            for child in p_elt:
                p_elt.addprevious(child)
            p_elt.addprevious(etree.Element(u"lb"))
            count += 1
        if count > 0:
            logger.warning(
                u"Removing <p> occuring inside non-legit parents: {0} "
                u"paragraphs have been removed.".format(count))
        return xml_root


MIXED_CONTENT = {
    u"abstract": tuple(),
    u"addressline": tuple(),
    u"archref": tuple(),
    u"author": tuple(),
    u"bibref": (u"imprint", u"name", u"title",),
    u"bibseries": tuple(),
    u"container": tuple(),
    u"corpname": tuple(),
    u"creation": (u"date",),
    u"date": tuple(),
    u"descrules": (u"extref",),
    u"dimensions": tuple(),
    u"edition": tuple(),
    u"emph": tuple(),
    u"entry": tuple(),
    u"event": tuple(),
    u"extent": tuple(),
    u"extref": tuple(),
    u"extrefloc": tuple(),
    u"famname": tuple(),
    u"function": tuple(),
    u"genreform": tuple(),
    u"geogname": tuple(),
    u"head": tuple(),
    u"head01": tuple(),
    u"head02": tuple(),
    u"imprint": (u"date", u"geogname", u"publisher",),
    u"item": (u"emph", u"extref", u"lb", u"list",),
    u"label": tuple(),
    u"langmaterial": (u"language",),
    u"language": tuple(),
    u"langusage": (u"language",),
    u"legalstatus": tuple(),
    u"materialspec": tuple(),
    u"name": tuple(),
    u"num": tuple(),
    u"occupation": tuple(),
    u"origination": (u"corpname", u"famname", u"name", u"persname",),
    u"p": (u"abbr", u"emph", u"expan", u"extref", u"lb", u"note",),
    u"persname": tuple(),
    u"physdesc": (u"dimensions", u"extent", u"genreform", u"physfacet",),
    u"physfacet": tuple(),
    u"physloc": tuple(),
    u"publisher": tuple(),
    u"ref": tuple(),
    u"refloc": tuple(),
    u"repository": (u"address", u"corpname", u"extref", u"name",),
    u"resource": tuple(),
    u"runner": tuple(),
    u"sponsor": tuple(),
    u"subarea": tuple(),
    u"subject": tuple(),
    u"subtitle": (u"emph", u"lb",),
    u"title": tuple(),
    u"titleproper": (u"emph", u"lb",),
    u"unitdate": tuple(),
    u"unitid": (u"extptr", u"title", u"abbr", u"emph", u"expan", u"lb",),
    u"unittitle": (u"abbr", u"emph", u"expan", u"lb",),
}


def _adjust_mixed_content(xml_elt):
    count = 0
    child_names = set()
    if len(xml_elt) == 0:
        return 0
    for child in xml_elt.iterchildren(etree.Element):
        child_names.add(split_qname(child.tag)[1])
        count += _adjust_mixed_content(child)
    namespace, name = split_qname(xml_elt.tag)
    to_keep = MIXED_CONTENT.get(name)
    if namespace is not None or to_keep is None:
        return count
    # If <lb> is not to keep, adds a space
    if u"lb" not in to_keep:
        for lb_elt in xml_elt.xpath(u'lb'):
            lb_elt.tail = u" " + (lb_elt.tail or u"")
    # Suppress the mixed elements not to be kept
    if len(child_names.difference(set(to_keep))) > 0:
        count += 1
    adjust_content_in_mixed(xml_elt, to_keep)
    return count


def _adjust_mixed_content_and_log(xml_elt):
    if len(xml_elt) == 0:
        return []
    children_log_data = {}
    child_names = set()
    for child in xml_elt.iterchildren(etree.Element):
        _, cname = split_qname(child.tag)
        child_names.add(cname)
        if cname not in children_log_data:
            children_log_data[cname] = []
        children_log_data[cname].extend(_adjust_mixed_content_and_log(child))
    namespace, name = split_qname(xml_elt.tag)
    to_keep = MIXED_CONTENT.get(name)
    if namespace is not None or to_keep is None:
        log = list(itertools.chain.from_iterable(children_log_data.values()))
        return log
    removed = set()
    # If <lb> is not to keep, adds a space
    if u"lb" not in to_keep:
        for lb_elt in xml_elt.xpath(u'lb'):
            lb_elt.tail = u" " + (lb_elt.tail or u"")
    # Suppress the mixed elements not to be kept
    for cname in child_names.difference(set(to_keep)):
        removed.add(cname)
        for item in children_log_data.pop(cname):
            removed = removed.union(item[1])
    adjust_content_in_mixed(xml_elt, to_keep)
    log_data = [(write_hierarchy(xml_elt), removed), ]
    log_data.extend(
        list(itertools.chain.from_iterable(children_log_data.values()))
    )
    return log_data


class MixedContentAdjuster(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"mixed-content-adjuster"
    name = u"Removing the non-legit children in the mixed content elements"
    category = u"Text data"
    desc = (u"In Ape-EAD, the elements with a mixed content (child elements "
            u"mixed with text content) have a much more restricted list of "
            u"allowed children. This action removes the non-legit children "
            u"but keeps their textual content.")

    def _execute(self, xml_root, logger, log_details):
        if log_details:
            log_data = _adjust_mixed_content_and_log(xml_root)
            count = len(log_data)
        else:
            count = _adjust_mixed_content(xml_root)
        if count > 0:
            logger.warning(
                u"{0:d} mixed content elements have had some of their "
                u"children deleted".format(count))
            if log_details:
                log_info = [u"{0}\n   Removed elements: {1}"
                            u"".format(elt, u", ".join(remov))
                            for elt, remov in log_data if len(remov) > 0]
                logger.warning(
                    u"The following mixed content elements have "
                    u"been modified:", u"\n".join(log_info))
        return xml_root
