import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyrspb.db")
engine = create_engine(f"sqlite:////{path}", echo=False)
Base = declarative_base()
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
