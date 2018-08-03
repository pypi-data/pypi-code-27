#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ORM models for the URL table where we are storing the short url/key and
the long url.

"""

# Third party
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Local
from .settings import DATABASE

Base = declarative_base()


class URL(Base):
    __tablename__ = 'urls'
    # MD5 is only 32 characters long. However, I want to have the
    # flexibility to change the hashing algorithm
    short = Column(String(128), primary_key=True, index=True)
    long = Column(String(4000))


# Stores data in the local directory's db file.
engine = create_engine(DATABASE)

# Create all tables in the engine.
Base.metadata.create_all(engine)
