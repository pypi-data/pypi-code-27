# External Modules
from typing import Optional,Any,List
from copy import deepcopy
# Internal Modules
from dbgen.support.datatypes.sqltypes   import SQLType,Int
from dbgen.support.datatypes.table      import Col
from dbgen.support.datatypes.constraint import EQ,NE,LT,GT

"""
Defines the Attr (Attribute) class, which have overloaded operations so that
they can be used as part of an EDSL.
"""

###############################################################################
class Attr(object):
    """
    A property of an object. Corresponds to a column of a table in a database.

    name  - column name (also in Python the attr can be accessed via "Obj.name")
    dtype - SQL data type
    nnull - whether or not a NOT NULL constraint should be placed on property
    ind   - whether or not to index the column in DB
    default - SQL default when initialize new objects in DB
    uniq    - whether this column is part of a UNIQUE constraint for its object
    auto    - SQL's AUTOINCREMENT
    pk      - whether this column is part of a PRIMARY KEY constraint
    obj     - the name of the object that this attribute is associated with
    """
    def __init__(self
                ,name    : str
                ,dtype   : SQLType       = Int()
                ,nnull   : bool          = False
                ,ind     : bool          = False
                ,default : Optional[Any] = None
                ,uniq    : bool          = False
                ,auto    : bool          = False
                ,pk      : bool          = False
                ,obj     : str           = '???'
                ) -> None :

        self.name    = name
        self.dtype   = dtype
        self.nnull   = nnull
        self.ind     = ind
        self.default = default
        self.uniq    = uniq
        self.auto    = auto
        self.pk      = pk
        self.obj     = obj

    # Basic
    #------

    def __str__(self) -> str:
        return '%s.%s'%(self.obj,self.name)

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self,other : object)->EQ: # type: ignore
        return EQ(self,other)

    def __ne__(self,other : object)->NE: # type: ignore
        return NE(self,other)

    def __lt__(self,other : object)->LT: # type: ignore
        return LT(self,other)

    def __gt__(self,other : object)->GT: # type: ignore
        return GT(self,other)

    def __hash__(self)->int:
        return hash(self.name)

    # Other methods
    #--------------
    def _mkCol(self)->Col:
        return Col(name    = self.name
                  ,typ     = self.dtype
                  ,nn      = self.nnull
                  ,uniq    = self.uniq
                  ,ind     = self.ind
                  ,default = self.default
                  ,auto    = self.auto
                  ,pk      = self.pk)
