from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from pyrspb.objects.database import Base


class Material(Base):
    __tablename__ = "materials"
    name = Column(String, nullable=False, primary_key=True)
    level = Column(Integer, nullable=False)
    xp = Column(Integer, nullable=False)
    rarity = Column(String, nullable=False)
    short_sources = Column(String, nullable=False)
    full_list_url = Column(String, nullable=False)
    sources = relationship("MaterialSource", backref="materials")

    def __str__(self):
        return "{}\n" \
               "Level: {}\n" \
               "Xp: {}\n" \
               "Sources: {}\n" \
               "Full list: {}".format(self.name, self.level, self.xp, self.short_sources, self.full_list_url)

    def __repr__(self):
        return f"<Material(name={self.name}, level={self.level}, xp={self.xp}," \
               f" rarity={self.rarity}, short_sources={self.short_sources}, full_list_url={self.full_list_url})>"
