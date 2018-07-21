#! usr/bin/python3

import mysql.connector as mysql

class Connection:
    manual_config = True
    params = {}
    
    def __init__(self, db=None):             
        try:
            if hasattr(Connection, 'config') and  Connection.manual_config:
                self.connection = mysql.connect(**Connection.config)
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
            
