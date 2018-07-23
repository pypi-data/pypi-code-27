# from pyrspb.objects import Rarity
from enum import Enum

from pyrspb.utils.string_formatting import *


class Rarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"


class Material:
    def __init__(self, rarity, columns):
        name = columns[0]
        level = columns[1]
        xp = columns[2]
        full_list = columns[-1]

        self.name = name.text.strip()
        self.level = int(level.string)
        self.xp = make_float(xp.text)

        if rarity == Rarity.RARE:
            self.sources = "See the full list of items for source info"
        else:
            self.sources = columns[3].string.strip()

        self.full_list = "https://runescape.wikia.com" + full_list.a["href"]
        self.rarity = rarity

    def __str__(self):
        return "{}\n" \
               "Level: {}\n" \
               "Xp: {}\n" \
               "Sources: {}\n" \
               "Full list: {}".format(self.name, self.level, self.xp, self.sources, self.full_list)
