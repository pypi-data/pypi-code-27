import datetime
from typing import List

from pyrspb.objects.database import session
from pyrspb.objects.invention import Material, MaterialSource
from pyrspb.parsers.invention import MaterialSourceScraper


def material_from_string(s: str) -> Material:
    return session.query(Material).filter(Material.name.ilike(f"%{s}%")).one_or_none()


def identify_ideal_sources(m: Material, buy_limit=100, cost_per=100000, per_hour=100) -> List[MaterialSource]:
    # Save sources if they don't exist
    # Call function again with updated object
    if m.rarity == "Rare":
        return []
    elif len(m.sources) is 0:
        MaterialSourceScraper(m).save_to_db()

    sources: List[MaterialSource] = m.sources
    # Last time data was pulled
    last_updated: datetime.timedelta = datetime.datetime.now() - sources[0].last_updated
    # Update the db if it's been over a day
    if last_updated.days >= 1:
        MaterialSourceScraper(m).save_to_db()

    return session.query(MaterialSource).filter(MaterialSource.material == m) \
        .filter(MaterialSource.buy_limit >= buy_limit) \
        .filter(MaterialSource.cost_per_material <= cost_per) \
        .filter(MaterialSource.materials_per_hour >= per_hour) \
        .order_by(MaterialSource.cost_per_material).all()
