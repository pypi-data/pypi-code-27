# -*- coding: utf-8 -*-
"""
Module containing actions that modify the namespace of the XML elements.
"""

from lxml import etree
from glamconv.ead.utils import NS, split_qname
from glamconv.ead.formats import EAD_2002, EAD_APE
from glamconv.transformer.actions import TransformAction


class EadNamespaceAdder(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"ead-namespace-adder"
    name = u"Adding the Ape-EAD namespace"
    category = u"Naming"
    desc = (u"This action puts all the XML elements with an empty namespace "
            u"inside the Ape-EAD standard namespace. The attribute names are "
            u"not changed. All the other actions designed for EAD-2002 "
            u"documents expect the elements to have an empty namespace "
            u"(such as the elements in EAD 2002). Therefore, be sure to run "
            u"this action at the end of the transformation, just before the "
            u"Ape-EAD validation.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        for elt in xml_root.iter(etree.Element):
            namespace, local_name = split_qname(elt.tag)
            if namespace is None:
                elt.tag = u"{{{0}}}{1}".format(NS["ead"], local_name)
                count += 1
        if count > 0:
            logger.info(u"{0:d} elements with an empty namespace have been "
                        u"transfered in Ape-EAD namespace".format(count))
        return xml_root


class EadNamespaceRemover(TransformAction):
    applicable_for = (EAD_2002, EAD_APE)
    uid = u"ead-namespace-remover"
    name = u"Removing the Ape-EAD namespace"
    category = u"Naming"
    desc = (u"This action puts all the XML elements with the Ape-EAD standard "
            u"namespace inside the empty namespace. The attribute names are "
            u"not changed. This action does the opposite of the action that "
            u"adds the Ape-EAD namespace to the XML elements.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        for elt in xml_root.iter(etree.Element):
            namespace, local_name = split_qname(elt.tag)
            if namespace == NS[u"ead"]:
                elt.tag = u"{{}}{0}".format(local_name)
                count += 1
        if count > 0:
            logger.info(u"{0:d} elements with the Ape-EAD namespace have been "
                        u"transfered in the empty namespace".format(count))
        return xml_root
