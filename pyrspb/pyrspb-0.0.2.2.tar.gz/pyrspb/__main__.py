from pyrspb.parsers.invention import MaterialScraper, MaterialSourceScraper
import json
from pyrspb.objects.invention.material import Material
from pyrspb.objects.database import Base, engine, session
from pyrspb.api.invention import material_calculator
import os

print(Material.__table__)
Base.metadata.create_all(engine)
MaterialScraper().save_to_db()
x = MaterialSourceScraper(session.query(Material).filter(Material.name.ilike("%direct%")).one())
items = x.sources
for item in items:
    print(item)
    print(item.material)
x.save_to_db()

# calc = MaterialCalculator("Direct")
# for item in reversed(calc.ideal_items):
#     print(item)
# for s in material_calculator.identify_ideal_sources(material_calculator.material_from_string("direct")):
#     print(s)
# mats = MaterialsScraper()
# mats.dump_to_json()
# for mat in mats.materials:
#     print(str(Material(mat.rarity, dict=mat.to_dict())))
# print("https://discordapp.com/oauth2/authorize?client_id={}&scope=bot".format("470682754929917963"))

# book = BookVersion()
# print(book.version, "|", book.date)

# for item in MaterialCalculator("Dextrous").ideal_items[:5]:
#     print(str(item))

# MaterialCalculator("Dextrous")
# for i in MaterialCalculator("Dextrous").ideal_items[:5]:
#     print(i)
#     print("------")
# mats = MaterialCalculator("Direct")
#
# for i in mats.ideal_items[:5]:
#     print(json.dumps(i.__dict__))
#     print(i)
# for i in mats.ideal_items:
# print("YO", i)


# print(session.query(Material).all())
# direct: Material = session.query(Material).filter(Material.name.ilike("%direct%")).one()
# for source in direct.sources:
#     print(source)
