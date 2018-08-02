from pyrspb.objects import MaterialSource, PageParser
from pyrspb.objects.database import session
from pyrspb.utils.string_formatting import *


def columns_to_item(material, cols):
    item_name_element, materials_each_element, junk_chance_element, \
    price_per_disassemble_element, buy_limit_element, raw_chance_element, \
    average_number_element, cost_per_material_element, materials_per_hour_element = cols

    item_name = item_name_element.a["title"]
    materials_each = make_int(materials_each_element.string)
    junk_chance = percent_str_to_float(junk_chance_element.string)
    price_per_disassemble = make_float(price_per_disassemble_element.string)
    buy_limit = make_int(buy_limit_element.string)
    raw_chance = percent_str_to_float(raw_chance_element.string)
    average_number = percent_str_to_float(average_number_element.string)
    cost_per_material = make_float(cost_per_material_element.string)
    materials_per_hour = make_float(materials_per_hour_element.string)

    return MaterialSource(name=item_name,
                          materials_each=materials_each,
                          junk_chance=junk_chance,
                          price_per_disassemble=price_per_disassemble,
                          buy_limit=buy_limit,
                          raw_chance=raw_chance,
                          average_number=average_number,
                          cost_per_material=cost_per_material,
                          materials_per_hour=materials_per_hour,
                          material=material)


class MaterialSourceScraper(PageParser):
    def __init__(self, material):
        self.material = material
        PageParser.__init__(self, self.__get_material_url())
        self.sources = self.__parse()

    def __get_material_url(self):
        return "https://runescape.wikia.com/wiki/Calculator:Disassembly_by_material/{}" \
            .format(self.material.name.split(" ")[0])

    def __parse(self):
        table = self.content.find_all("tr")
        columns = [list(row.children) for row in table]
        pred = lambda c: len(c) > 3 and 'th' not in list(map(lambda n: n.name, c))
        rows = list(filter(pred, columns))

        return [columns_to_item(self.material, row) for row in rows]

    def save_to_db(self):
        query = session.query(MaterialSource).filter(MaterialSource.material == self.material)
        map(session.delete, query)
        session.add_all(self.sources)
        session.commit()
