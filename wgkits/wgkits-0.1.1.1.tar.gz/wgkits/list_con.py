# -*- coding:utf-8 -*
"""
author: wang geng
date: 2018-06-15
func: extend ConfigParser class and make it read list items
      modify only '=' as separator for options

"""

try:
    import ConfigParser as cp
except ImportError:
    import configparser as cp
import re

class MyListConf(cp.ConfigParser, object):

    OPTCRE_NV = re.compile(
        r'(?P<option>[^=\s][^=]*)'
        r'\s*(?:'
        r'(?P<vi>[=])\s*'
        r'(?P<value>.*))?$'
        )

    _LIST_R = r"""
        @(list)?
        \s*(?P<header>\w+)
        """

    LISTP = re.compile(_LIST_R, re.VERBOSE)

    def __init__(self):
        super(MyListConf, self).__init__(allow_no_value=True)

    def optionxform(self, optionstr):
        return optionstr

    def _get_list_name(self, section):
        if not self.LISTP.match(section):
            section = "@list "+section
        return section

    def has_list(self, section):
        return self.has_section(self._get_list_name(section))

    def list(self, section):
        return self.options(self._get_list_name(section))

    def lists(self):
        list_sections = []
        for name in self.sections():
            m = self.LISTP.search(name)
            if m:
                list_sections.append(m.group('header'))
        return list_sections
