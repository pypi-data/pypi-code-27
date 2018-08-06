#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ORM models for the URL table where we are storing the short url/key and
the long url.

"""
# Standard
import base64

# Third party
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Local
from .settings import DATABASE

Base = declarative_base()


class URL(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(4000), index=True)

    def key(self):
        id = str(self.id).encode('utf-8')
        return base64.b64encode(id).decode('utf-8')


# Stores data in the local directory's db file.
engine = create_engine(DATABASE)

# Create all tables in the engine.
Base.metadata.create_all(engine)
