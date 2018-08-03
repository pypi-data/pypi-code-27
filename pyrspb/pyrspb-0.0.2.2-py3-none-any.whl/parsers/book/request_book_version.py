import re

from pyrspb.objects.page_parser import PageParser


class VersionScraper(PageParser):
    def __init__(self):
        PageParser.__init__(self, "https://rspocketbook.com/")
        self.version, self.date = self.__parse()

    def __parse(self):
        *junk, version = self.content.find_all("div", class_="box")
        full_version_string = version.find_all("p")[-1].text
        # v
        version, date = re.search('(v[\d|\.]+\d). (.+)', full_version_string).groups()
        return [version, date]

