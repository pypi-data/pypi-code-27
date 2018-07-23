from pyrspb.utils.string_formatting import *


class InventionItem:
    def __init__(self, columns):
        item_name, materials_each, junk_chance, \
          price_per_disassemble, buy_limit, raw_chance, \
          average_number, cost_per_material, materials_per_hour = columns

        self.item_name = item_name.a["title"]
        self.materials_each = int(materials_each.string)
        self.junk_chance = percent_str_to_float(junk_chance.string)
        self.price_per_disassemble = make_float(price_per_disassemble.string)
        self.buy_limit = maybe_make_int(buy_limit.string)
        self.raw_chance = percent_str_to_float(raw_chance.string)
        self.average_number = percent_str_to_float(average_number.string)
        self.cost_per_material = make_int(cost_per_material.string)
        self.materials_per_hour = make_float(materials_per_hour.string)

    def __str__(self):
        return "{} ({}/4hrs) gives {} materials per hour at a cost of {} gp each".format(self.item_name,
                                                                                         self.buy_limit,
                                                                                         self.materials_per_hour,
                                                                                         self.cost_per_material)
