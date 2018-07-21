from datetime import datetime as detym, date as det, time as tym
from collections import OrderedDict
import ast

class DescriptorMeta(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return dict(OrderedDict())
        
    '''Metaclass for model fields'''
    def __new__(meta, clsname, bases, clsdict):
        clsobj = super().__new__(meta, clsname, bases, dict(clsdict))
        return clsobj
        
        
class Descriptor(metaclass=DescriptorMeta):
    def __init__(self, name=None):
        self.name = name
        
    def __set__(self, instance, value):
        msg = 'Expected type {}, got type {}'
        assert isinstance(value, self.type), msg.format(self.type, type(value))
        instance.__dict__[self.name] = value
        

class INTEGER(Descriptor):
    type = int
    def __init__(self, maxlen=None):
        self.maxlen = maxlen
        
    def __str__(self):
        if self.maxlen:
            return "INTEGER(%s)"%self.maxlen
        else:
            return "INTEGER"
            
    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError('Expected %s, got %s'%(self.type,type(value)))

        if value < 0:
            raise ValueError("Integer Value should be greater than zero")

        super().__set__(instance, value)
        
                
class String(Descriptor):
    type = str
    def __init__(self, maxlen, default=None, null=True):
        self.maxlen = maxlen
        self.default = default
        self.null = null

    def __str__(self):
        self.type_name = self.__class__.__name__.upper()

        if not self.default and self.null:
            return "%s(%s)"%(self.type_name, self.maxlen)
            
        elif self.default and self.null:
            return "%s(%s) DEFAULT '%s'"%(self.type_name, self.maxlen, self.default)
            
        elif self.default and not self.null:
            return "%s(%s) DEFAULT '%s' NOT NULL"%(self.type_name, self.maxlen, self.default)
        else:
            return "%s NOT NULL"%(self.type_name)

class CHAR(String):
    pass
    
class VARCHAR(String):
    pass
        
        
class TEXT(String):
    def __init__(self, default=None, null=True):
        self.default = default
        self.null = null
        
    def __str__(self):
        self.type_name = self.__class__.__name__.upper()
        if self.default == None and self.null==True:
            return "%s"%(self.type_name)
               
        elif self.default  and self.null==True:
            return "%s DEFAULT '%s'"%(self.type_name, self.default)
            
        elif self.default and not self.null:
            return "%s DEFAULT '%s' NOT NULL"%(self.type_name, self.default)
        
        else:
            return "%s NOT NULL"%(self.type_name)


class ENUM(String):
    def __init__(self, values):
        assert isinstance(values, (tuple, list)), "Expected a tuple/list"
        self.values = values
        
    def __str__(self):
        return "ENUM%s"%str(tuple(self.values))
        
class DATE(Descriptor):
    type = det
    def __init__(self, default=None):
        self.default = default
    
    def __str__(self):
        return "DATE default '%s'"%self.default if self.default else "DATE"
        
    def __set__(self, instance, value):
        if not value:
            value = detym.now().strftime('%Y-%m-%d')

        if isinstance(value, str):
            super().__set__(instance, detym.strptime(value, '%Y-%m-%d').date())
        elif isinstance(value, det):
            super().__set__(instance, value)
        
        
class TIME(Descriptor):
    type = tym
    def __init__(self, default=None):
        self.default = default
    
    def __str__(self):
        return "TIME default '%s'"%self.default if self.default else "TIME"
        
    def __set__(self, instance, value):
        if not value:
            value = detym.now().strftime('%H:%M:%S')

        if isinstance(value, str):
            super().__set__(instance, detym.strptime(value, '%H:%M:%S').time())
        elif isinstance(value, tym):
            super().__set__(instance, value)
    

class DATETIME(Descriptor):
    type = detym
    
    def __init__(self, default=None):
        self.default = default
    
    def __str__(self):
        return "DATETIME %s"%self.default if self.default else "DATETIME"
        
    def __set__(self, instance, value):
        if not value:
            value = detym.now().strftime('%Y-%m-%d %H:%M:%S')
            
        if isinstance(value, str):
            super().__set__(instance, detym.strptime(value, '%Y-%m-%d %H:%M:%S'))
        elif isinstance(value, detym):
            super().__set__(instance, value)


class FULLAGEFIELD(Descriptor):
    type = tuple

    def __str__(self):
        return "VARCHAR(50)"

    def __set__(self, instance, value):
        if isinstance(value, str):
            try:
                value = ast.literal_eval(value)
            except:
                raise ValueError('Invalid data type, should be a tuple')
            assert len(value)==2, 'tuple length should be 2'
            super().__set__(instance, value)

        elif isinstance(value, tuple):
            assert len(value)==2, 'tuple length should be 2'
            super().__set__(instance, value)


class AGEFIELD(Descriptor):
    type = tuple

    def __str__(self):
        return "VARCHAR(50)"

    def __set__(self, instance, value):
        if isinstance(value, str):
            try:
                value = ast.literal_eval(value)
            except:
                raise ValueError('Invalid data type, should be a tuple')

            assert len(value)==3, 'tuple length should be 3'
            super().__set__(instance, value)

        elif isinstance(value, tuple):
            assert len(value)==3, 'tuple length should be 3'
            super().__set__(instance, value)


class LONGTEXT(String):
    def __init__(self, default=None, null=True):
        self.default = default
        self.null = null
        
    def __str__(self):
        self.type_name = self.__class__.__name__.upper()
        if self.default == None and self.null==True:
            return "%s"%(self.type_name)
               
        elif self.default  and self.null==True:
            return "%s DEFAULT '%s'"%(self.type_name, self.default)
            
        elif self.default and not self.null:
            return "%s DEFAULT '%s' NOT NULL"%(self.type_name, self.default)
        
        else:
            return "%s NOT NULL"%(self.type_name)


class BLOB(Descriptor):
    type = bytes

    def __str__(self):
        return "BLOB"

class FLOAT(Descriptor):
    type = float

    def __str__(self):
        return "FLOAT"

class BOOLEAN(Descriptor):
    type = bool

    def __str__(self):
        return "BOOLEAN"
          

class DECIMAL(Descriptor):
    import decimal
    type = decimal.Decimal

    def __str__(self):
        return "DECIMAL"

    def __get__(self, instance, val):
        try:
            return decimal.Decimal(instance.__dict__[self.name])
        except:
            return float(instance.__dict__[self.name])



class DOUBLE(FLOAT):
    def __get__(self, instance, val):
        return float("%.2f"%instance.__dict__[self.name])


