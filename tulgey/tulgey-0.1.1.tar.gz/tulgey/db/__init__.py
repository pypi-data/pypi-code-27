from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.exc import OperationalError
from time import sleep
import os
import logging

Base = declarative_base()

__session_factory = None
__engine = None

def connect(cnt=0) -> None:
    global __session_factory
    global __engine

    try:
        if not __engine:
            __engine = create_engine(
                "postgresql://postgres:%s@db:5432/" % os.environ["POSTGRES_PASSWORD"],
                max_overflow=1000  # High number but not setting to -1
            )
        if not __session_factory:
            __session_factory = sessionmaker(bind=__engine)
            Base.metadata.create_all(__engine)
    except OperationalError as e:
        if cnt > 30:
            raise e
        sleep(1)
        logging.info(
            "Failed to connect to DB! Assuming this is a timeout error and waiting 1 second before retrying!"
        )
        return connect(cnt=cnt + 1)

def getSession() -> Session:
    connect()
    return scoped_session(__session_factory)

def getEngine():
    connect()
    return __engine