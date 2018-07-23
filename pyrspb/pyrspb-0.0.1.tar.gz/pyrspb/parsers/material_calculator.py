from pyrspb.objects import InventionItem, PageParser


class MaterialCalculator(PageParser):
    def __init__(self, material):
        self.material = material
        PageParser.__init__(self, self.__get_material_url())
        self.items = self.__parse()
        self.ideal_items = self.__filter_and_sort()

    def __get_material_url(self):
        return "https://runescape.wikia.com/wiki/Calculator:Disassembly_by_material/{}".format(self.material)

    def __parse(self):
        table = self.content.find_all("tr", class_="dis-calc-row")
        rows = [row.children for row in table]
        columns = map(list, rows)
        return list(map(InventionItem, columns))

    def __filter_and_sort(self):
        ideal = filter(lambda x: x.cost_per_material <= 100000, self.items)
        ideal = filter(lambda x: x.materials_per_hour >= 100, ideal)
        ideal = filter(lambda x: x.buy_limit > 100, ideal)
        ideal = sorted(ideal, key=lambda x: x.cost_per_material)
        return ideal
