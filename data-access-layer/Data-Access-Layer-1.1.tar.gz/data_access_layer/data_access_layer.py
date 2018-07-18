import pyodbc
import pandas as pd


class DataAccessLayer(object):

    def __init__(self):

        """DataAccessLayer constructor tries to set a connection to the following local server and database:
        selver: DESKTOP-PF3IHF1\SQLEXPRESS
        database: Books"""

        self.connection = None
        self.cursor = None

        # connect to the default database
        print('Connecting to the database...')
        try:
            connection = pyodbc.connect(
                r'Driver={SQL Server}; Server=DESKTOP-PF3IHF1\SQLEXPRESS;Database=Books;Trusted_Connection=yes;')
        except:
            print('Application not connected to a database. execute "connect_to_database" for connection')
            return

        print('Successfully connected to server "DESKTOP-PF3IHF1\SQLEXPRES" and Database: "Books"')

        # assign properties
        self.connection = connection
        self.cursor = connection.cursor()
        self.server_name = 'DESKTOP-PF3IHF1\SQLEXPRESS'
        self.database_name = 'Books'

    def connect_to_database(self, server_name, database_name):

        """connect_to_database allows users to generate a connection to any microsoft server and database selected.
        Inputs:
        sever_name: Full server name, string
        database_name: Name of an existing database on server_name, string"""

        if self.connection is not None:
            print('Currently connected to database "' + self.database_name + '" on server "' + self.server_name)
        else:
            
            # Try connection to the specified server and database
            try:
                connection = pyodbc.connect(
                    r'Driver={SQL Server}; Server=DESKTOP-PF3IHF1\SQLEXPRESS;Database=Books;Trusted_Connection=yes;')
                self.server_name = server_name
                self.database_name = database_name
            except:
                print('Unable to connect to database ' + database_name + ' on server ' +  server_name)

    def disconnect_from_database(self):
        
        """"disconnect_from_database enables to close the connection to the database.
        It will break the connection and clear the variables associated"""

        assert(self.connection is not None), 'DataAccessLayer is already disconnected from the server'
        assert (self.cursor is not None), 'DataAccessLayer is already disconnected from the server'

        # delete cursor and connection
        csr = self.cursor
        csr.close()
        del csr
        self.connection.close()
        self.connection = None
        self.cursor = None

    def get_all_table_names(self):
        
        """get_all_table_names looks for existing data tables within the  
        active database and retrieves a list of table names"""

        query_res = self.cursor.execute('SELECT name FROM sys.Tables')
        table_names = [this_table_name[0] for this_table_name in query_res]
        return table_names

    def get_table_values(self, table_name):
        
        """get_table_values allows to retrieve a full table with all its values.
        Input:
         table_name: must be a string containing the name of one of the existing tables.

        Output will be a pandas.Dataframe format data table with database table contents"""
        
        all_table_names = self.get_all_table_names()
        assert(table_name in all_table_names), 'Table name does not exist within the connected database'

        # write query and retrieve data
        sql_query = 'SELECT * FROM ' + table_name
        data = self.query_data(sql_query)
        return data

    def query_data(self, sql_query):

        """query_data allows the user to query the database just by passing an SQL query syntax.
        Input:
        sql_query: string containing SQL syntax
        Output: pandas.Dataframe object with database table contents"""

        data = pd.io.sql.read_sql(sql_query, self.connection)
        return data

if __name__ == "__main__":
    dal = DataAccessLayer()
    tables = dal.get_all_table_names()
    print(tables)
    for this_table in tables:
        d = dal.get_table_values(this_table)
        print(d)
    dal.disconnect_from_database()
