#! usr/bin/python3

import mysql.connector as mysql
from configparser import ConfigParser
import os

settings = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini')

def read_config(fn):
    config = ConfigParser()
    config.optionxform = str
    config.read(fn)

    return {
        'host': config.get('MYSQL','host'),
        'user': config.get('MYSQL','user'),
        'database': config.get('MYSQL','database'),
        'password': config.get('MYSQL','password')
    }
    
    
if os.path.exists(settings):
    conf = read_config(settings)
    

class Connection:
    manual_config = True
    params = {}
    
    def __init__(self, db=None):             
        try:
            if hasattr(Connection, 'config') and  Connection.manual_config:
                self.connection = mysql.connect(**Connection.config)
            else:
                if 'conf' in globals():
                    config = globals().get('conf')
                    self.connection = mysql.connect(**config)
                    Connection.manual_config = False
                    Connection.params = config
                else:
                    raise SystemExit("No connection to the database")
            if db:
                self.use(db)
         
        except mysql.Error as e:
            if e.errno ==1045:
                raise SystemExit("Invalid Login credentials: %s"%config)
            else:
                print(str(e.msg))
                raise SystemExit(1)
               
                
    @classmethod
    def connect(cls, **kwargs):
        if kwargs:
            cls.config = kwargs
            Connection.manual_config = True
            Connection.params = kwargs
                
    def use(self, db):
        try:
            self.connection.database = db
        except mysql.Error as e:
            if e.errno == mysql.errorcode.ER_BAD_DB_ERROR:
                self.create_database(db)
                self.connection.database = db
            else:
                raise e
                
    def create_database(self, db):
        cursor = self.connection.cursor()
        cursor.execute("CREATE DATABASE %s DEFAULT CHARACTER SET 'utf8'"%db)
            
    def __enter__(self):
        return self.connection
        
    def __exit__(self, exc_type, exc_val, tb):
        if exc_type:
            self.connection.rollback()
            self.connection.close()
            return False
        else:
            try:
                self.connection.commit()
            except mysql.errors.InternalError:
                pass
            self.connection.close()
            return True
            
