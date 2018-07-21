#! usr/bin/env python3
from collections import ChainMap
import models
import csv
import os
import ast
from fields import *

ROOT_WINDOW = None

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
        if not hasattr(Base, 'rpcproxy'):
            raise AttributeError("Configure proxy client for Base with approprate host & port "
                "Forexample:\n\nfrom rpcdb import Base, Proxy\nBase.rpcproxy=Proxy('127.0.0.1', 17000)")
        
        self.proxy = Base.rpcproxy
        if hasattr(Base, 'ast_convert'):
            self.ast_convert = Base.ast_convert
        else:
            self.ast_convert = []

        if not hasattr(self, 'ignore_on_save'):
            self.ignore_on_save = []

        for name, value in kwargs.items():
            if name in self.fields:
                setattr(self, name, value)

        if not hasattr(self, 'debug'):
            self.debug = False

        self.mapper = Mapper().maps

        global ROOT_WINDOW
        if not ROOT_WINDOW:
            Base.App = Tk()
            ROOT_WINDOW = Base.App
        else:
            Base.App = ROOT_WINDOW

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
            result = self.proxy.execute(
                "SELECT * FROM %s WHERE %s='%s'"%(self.table, self.pk, ID))

            return len(result) > 0
        except AttributeError:
            return False
        
    def save(self):
        keys = ", ".join(list(self.kwargs.keys()))
        values = tuple(list(self.kwargs.values()))
        
        SQL = """INSERT INTO %s (%s) VALUES(""" % (self.table, keys)
        SQL += """ "%s",""" * len(values) % (values)
        SQL = SQL[:-1] + ")"
        
        if not self.exists():
            return self.proxy.save(SQL) 
        else:
            return "Already exists..."
    
    def description(self):
        sql = "DESCRIBE %s"%self.table
        return self.proxy.description(sql)
        
        
    def update(self):
        if not self.exists():
            return "This record does not exist. Can only update saved records"

        keys = ", ".join(list(self.kwargs.keys()))
        values = tuple(list(self.kwargs.values()))
        
        SQL = """UPDATE {} SET """.format(self.table)
        for key, value in self.kwargs.items():
            SQL += """ %s = "%s" ,""" % (key, value)

        SQL = SQL[:-1] + """ WHERE {} = "{}" """.format(self.pk, self.kwargs.get(self.pk))
        if self.debug:
            print(SQL)
        return self.proxy.update(SQL)
        
        
    def delete(self):
        SQL = "DELETE FROM %s WHERE %s= '%s' "%(self.table, self.pk, 
            self.kwargs.get(self.pk))

        if self.debug:
            print(SQL)
        return self.proxy.delete(SQL)
        
        
    def drop_column(self, column):
        sql ="ALTER TABLE %s DROP COLUMN %s"%(self.table, column)
        if self.debug:
            print(sql)
        return self.proxy.execute(sql)
        
    def add_column(self, column, after):
        sql ="ALTER TABLE {} ADD COLUMN {} AFTER {}"
        sql = sql.format(self.table, column, after)
        if self.debug:
            print(sql)
        self.proxy.execute(sql)
        
        
    def alter_column(self, old_column, new_column):
        sql ="ALTER TABLE {} CHANGE COLUMN {} {}"
        sql = sql.format(self.table, old_column, new_column)
        if self.debug:
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
    
    def write_to_csv(self):
        header_row = self.description()
        data = self.get()
        filename = self.__class__.__name__ + ".csv"
        
        with open(filename, 'w', newline="") as in_file:
            writer = csv.writer(in_file)
            writer.writerow(header_row)    
            for row in data:
                writer.writerow(row)
        if self.debug:
            print('Saved the data to: ', filename) 
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
        if self.debug:
            print([(col, self.drop_column(col)) 
            for col in self.description() if col not in self.fields])
        unchanged = []

        for name, dtype in self.columns.items():
            if name in self.description():
                unchanged.append(name)
            else:
                column = name + " " + str(dtype)
                try:
                    after  = unchanged.pop()
                    self.add_column(column, after)
                except IndexError:
                    pass

    def onSave(self):
        data = {k:v.get() for k, v in self.entries.items()
        if k not in self.ignore_on_save}
        instance = self.__class__(**data)

        msg=instance.save()
        if self.debug:
            print("Saving the record...")
            print(msg)

        msg2 = instance.update()
        if self.debug:
            print("Trying to update the record if it exists...")
            print(msg2)
        

    def onDelete(self):
        msg = self.delete()
        if self.debug:
            print(msg)


    def onFind(self):
        pk = self.pk
        value = self.entries[pk].get()
        sql = "SELECT * FROM %s WHERE %s='%s'"%(self.table, pk, value)
        data = self.proxy.get(sql, as_dict=True, only_one=True)
        self.show_record(data)

    def onClear(self):
        for ent in self.entries.values():
            ent.delete(0, 'end')

    def show_record(self, data={}):
        for name, val in data.items():
            try:
                self.entries[name].delete(0, 'end')
                self.entries[name].insert(0, val)
            except:
                pass


    def widget(self, parent, font="Consolas 13", relief='raised', bd=2, 
        sticky='ew', label_fg = 'black', label_bg='SystemButtonFace'):
        
        class MyFrame(Frame):
            def __init__(self, parent, master):
                super(MyFrame, self).__init__(parent)
                self.pack(fill=BOTH, expand=1)
                self.configure(padx=5, pady=5)

                btns = ("Save",  "Find", "Clear", "Delete")

                title = Label(self, text='%s Form'%master.__class__.__name__)
                title.config(font='Consolas 18 bold', fg='green')
                title.pack(fill=X)

                btnframe = Frame(self)
                btnframe.pack(fill=X)

                for btn in btns:
                    style = ttk.Style()
                    style.theme_use('clam')
                    style.configure("T.TButton", background='powderblue')
                    b = ttk.Button(btnframe, text=btn, style='T.TButton')
                    b['command'] = getattr(master, 'on%s'%btn)
                    b.pack(side='left', padx=4, pady=4)

        def make_form(frame):
            self.entries = OrderedDict()

            lfrm = Frame(frame, padx=4,relief=relief, bd=bd, pady=4)
            lfrm.pack(padx=4, pady=4, anchor='w')

            for index, field in enumerate(self.fields, 1):
                field_type = type(self.columns[field]).__name__
                widget= self.mapper[field_type]
                label = ttk.Label(lfrm, text=field.upper().replace("_", " "))
                label.config(font='Consolas 12', background=label_bg, foreground=label_fg)
                label.grid(row=index, column=0, sticky='e')

                entry = widget(lfrm)
                entry.grid(row=index, column=1, sticky=sticky, pady=4)
                entry.configure(font=font)
                
                try:
                    values= self.columns.get(field).values
                    entry.configure(values=values)
                except:
                    pass

            
                self.entries[field] =  entry

        frame = MyFrame(parent, self)
        make_form(frame)
        return frame

    def show(self):
        Base.App.withdraw()
        top = Toplevel(Base.App)
        top.protocol('WM_DELETE_WINDOW', Base.App.destroy)
        top.focus()
        top.grab_set()
        top.title(self.__class__.__name__)
        Base.App.title(self.__class__.__name__)

        empframe = self.widget(top)
        empframe.grid()
        self.show_record()
        self.root.mainloop()

