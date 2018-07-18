#! usr/bin/env python3
from client_proxy import Proxy
from collections import OrderedDict, ChainMap
import models
import csv
import os


class BaseMeta(type):

    @classmethod
    def __prepare__(cls, name, bases):
        fields_dict = {key:val for key, val in models.__dict__.items()
        if isinstance(val, models.DescriptorMeta)}
      
        return dict(ChainMap({}, fields_dict))
        
    def __new__(meta, clsname, bases, clsdict):
        clsobj = super().__new__(meta, clsname, bases, clsdict)
        
        # set names on descriptors
        for key, val in vars(clsobj).items():
            if isinstance(val, models.Descriptor):
                setattr(val, 'name', key)
                
        # make __init__ based on fields
        fields = [key for key, val in clsobj.__dict__.items()
        if isinstance(val, models.Descriptor) ]
        setattr(clsobj, 'fields', fields)
        
        columns = {key:val for key,val in vars(clsobj).items() if isinstance(val, models.Descriptor)}
        setattr(clsobj, 'columns', columns)
        
        return clsobj
        
class Base(metaclass=BaseMeta):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.proxy = Proxy()
        
        for name, value in kwargs.items():
            if name in self.fields:
                setattr(self, name, value)

        self.create_table()
        
    def __repr__(self):
        params = ', '.join("%s='%s'" % (key, val)
                for key, val in self.kwargs.items())

        return "<{}({})>".format(type(self).__name__, params)
              
        
    @classmethod
    def schema(cls):
        sql = "CREATE TABLE IF NOT EXISTS %s ("%cls.table
        for key, val in cls.__dict__.items():
            if isinstance(val, models.Descriptor):
                sql += "%s %s, " % (key, str(val))
        if 'pk' in cls.__dict__:
            pk = cls.__dict__['pk']
            sql = sql[:-2] + ", PRIMARY KEY(`%s`)) ENGINE=InnoDB"%pk
        else:
            sql = sql[:-2] + ") ENGINE=InnoDB"

        return sql
        
    def create_table(self):
        return self.proxy.execute(self.schema())         
        
    def getall(self, as_dict=False, only_one=False):
        SQL = "SELECT * FROM %s"%self.table
        return self.proxy.get(SQL, as_dict, only_one)
        
        
    def get(self, as_dict=False, only_one=False, strict=True, 
        groupby=None, orderby=None, 
        sortby='ASC', limit=None, offset=None, **where):
        
        if not where:
            query = 'SELECT * FROM %s'%self.table
        else:
            query = 'SELECT * FROM %s WHERE'%self.table
                
        index= 1
        operator = '=' if strict else 'RLIKE'

        for key, value in where.items():
            if index == 1:
                query+= " %s %s '%s'"%(key, operator, value)
            else:
                query+= " AND %s %s '%s' "%(key, operator, value)
            index += 1
            
        if groupby:
            query += " GROUP BY %s"%groupby
            
        if orderby:
            query += " ORDER BY %s %s"%(orderby, sortby)
            
        # Apply limit filters and grouping
        if isinstance(limit, int):
            query += " LIMIT %s"%limit
        
        if isinstance(offset, int):
            query += " OFFSET %s"%offset
        
        return self.proxy.get(query, as_dict, only_one)
        
    def execute(self, sql):
        return self.proxy.execute(sql)
        
    def exists(self):
        ''' Check if a record of exists in table '''
        try:
            ID = self.kwargs.get(self.pk)
            result = self.get(ID, only_one=True)
            return len(result) > 0
        except AttributeError:
            return "Can't use exists. pk attr not in cls %s"%self.__class__.name__
        
    def save(self):
        keys = ", ".join(list(self.kwargs.keys()))
        values = tuple(list(self.kwargs.values()))
        
        SQL = """INSERT INTO %s (%s) VALUES(""" % (self.table, keys)
        SQL += """ "%s",""" * len(values) % (values)
        SQL = SQL[:-1] + ")"
        
        return self.proxy.save(SQL) 
    
    def description(self):
        sql = "DESCRIBE %s"%self.table
        return self.proxy.description(sql)
        
        
    def update(self, update_on='patient_id'):
        keys = ", ".join(list(self.kwargs.keys()))
        values = tuple(list(self.kwargs.values()))
        
        SQL = """UPDATE {} SET """.format(self.table)
        for key, value in self.kwargs.items():
            SQL += """ %s = "%s" ,""" % (key, value)

        SQL = SQL[:-1] + """ WHERE {} = "{}" """.format(update_on, self.kwargs.get(update_on))
        print(SQL)
        return self.proxy.update(SQL)
        
        
    def delete(self, del_on='patient_id'):
        SQL = "DELETE FROM %s WHERE %s= '%s' "%(self.table, del_on, self.kwargs.get(del_on))
        return self.proxy.delete(SQL)
        
        
    def drop(self):
        ans = input('Are you sure you want to drop the table: %s [y/n]'%self.table)
        if ans =='y':
            sql = "DROP TABLE IF EXISTS %s"%self.table
            self.proxy.execute(sql)
            return True
        else:
            print("Operation cancelled by user")
            return False
            
    def drop_column(self, column):
        sql ="ALTER TABLE %s DROP COLUMN %s"%(self.table, column)
        print(sql)
        return self.proxy.execute(sql)
        
    def add_column(self, column, after):
        sql ="ALTER TABLE {} ADD COLUMN {} AFTER {}"
        sql = sql.format(self.table, column, after)
        print(sql)
        self.proxy.execute(sql)
        
        
    def alter_column(self, old_column, new_column):
        sql ="ALTER TABLE {} CHANGE COLUMN {} {}"
        sql = sql.format(self.table, old_column, new_column)
        print(sql)
        self.proxy.execute(sql)
    
            
    def __eq__(self, other):
        if type(self) == type(other):
            if self.kwargs == other.kwargs:
                return True
                
            else:
                return False
        else:
            return False
    
    def to_csv(self):
        header_row = self.description()
        data = self.get()
        filename = self.__class__.__name__ + ".txt"
        
        with open(filename, 'w', newline="") as in_file:
            writer = csv.writer(in_file)
            writer.writerow(header_row)    
            for row in data:
                writer.writerow(row)
                
        return filename
       
    def read_csv(self, filename):
        fn = os.path.abspath(filename)
        if os.path.exists(fn):
            reader = csv.reader(open(fn))
            return [tuple(row) for row in reader]
            
            
    def save_csv_data(self, data):
        if not data:
            return (False, "No csv data")
            
        if not isinstance(data, (list, tuple)):
            raise ValueError("Invalid data type: %s. "
            "Expected list or tuple "%(type(data)))
            
        keys = ", ".join(data[0])
        params = data[0]
        values = tuple(data[1:])
        #tuple of tuples --> Use executemany()
       
        SQL = """INSERT INTO %s (%s) VALUES(""" % (self.table, keys)
        SQL += """%s,""" * len(params)
        SQL = SQL[:-1] + ")"
        return self.proxy.execute_many(SQL, values)
        
    def as_csv_data(self, filename, iterable):
        if isinstance(iterable, (list, tuple)):
            with open(filename, 'w', newline="") as in_file:
                writer = csv.writer(in_file)
                for row in iterable:
                    writer.writerow(row)
                    
            return filename
        return False
           
    def __iter__(self):
        for record in self.getall():
            yield record
            
    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.getall()[index]
        elif isinstance(index, numbers.Integral):
            return self.getall()[index]
        else:
            msg = "{} class does not support indexing with {}"
            raise TypeError(msg.format(self.__class__.__name__, type(index)))
            
    def __call__(self, **kwargs):
        return self.get(**kwargs)
        
        
    def migrate(self):
        print([(col, self.drop_column(col)) 
        for col in self.description() if col not in self.fields])
        unchanged = []

        for name, dtype in self.columns.items():
            if name in self.description():
                unchanged.append(name)
            else:
                column = name + " " + str(dtype)
                after  = unchanged.pop()
                self.add_column(column, after)
            
