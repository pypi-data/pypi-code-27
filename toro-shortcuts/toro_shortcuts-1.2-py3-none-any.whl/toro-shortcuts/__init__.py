from __future__ import absolute_import
from __future__ import unicode_literals

import markdown
from markdown import Extension
from markdown.inlinepatterns import Pattern
import re

CUSTOM_CLS_RE = r'[?]{2}(?P<shortcut>.*?)[?]{2}'


class ToroElementPatternExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns["toro-shortcuts"] = ToroElementPattern(CUSTOM_CLS_RE, md)


class ToroElementPattern(Pattern):

    def convertToMacOsShortcut(self, shortcut):
        """ Converts the keyboard shortcut with MacOS keyboard shortcut symbols.
        :param
            shortcut (string): Keyboard shortcut.
        :return:
            string: Converted keyboard shortcut with MacOS symbols.
        """
        shortcut = shortcut.lower()
        shortcut = shortcut.replace("mod", u"\u2318")
        shortcut = shortcut.replace("alt", u"\u2325")
        shortcut = shortcut.replace("enter", u"\u23CE")
        shortcut = shortcut.replace("delete", u"\u232B")
        shortcut = shortcut.replace("shift", u"\u21E7")
        shortcut = shortcut.replace("ctrl", u"\u2303")
        shortcut = shortcut.replace("left arrow", u"\u2190")
        shortcut = shortcut.replace("right arrow", u"\u2192")
        shortcut = shortcut.replace("up arrow", u"\u2191")
        shortcut = shortcut.replace("down arrow", u"\u2193")
        shortcut = shortcut.replace("tab", u"\u21E5")
        shortcut = shortcut.replace("esc", u"\u238B")

        shortcut = self.toCapitalize(shortcut, "+")
        shortcut = self.toCapitalize(shortcut, " ")
        shortcut = re.sub(r'[ ]{2,}', " ", shortcut.replace("+", " "))

        return shortcut

    def convertToWindowsLinuxShortcut(self, shortcut):
        """ Converts the keyboard shortcut with Windows/Linux shortcut symbols.
        :param
            shortcut (string): Keyboard shortcut.
        :return:
            string: Converted keyboard shortcut with Windows/Linux shortcut symbols.
        """
        shortcut = shortcut.lower()
        shortcut = shortcut.replace("mod", "ctrl")

        shortcut = self.toCapitalize(shortcut, "+")
        shortcut = self.toCapitalize(shortcut, " ")

        return shortcut

    def toCapitalize(self, shortcut, separator):
        """
        Capitalizes the keyboard shortcut.
        :param
            shortcut (string): Keyboard shortcut.
            separator (string): Separator for the keys in the keyboard shortcut.
        :return:
            string: Capitalized keyboard shortcut.
        """
        keys = shortcut.split(separator)
        shortcut = ""

        numberOfKeys = len(keys)
        for i, key in enumerate(keys):
            shortcut += key.capitalize()

            if i != numberOfKeys-1:
                shortcut += " " + separator + " "

        return re.sub(r'[ ]{2,}', " ", shortcut)

    def handleMatch(self, matched):
        etree = markdown.util.etree

        shortcut = matched.group("shortcut")
        kdbElement = etree.Element("kdb")

        macosShortcut = self.convertToMacOsShortcut(shortcut)
        windowsLinuxShortcut = self.convertToWindowsLinuxShortcut(shortcut)

        kdbElement.set("linux", windowsLinuxShortcut)
        kdbElement.set("windows", windowsLinuxShortcut)
        kdbElement.set("macos", macosShortcut)

        return kdbElement

def makeExtension(*args, **kwargs):
    return ToroElementPatternExtension(*args, **kwargs)