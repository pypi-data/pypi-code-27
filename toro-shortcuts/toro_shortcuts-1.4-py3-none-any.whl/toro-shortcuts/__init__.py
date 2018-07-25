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
        shortcut = shortcut.replace("left", u"\u2190")
        shortcut = shortcut.replace("right", u"\u2192")
        shortcut = shortcut.replace("up", u"\u2191")
        shortcut = shortcut.replace("down", u"\u2193")
        shortcut = shortcut.replace("tab", u"\u21E5")
        shortcut = shortcut.replace("esc", u"\u238B")
        shortcut = shortcut.replace("space", "Space")

        shortcut = self.capitalize(shortcut)
        shortcut = shortcut.replace("+", "")

        shortcut = re.sub(r'[ ]', "", shortcut).strip()

        return shortcut

    def convertToWindowsLinuxShortcut(self, shortcut):
        """ Converts the keyboard shortcut with Windows/Linux shortcut symbols.
        :param
            shortcut (string): Keyboard shortcut.
        :return:
            string: Converted keyboard shortcut with Windows/Linux shortcut symbols.
        """
        shortcut = shortcut.lower()
        shortcut = shortcut.replace("mod", "Ctrl")
        shortcut = shortcut.replace("alt", "Alt")
        shortcut = shortcut.replace("enter", "Enter")
        shortcut = shortcut.replace("delete", "Delete")
        shortcut = shortcut.replace("shift", "Shift")
        shortcut = shortcut.replace("ctrl", "Ctrl")
        shortcut = shortcut.replace("left", "Left")
        shortcut = shortcut.replace("right", "Right")
        shortcut = shortcut.replace("up", "Up")
        shortcut = shortcut.replace("down", "Down")
        shortcut = shortcut.replace("tab", "Tab")
        shortcut = shortcut.replace("esc", "ESC")
        shortcut = shortcut.replace("space", "Space")
        shortcut = self.capitalize(shortcut)

        shortcut = shortcut.replace("+", " + ")
        shortcut = re.sub(r'[ ]{2,}', " ", shortcut).strip()

        return shortcut

    def capitalize(self, shortcut):
        """
        Capitalizes the shortcut keys.
        :param
            shortcut (string): Keyboard shortcut.
        :return:
            string: Capitalized shortcut keys.
        """

        separator = "+"
        keys = shortcut.split(separator)
        shortcut = ""

        numberOfKeys = len(keys)
        for i, key in enumerate(keys):
            shortcut += key.strip().capitalize()

            if i != numberOfKeys - 1:
                shortcut += separator

        return shortcut

    def handleMatch(self, matched):
        etree = markdown.util.etree

        shortcut = matched.group("shortcut")
        kbdElement = etree.Element("kbd")

        macosShortcut = self.convertToMacOsShortcut(shortcut)
        windowsLinuxShortcut = self.convertToWindowsLinuxShortcut(shortcut)

        kbdElement.set("linux", windowsLinuxShortcut)
        kbdElement.set("windows", windowsLinuxShortcut)
        kbdElement.set("macos", macosShortcut)

        return kbdElement


def makeExtension(*args, **kwargs):
    return ToroElementPatternExtension(*args, **kwargs)


# md = markdown.Markdown(extensions=["toro-shortcuts"])
# print(md.convert("??mod+a??"))