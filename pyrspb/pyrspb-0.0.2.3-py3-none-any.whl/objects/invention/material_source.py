import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from pyrspb.objects.database import Base
from pyrspb.objects.invention.material import Material


class MaterialSource(Base):
    __tablename__ = "material_sources"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    materials_each = Column(Integer, nullable=False)
    junk_chance = Column(Float, nullable=False)
    price_per_disassemble = Column(Float, nullable=False)
    buy_limit = Column(Integer, nullable=False)
    raw_chance = Column(Float, nullable=False)
    average_number = Column(Float, nullable=False)
    cost_per_material = Column(Float, nullable=False)
    materials_per_hour = Column(Float, nullable=False)
    material_name = Column(String, ForeignKey("materials.name"))
    material = relationship(Material, backref="material_sources")
    last_updated = Column(DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now())

    def __str__(self):
        return "{} ({}/4hrs) gives {} {} per hour at a cost of {} gp each".format(self.name,
                                                                                  self.buy_limit,
                                                                                  self.materials_per_hour,
                                                                                  self.material.name,
                                                                                  self.cost_per_material)

    def __repr__(self):
        return f"<MaterialSource(name={self.name})>"

#
#
# class InventionItem:
#     def __init__(self, columns):
#         item_name, materials_each, junk_chance, \
#           price_per_disassemble, buy_limit, raw_chance, \
#           average_number, cost_per_material, materials_per_hour = columns
#
#         self.item_name = item_name.a["title"]
#         self.materials_each = make_int(materials_each.string)
#         self.junk_chance = percent_str_to_float(junk_chance.string)
#         self.price_per_disassemble = make_float(price_per_disassemble.string)
#         self.buy_limit = make_int(buy_limit.string)
#         self.raw_chance = percent_str_to_float(raw_chance.string)
#         self.average_number = percent_str_to_float(average_number.string)
#         self.cost_per_material = make_float(cost_per_material.string)
#         self.materials_per_hour = make_float(materials_per_hour.string)
#
#     def __str__(self):
#         return "{} ({}/4hrs) gives {} materials per hour at a cost of {} gp each".format(self.item_name,
#                                                                                          self.buy_limit,
#                                                                                          self.materials_per_hour,
#                                                                                          self.cost_per_material)
