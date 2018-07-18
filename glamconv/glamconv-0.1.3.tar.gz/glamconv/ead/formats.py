# -*- coding: utf-8 -*-
"""
Module defining the formats for Ape-EAD and EAD-2002 (instances of
:class:`~glamconv.transformer.formats.DataFormat)
"""

from glamconv.transformer.formats import DataFormat
from glamconv.transformer.rw_actions import XmlReader, XmlWriter
from glamconv.ead.validators import Ead2002Validator, ApeEadValidator


EAD_2002 = DataFormat(
    u"ead-2002", u"XML / EAD-2002", u"text/xml", u".xml",
    u"XML data complying with the EAD-2002 standard as defined in the EAD-2002"
    u" DTD")
XmlReader.applicable_for.add(EAD_2002)
XmlWriter.applicable_for.add(EAD_2002)
Ead2002Validator.applicable_for.add(EAD_2002)
EAD_2002.reading_class = XmlReader
EAD_2002.writing_class = XmlWriter
EAD_2002.validating_class = Ead2002Validator

EAD_APE = DataFormat(
    u"ape-ead", u"XML / Ape-EAD", u"text/xml", u".xml",
    u"XML data complying with the Ape-EAD standard as defined in the Ape-EAD "
    u"XML Schema")
XmlReader.applicable_for.add(EAD_APE)
XmlWriter.applicable_for.add(EAD_APE)
ApeEadValidator.applicable_for.add(EAD_APE)
EAD_APE.reading_class = XmlReader
EAD_APE.writing_class = XmlWriter
EAD_APE.validating_class = ApeEadValidator
