import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'shpAKIsnmnm6YadSdfXcVbN2G4zbKBZHkjhKSHsJKHsJKHsH'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'mssql+pyodbc://(local)/MidaxUsers?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False