from pyrspb.objects import PageParser, Material, Rarity


def select_relevant_columns(row):
    _, _, *columns = row
    return columns


def get_rows(table):
    _, *rows = table.find_all("tr")
    return [select_relevant_columns(row) for row in rows]


def make_materials(rarity, cleaned_rows):
    return [Material(rarity, row) for row in cleaned_rows]


class Materials(PageParser):
    def __init__(self):
        PageParser.__init__(self, "https://runescape.wikia.com/wiki/Materials")
        self.materials = self.__parse()

    def __parse(self):
        common_table, uncommon_table, rare_table, *_ = self.content.find_all("table")
        self.common = make_materials(Rarity.COMMON, get_rows(common_table))
        self.uncommon = make_materials(Rarity.UNCOMMON, get_rows(uncommon_table))
        self.rare = make_materials(Rarity.RARE, get_rows(rare_table))
        return self.common + self.uncommon + self.rare
