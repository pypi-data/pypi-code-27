from typing import List

from bs4.element import PageElement

from pyrspb.objects import PageParser, Material
from pyrspb.objects.database import session
from pyrspb.utils.string_formatting import *
from . import MaterialSourceScraper


def select_relevant_columns(row: List[PageElement]):
    _, _, *columns = row
    return columns


def get_rows(table):
    _, *rows = table.find_all("tr")
    return [select_relevant_columns(row) for row in rows]


def extract_info(rarity, row):
    count = len(row)
    name_element, level_element, xp_element, *rest = row
    data = []

    if count == 5:
        sources_element, full_list_element = rest
        data.append(sources_element.text.strip())
        data.append("https://runescape.wikia.com" + full_list_element.a["href"])
    elif count == 4:
        sources = "See the full list of items for source info"
        full_list_element = rest[-1]
        data.append(sources)
        data.append("https://runescape.wikia.com" + full_list_element.a["href"])
    else:
        return None

    sources, full_list = data
    name = name_element.text.strip()
    level = int(level_element.text)
    xp = make_float(xp_element.text)

    return Material(name=name,
                    level=level,
                    xp=xp,
                    short_sources=sources,
                    full_list_url=full_list,
                    rarity=rarity)


class MaterialScraper(PageParser):
    def __init__(self):
        PageParser.__init__(self, "https://runescape.wikia.com/wiki/Materials")
        self.materials = self.__parse()

    def __parse(self):
        common_table, uncommon_table, rare_table, *_ = self.content.find_all("table")
        self.common = [extract_info("Common", row) for row in get_rows(common_table)]
        self.uncommon = [extract_info("Uncommon", row) for row in get_rows(uncommon_table)]
        self.rare = [extract_info("Rare", row) for row in get_rows(rare_table)]
        return self.common + self.rare + self.uncommon

    def save_to_db(self):
        session.query(Material).delete()
        # for m in self.materials:
        #
        #     session.query(Material).filter(Material.name == m.name).delete()
        #     session.add(new_material)
        session.add_all(self.materials)
        session.commit()
