# -*- coding: utf-8 -*-
"""
Module containing actions for processing the links (URLs and internal links)
inside the XML elements.
"""

from urllib import urlencode

from six import text_type

from lxml import etree

from glamconv.ead.utils import NS, split_qname, log_element
from glamconv.ead.formats import EAD_2002, EAD_APE
from glamconv.transformer.actions import TransformAction
from glamconv.transformer.parameters import SingleParameter, CouplesParameter


class InternalLinkTransformer(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"internal-link-transformer"
    name = u"Transforming <ref> and <ptr> into <extref> and <extptr>"
    category = u"Links & Refs"
    desc = (u"In Ape-EAD, the elements describing an internal link (<ptr> and "
            u"<ref>) doesn't exist anymore. This action transforms the <ref> "
            u"elements into <extref> elements and the <ptr> elements into "
            u"<extptr> elements. The URL of the new link will have the "
            u"following form: \"#internal-id\".")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for elt in xml_root.xpath('.//ref|.//ptr'):
            _, name = split_qname(elt.tag)
            elt.tag = u"ext{0}".format(name)
            if u"target" in elt.attrib:
                elt.set(u"href", u"#{0}".format(elt.attrib.pop("target")))
            count += 1
            if log_details:
                log_data.append(
                    log_element(elt, attributes=(u"href", u"xlink:href")))
        if count > 0:
            logger.warning(
                u"Transforming elements containing an internal link into "
                u"elements containing an external link. {0:d} elements "
                u"have been modified.".format(count))
            if log_details:
                logger.warning(u"The following elements have been modified:",
                               u"\n".join(log_data))
        return xml_root


class ExternalLinkTransformer(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"external-link-transformer"
    name = u"Transforming <archref>, <bibref>, <extptr>, <extref>"
    category = u"Links & Refs"
    desc = (u"This action transforms the <archref>, <bibref>, <extptr> and "
            u"<extref> elements into the legit element for describing the "
            u"external link in the current parent element (e.g. <bibref> in "
            u"<bibliography>, <extref> in <p>).")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        names = (u"archref", u"bibref", u"extptr", u"extref",)
        legit_elt = {u"bibliography": u"bibref", u"unitid": u"extptr",
                     u"descrules": u"extref", u"item": u"extref",
                     u"p": u"extref", u"repository": u"extref"}
        xpath_req = u" | ".join([u'.//{0}'.format(eltname)
                                 for eltname in names])
        for elt in xml_root.xpath(xpath_req):
            parent = elt.getparent()
            newname = legit_elt.get(split_qname(parent.tag)[1], None)
            if newname is None:
                continue
            _, oldname = split_qname(elt.tag)
            if newname == oldname:
                continue
            elt.tag = newname
            count += 1
            lnk = (elt.get(u"href")
                   or elt.get(u"{{{xlink}}}href".format(**NS), u""))
            if newname == "extptr" and len(elt.text or u"") > 0:
                if log_details:
                    log_data.append(
                        log_element(
                            elt, msg=u"    Text content will be deleted",
                            attributes=(u"href", u"xlink:href"),
                            text_content=True))
                elt.text = None
            elif oldname == "extptr" and len(lnk) > 0:
                elt.text = lnk
                if log_details:
                    log_data.append(
                        log_element(
                            elt, msg=u"    href will be added as text content",
                            attributes=(u"href", u"xlink:href")))
            elif log_details:
                log_data.append(
                    log_element(elt, attributes=(u"href", u"xlink:href"),
                                text_content=True))
        if count > 0:
            logger.warning(
                u"Transforming external link elements into the element that "
                u"can occur inside parent element. {0:d} elements have "
                u"been modified.".format(count))
            if log_details:
                logger.warning(u"The following elements have been modified:",
                               u"\n".join(log_data))
        return xml_root


class DaodescEraser(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"daodesc-eraser"
    name = u"Deleting <daodesc> from <dao> and <daogrp>"
    category = u"Links & Refs"
    desc = (u"<daodesc> elements don't exist anymore in Ape-EAD. This "
            u"action deletes the <daodesc> that were defined in <dao> or "
            u"<daogrp> elements.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for elt in xml_root.xpath('.//daodesc'):
            if log_details:
                log_data.append(log_element(elt, text_content=True))
            elt.getparent().remove(elt)
            count += 1
        if count > 0:
            logger.warning(u"{0:d} <daodesc> elements have been deleted."
                           u"".format(count))
            if log_details:
                logger.warning(u"The following elements have been deleted:",
                               u"\n".join(log_data))
        return xml_root


class DaoContentEraser(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"dao-content-eraser"
    name = u"Deleting content in <dao>"
    category = u"Links & Refs"
    desc = (u"In Ape-EAD, <dao> elements must be empty (no text, not even "
            u"spaces). This action deletes the content that might remain in "
            u"<dao> elements.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for elt in xml_root.xpath('.//dao[text() != "" or node()]'):
            elt.text = None
            for child in elt:
                elt.remove(child)
            count += 1
            if log_details:
                log_data.append(
                    log_element(elt, attributes=(u"href", u"xlink:href")))
        if count > 0:
            logger.warning(
                u"Inner content has been deleted from {0:d} <dao> elements."
                u"".format(count))
            if log_details:
                logger.warning(u"The following <dao> elements have been "
                               u"emptied.", u"\n".join(log_data))
        return xml_root


class DaogrpTransformer(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"daogrp-transformer"
    name = u"Transforming <daogrp> into <dao>"
    category = u"Links & Refs"
    desc = (u"Ape-EAD doesn't have any element for describing the extended "
            u"links and their various parts (locator, arc, resource). The "
            u"only possible links are simple links. Instead of simply "
            u"deleting the <daogrp> elements, this action retrieves the "
            u"<daoloc> that often describe some resources (images, etc.) "
            u"and transforms them into <dao> elements outside the <daogrp>. "
            u"The other elements in the <daogrp> (resources, arcs, etc.) are "
            u"deleted.")

    def _execute(self, xml_root, logger, log_details):
        count1, count2 = 0, 0
        if log_details:
            log_data1 = []
            log_data2 = []
        for daogrp in xml_root.xpath(u'.//daogrp'):
            for daoloc in daogrp.xpath(u'daoloc'):
                daoloc.tag = u"dao"
                label = daoloc.attrib.pop(u"label", u"").strip()
                if label != u"" and u"role" not in daoloc.attrib:
                    daoloc.set(u"role", label)
                daogrp.addprevious(daoloc)
                count1 += 1
                if log_details:
                    log_data1.append(
                        log_element(daoloc,
                                    attributes=(u"href", u"xlink:href")))
            if len(daogrp) > 0:
                count2 += 1
                if log_details:
                    log_data2.append(log_element(daogrp))
            daogrp.getparent().remove(daogrp)
        if count1 > 0:
            logger.warning(
                u"{0:d} <dao> elements have been defined from <daoloc> "
                u"found in <daogrp> elements.".format(count1))
            if log_details:
                logger.warning(u"The following <dao> elements have been "
                               u"defined:", u"\n".join(log_data1))
        if count2 > 0:
            logger.warning(
                u"{0:d} <daogrp> elements that contained data other "
                u"than <daoloc> have been deleted.".format(count2))
            if log_details:
                logger.warning(u"The following non-empty <daogrp> elements "
                               u"have been deleted:", u"\n".join(log_data2))
        return xml_root


class ArchdescCDaoMover(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"archdesc-c-dao-mover"
    name = u"Moving <dao> inside <c> or <archdesc> into <did>"
    category = u"Links & Refs"
    desc = (u"In Ape-EAD, the <dao> elements can't be directly inserted into "
            u"a <c> or an <archdesc> element. This action moves the <dao> "
            u"elements from these <c> or <archdesc> into the <did> child "
            u"element they always contain.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for dao in xml_root.xpath(u'.//c/dao | .//archdesc/dao'):
            dids = dao.xpath(u'../did')
            if len(dids) == 0:
                continue
            did = dids[0]
            did.append(dao)
            count += 1
            if log_details:
                log_data.append(
                    log_element(dao, attributes=(u"href", u"xlink:href")))
        if count > 0:
            logger.warning(
                u"{0:d} <dao> elements have been moved from a <c> or an "
                u"<archdesc> into their <did> sibling.".format(count))
            if log_details:
                logger.warning(u"The following <dao> elements have "
                               u"been moved:", u"\n".join(log_data))
        return xml_root


class OddDaoTransformer(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"odd-dao-transformer"
    name = u"Transforming <dao> inside <odd>"
    category = u"Links & Refs"
    desc = (u"In Ape-EAD, the <dao> elements can't exist inside an <odd> "
            u"element. This action transforms these <dao> elements into "
            u"<extref> elements inside a <list>.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for odd in xml_root.xpath(u'.//odd[dao]'):
            lst_elt = etree.SubElement(odd, u'list')
            for dao in odd.xpath(u'dao'):
                dao.tag = u'extref'
                lnk = (dao.get(u"href")
                       or dao.get(u"{{{xlink}}}href".format(**NS), u""))
                title = (dao.get(u"title")
                         or dao.get(u"{{{xlink}}}title".format(**NS), u""))
                if title != u"":
                    dao.text = title
                else:
                    dao.text = lnk
                itm = etree.SubElement(lst_elt, u'item')
                itm.append(dao)
                count += 1
                if log_details:
                    log_data.append(
                        log_element(dao, attributes=(u"href", u"xlink:href")))
        if count > 0:
            logger.warning(u"{0:d} <dao> elements inside an <odd> have been "
                           u"transformed in <extref> element.".format(count))
            if log_details:
                logger.warning(
                    u"Non-legit <dao> elements have been transformed into the "
                    u"following elements:", u"\n".join(log_data))
        return xml_root


class LinkgrpEraser(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"linkgrp-eraser"
    name = u"Erasing the <linkgrp>"
    category = u"Links & Refs"
    desc = (u"Ape-EAD doesn't have any element for describing the extended "
            u"links and their various parts (locator, arc, resource). The "
            u"only possible links are simple links. This action deletes the "
            u"<linkgrp> elements that describe an extended link.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for elt in xml_root.xpath('.//linkgrp'):
            if log_details:
                log_data.append(log_element(elt))
            elt.getparent().remove(elt)
            count += 1
        if count > 0:
            logger.warning(u"{0:d} <linkgrp> elements have been deleted."
                           u"".format(count))
            if log_details:
                logger.warning(u"The following elements have been deleted:",
                               u"\n".join(log_data))
        return xml_root


class XLinkAttribSetter(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"xlink-setter"
    name = u"Using xlink attributes in links"
    category = u"Links & Refs"
    desc = (u"This action transforms the attributes of <bibref>, <extprt>, "
            u"<extref> and <dao> elements that describe the links into the "
            u"corresponding xlink attributes.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        names = (u"bibref", u"extptr", u"extref", u"dao",)
        xpath_req = u" | ".join([u'.//{0}'.format(eltname)
                                 for eltname in names])
        attrs = (u"actuate", u"arcrole", u"href", u"role", u"show", u"title")
        actuate_conv = {u"onload": u"onLoad", u"onrequest": u"onRequest",
                        u"actuatenone": u"none", u"actuateother": u"other"}
        show_conv = {u"new": u"new", u"embed": u"embed",
                     u"showother": u"other",
                     u"shownone": u"none", u"replace": u"replace"}
        for elt in xml_root.xpath(xpath_req):
            # Link is always a simple link in Ape-EAD
            elt.attrib.pop(u"type", None)
            elt.set(u"{{{xlink}}}type".format(**NS), u"simple")
            # Set xlink attributes
            num = 0
            for attname in elt.attrib:
                namespace, name = split_qname(attname)
                if namespace == NS[u"xlink"] or name not in attrs:
                    continue
                attvalue = elt.attrib.pop(attname)
                num = 1
                if name == "actuate":
                    attvalue = actuate_conv.get(attvalue)
                elif name == "show":
                    attvalue = show_conv.get(attvalue)
                attname = u"{{{0}}}{1}".format(NS[u"xlink"], name)
                if attvalue is not None:
                    elt.set(attname, attvalue)
            count += num
            if log_details and num > 0:
                log_data.append(log_element(elt, attributes=(u"xlink:href",)))
        if count > 0:
            logger.warning(
                u"{0:d} elements describing a link have had their attributes "
                u"transformed into xlink attributes.".format(count))
            if log_details:
                logger.warning(u"The following elements have been modified:",
                               u"\n".join(log_data))
        return xml_root


class DaoCharacterReplacer(TransformAction):
    applicable_for = (EAD_2002, EAD_APE)
    uid = u"dao-character-replacer"
    name = u"Replacing characters in the <dao> links"
    category = u"Links & Refs"
    desc = (
        u"This action replaces an expression with another one inside the "
        u"resource link (xlink:href) defined in the <dao> elements. Please "
        u"be sure to execute this action after the link attributes have "
        u"been transformed in xlink attributes.")
    params_def = (
        SingleParameter(
            u"old", u"Old",
            u"Expression to be found in the link and to be replaced by "
            u"the new one", u"Text", text_type, u""),
        SingleParameter(
            u"new", u"New",
            u"Expression replacing the old one in the link",
            u"Text", text_type, u"")
    )

    def _execute(self, xml_root, logger, log_details, old, new):
        count = 0
        if log_details:
            log_data = []
        for dao in xml_root.xpath(u'.//dao'):
            old_href = dao.get(u"{{{xlink}}}href".format(**NS))
            if old in old_href:
                new_href = old_href.replace(old, new)
                dao.set(u"{{{xlink}}}href".format(**NS), new_href)
                count += 1
                if log_details:
                    msg = (u"    Old href : {0}\n    New href : {1}"
                           u"".format(old_href, new_href))
                    log_data.append(log_element(dao, msg=msg))
        if count > 0:
            logger.warning(
                u"{0:d} <dao> elements have had their 'xlink:href' attribute "
                u"modified.".format(count))
            if log_details:
                logger.warning(u"The following elements have been modified:",
                               u"\n".join(log_data))
        return xml_root


class DaoAbsoluteUrlBuilder(TransformAction):
    applicable_for = (EAD_2002, EAD_APE)
    uid = u"dao-absolute-url-builder"
    name = u"Building absolute URLs in the <dao> links"
    category = u"Links & Refs"
    desc = (
        u"Builds an absolute URL from the data found inside the xlink:href "
        u"attribute of the <dao> elements. The URL contains an address "
        u"(e.g. http://www.exemple.com/data/{href}) and parameters "
        u"defined as key/value couples (e.g. height: 128, width: 128, "
        "id: {href}). In one of the other, the {href} expression can "
        u"be used to insert the content of the href attribute of the "
        u"<dao> element (cf. previous examples). Please be sure to execute "
        u"this action after the link attributes have been transformed in "
        u"xlink attributes.")
    params_def = (
        SingleParameter(
            u"url_address", u"Address",
            u"URL address. The expression {href} can be used to insert the "
            u"content of the href attribute of the <dao> element.", u"Text",
            text_type, u""),
        CouplesParameter(
            u"url_params", u"Parameters",
            u"URL parameters defined as a sequence of couples key/value. In "
            u"these values, the expression {href} can be used to insert the "
            u"content of the href attribute of the <dao> element.",
            u"List of couples (text, text)", text_type, text_type, [])
    )

    def _execute(self, xml_root, logger, log_details, url_address, url_params):
        count = 0
        if log_details:
            log_data = []
        for dao in xml_root.xpath(u'.//dao'):
            old_href = dao.get(u"{{{xlink}}}href".format(**NS))
            if u"{href}" in url_address:
                new_href = url_address.format(href=old_href)
            else:
                new_href = url_address
            params = []
            for key, value in url_params:
                if u"{href}" in value:
                    params.append((key, value.format(href=old_href)))
                else:
                    params.append((key, value))
            if len(params) > 0:
                new_href += "?{0}".format(urlencode(params))
            dao.set(u"{{{xlink}}}href".format(**NS), new_href)
            count += 1
            if log_details:
                msg = (u"    Old href : {0}\n    New href : {1}"
                       u"".format(old_href, new_href))
                log_data.append(log_element(dao, msg=msg))
        if count > 0:
            logger.warning(
                u"{0:d} <dao> elements have had an absolute URL built "
                u"in their 'xlink:href' attribute.".format(count))
            if log_details:
                logger.warning(u"The following elements have been modified:",
                               u"\n".join(log_data))
        return xml_root
