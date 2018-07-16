#External
from typing import Dict,Any,Tuple,Union,Set,List,Optional
from networkx    import DiGraph                                 # type: ignore
from networkx.algorithms.dag          import descendants        # type: ignore
from networkx.algorithms.simple_paths import all_simple_paths   # type: ignore

# Internal
from dbgen.support.datatypes.sqltypes     import SQLType
from dbgen.support.datatypes.attr         import Attr
from dbgen.support.datatypes.table        import Table,FK as OldFK
from dbgen.support.datatypes.constraint   import EQ,NE,LT,GT,NULL,Constraint
from dbgen.support.datatypes.insertupdate import Insert,Update,InsertFK,InsertUpdate
from dbgen.support.datatypes.rule         import Block,Rename
from dbgen.scripts.Pure.Misc.identity     import identity
from dbgen.support.datatypes.misc         import Arg

from dbgen.core.lists import flatten

#############################################################################
# Constants
#----------
class NotNull(object): pass
NOTNULL = NotNull()
class Unique(object): pass
UNIQUE = Unique()

class DEFAULT(object):
    def __init__(self,val:Any)->None:
        self.val = val
################################################################################
# Main Class
#------------


class Object(object):
    """
    Superclass for user-defined objects (which correspond to DB tables)

    _parents
        -- SUFFICIENT and NECCESARY objects needed to specify an instance
          (e.g. for 'Atom', 'Struct' and 'Element' (+ 'atom_id')
           are both necessary, but Struct+atom_id are sufficient.
    _components
        --

    <anything else>
        -- normal attribute (doesn't start with '_')
        -- should provide a SQLType followed by other information, if necessary

    """
    universe = {}    # type: Dict[str,Object]
    todo     = set() # type: Set[str]
    _parents = []    # type: List[Object]
    _name    = ''
    _pks     = []    # type: List[Attr]
    deleted  = Attr('deleted')

    def __init__(self,alias:Optional[str]=None)->None:
        if alias is None:
            alias = self._name # type: ignore
        self._alias=alias # only defining property of an INSTANCE of a class

    @classmethod
    def _process_parent(cls,par:type)->None:
        new_pks = [Attr(par._name+'_'+k.name,pk=True,obj=cls._name)  # type: ignore
                        for k in par._pks]         # type: ignore
        cls._pks.extend(new_pks)                   # type: ignore
        cls._fks.append(FK(new_pks,par,par._pks))  # type: ignore
        for p in new_pks: cls._addAttr(p)
    @classmethod
    def _process_component(cls,comp:type)->None:
        new_fks = [Attr(comp._name+'_'+k.name,obj=cls._name)  # type: ignore
                        for k in comp._pks]         # type: ignore
        for f in new_fks: cls._addAttr(f)
        cls._fks.append(FK(new_fks,comp,comp._pks))  # type: ignore

    @classmethod
    def _init_vars(cls)->None:
        """
        Initialize the parents,components,many_to_one,desc,pks, and fks fields
        Also take all attributes and make them fields of the class
        """
        import pdb;pdb.set_trace()
        cd               = cls.__dict__
        name             = cls.__name__.lower()  # type: ignore
        cls._parents     = cd.get('_parents',[])                     # type: ignore
        cls._components  = cd.get('_components',[])                  # type: ignore
        cls._many_to_one = cd.get('_many_to_one',False)              # type: ignore
        cls._desc        = cls.__dict__.get('__doc__','(No description)') # type: ignore

        cls._pks,cls._fks,cls._attrs = [],[],{}  # type: ignore

        new_attrs  = [cls._mkAttr(k,v)       # type: ignore
                      for k,v in cd.items()
                      if k[0]!='_'] + [Attr('deleted',obj=name,default=0)]

        has_indep_pk = (not cls._parents) or cls._many_to_one # type: ignore
        if has_indep_pk:
            pk = Attr(name+'_id',pk=True,auto=True,obj=name)
            cls._pks = [pk]          # type: ignore
            new_attrs.append(pk)

        for a in new_attrs:
            cls._addAttr(a)

    @classmethod
    def _addAttr(cls,attr:Attr)->None:
        if attr.name in cls._attrs:         # type: ignore
            print('Cannot re-add '+str(attr))
        else:
            assert(attr.obj == cls._name)  # type: ignore
            cls._attrs[attr.name] = attr   # type: ignore
            setattr(cls,attr.name,attr)

    @classmethod
    def _mkAttr(cls
               ,name : str
               ,data : Union[SQLType,Tuple]
               ) -> Attr:
        """
        Take user input and construct and Attr
        """
        if isinstance(data,tuple):
            types = (SQLType,NotNull,DEFAULT,Unique)
            assert all([isinstance(x,types) for x in data])
            dtype = [d for d in data if isinstance(d,SQLType)][0]
            default = [d.val for d in data if isinstance(d,DEFAULT)]
            return Attr(name
                       ,dtype   = dtype
                       ,nnull   = NOTNULL in data
                       ,uniq    = UNIQUE in data
                       ,obj     = cls._name                         # type: ignore
                       ,default = default[0] if default else None)
        else:
            err = 'Expected field %s to contain dtype, but instead found %s %s'
            assert isinstance(data,SQLType),err%(name,data,type(data))
            return Attr(name,dtype=data,obj=cls._name) # type: ignore

    @classmethod
    def _mkView(cls
               ,attr  : List[Union['Object',Attr]]
               ,const : List[Constraint]            = []
               ,nn    : List['Object']              = []
               ) -> 'View':
        return View(cls.universe,attr,const,nn)

    @classmethod
    def _get_unsafe(cls,colname:str)->Attr:
        return cls._attrs[colname] # type: ignore

    @classmethod
    def insert(cls,cols:Optional[List[str]] = None)->InsertUpdate:
        if cols is None:
            return Insert(cls.universe,cls._pks) # type: ignore
        else:
            try:
                return Insert(cls.universe,[cls._get_unsafe(x) for x in cols])
            except ValueError as e:
                print(e)
                import pdb;pdb.set_trace()
                raise ValueError
    @classmethod
    def select(cls
              ,attrs  : Optional[List[str]] = None
              ) -> List[Attr]:
        if attrs is None:
            return cls._pks # type: ignore
        else:
            return list(map(cls._get_unsafe,attrs))

    @classmethod
    def update(cls,attrs : List[str])->Update:
        return Update(cls.universe,[cls._get_unsafe(x) for x in attrs])

    @classmethod
    def update_component(cls
                        ,attrs   : List[Attr]
                        ) -> InsertUpdate:
        """
        Need to control the INSERT, get PK, update PK process
        """
        return InsertFK(cls.universe,attrs,cls)

    @classmethod
    def _mkTable(cls)->Table:
        return Table(name = cls._name,desc = cls._desc                       # type: ignore
                    ,cols = [c._mkCol() for c in cls._attrs.values()]        # type: ignore
                    ,fks  = [fk.to_old_style() for fk in cls._fks])          # type: ignore
    @classmethod
    def _hasnt(cls,comp:type)->Constraint:
        for fk in cls._fks: # type: ignore
            if fk._to == comp:
                return NULL(fk.from_attr[0])
        raise ValueError

def new_model(name:str)->Object:
    """
    Create a new model
    """
    class New(Object):
        _modelname = name

        def __init_subclass__(cls      : type
                             ,**kwargs : dict
                             ) -> None:
            """
            Upgrade a user-defined class given the state of the universe
            """
            if kwargs:
                raise ValueError('kwargs? '+str(kwargs))
            else:
                cls._init_subclass() # type: ignore

        @classmethod
        def _init_subclass(cls) -> None:
            uni  = cls.universe
            todo = cls.todo
            name = cls.__name__.lower()

            cls._name = name; cls._alias = name  # type: ignore
            if name in uni:
                print('Warning: this class (%s) was already defined for this universe'%name)
                return None # No repeats allowed

            cls._init_vars() # type: ignore


            for p in cls._parents: # type: ignore
                assert isinstance(p,(type,str)), type(p) # basic integrity check

                # Handle this if it's a real definition or known string
                #------------------------------------------------------------
                if isinstance(p,type) or p.lower() in uni:
                    if isinstance(p,type):
                        parent = p
                    else:
                        parent = uni[p.lower()]

                    # Acknowledge only after all of its parents have been provided
                    #------------------------------------------------------------
                    if all([isinstance(pp,type) for pp in parent._parents]): # type: ignore
                        cls._process_parent(parent)                      # type: ignore
                else:
                    todo.add(p.lower())

            for c in cls._components: # type: ignore
                assert isinstance(c,(type,str)), type(c) # basic integrity check

                # Handle this if it's a real definition rather or known string
                #------------------------------------------------------------
                if isinstance(c,type) or c.lower() in uni:
                    if isinstance(c,type):
                        comp = c
                    else:
                        parent = uni[c.lower()]

                    # Acknowledge only after all of its parents have been provided
                    #------------------------------------------------------------
                    if all([isinstance(pp,type) for pp in cls._parents]):
                        cls._process_component(comp)
                else:
                    assert isinstance(p,str)
                    todo.add(p.lower())

            # Wrap things up after we're done
            #--------------------------------
            uni[name] = cls # type: ignore
            if name in todo:
                # UPGRADE EVERYTHING ELSE IN UNIVERSE THAT POINTS TO THIS VIA STR
                todo.remove(name)

    return New # type: ignore



#mike = new_model('mike') # type: Any

################################################################################
# HELPER CLASSes
#---------------
class FK(object):
    """
    A Foreign Key in the language of Objects/Attributes is a pair of lists of
    Attributes, each having equal length but referring to different Objects
    """
    def __init__(self
                ,from_attr : List['Attr']
                ,_to       : Object
                ,to_attr   : List['Attr']
                ) -> None:
        # Validate
        #---------
        err1 = 'FK args not of equal length: %s %s'
        assert len(from_attr) == len(to_attr), err1%(from_attr,to_attr)
        err2 = 'FK args share the same object: %s'
        assert from_attr[0].obj != to_attr[0].obj, err2%from_attr[0].obj

        # Store Fields
        #-------------
        self.from_attr = from_attr
        self._to       = _to
        self.to_attr   = to_attr

    def __str__(self)->str:
        return self.zipped()
    def __repr__(self)->str:
        return str(self)

    def zipped(self) -> str:
        z = zip(self.from_attr,self.to_attr)
        return ' AND '.join(['%s = %s'%(f,t) for f,t in z])

    def to_old_style(self) -> OldFK:
        if self.to_attr[0].obj is None:
            raise ValueError
        else:
            return OldFK([a.name for a in self.from_attr]
                         ,self._to._name # type: ignore
                         ,[a.name for a in self.to_attr])

    def rename(self)->List[Block]:
        return [Rename(y.name,x.name)
                    for x,y in zip(self.from_attr,self.to_attr)]

################################################################################

class Join(object):
    """
    JOIN <A> AS <B> ON <C> = <D> AND ...
    """
    def __init__(self
                ,obj  : Object
                ,fk   : FK
                ,kind : str     = 'INNER'
                ) -> None:
        self.obj  = obj
        self.fk   = fk
        self.kind = kind
        self.direction = True # flip this to change direction of join

    # Basic Methods
    #--------------
    def __str__(self) -> str:
        join   = '%s JOIN'%self.kind
        to_obj = self.fk._to if self.direction else self.obj
        if to_obj is None:
            raise ValueError
        else:
            tab    = '%s AS %s'%(to_obj._name,to_obj._alias)
            return '\n\t%s %s \n\t\tON %s'%(join,tab,self.fk.zipped())

    def flip(self)->None:
        self.direction = not self.direction



class From(object):
    """
    FROM clause
    """
    def __init__(self
                ,obj   : Object
                ,joins : List[Join] = []
                ) -> None:
        self.obj   = obj
        self.joins = joins
        self.allobj = [obj]+[j.obj for j in joins]
        assert len(set(self.allobj)) == len(joins)+1

    # Basic Methods
    #--------------
    def __str__(self) -> str:
        tab = ' %s AS %s '%(self.obj._name,self.obj._alias) # type: ignore
        return 'FROM ' + tab + ''.join(['\n%s'%j for j in self.joins])

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self,other : object)->bool:
        if isinstance(other,Object):
            return self.__dict__ == other.__dict__
        else:
            return False



##############################################################################
class View(object):
    """
    A query of sorts
    """
    def __init__(self
                ,uni         : Dict[str,Object]
                ,attrs       : List[Union[Attr,Object]]
                ,constraints : List[Constraint]         = []
                ,mbNull      : List[Object]               = []
                ) -> None:

        self.uni     = uni
        self.objects = list(uni.values())
        self.graph   = self.mk_graph()

        allobj = sorted(set([uni[x.obj] if isinstance(x,Attr) else x
                             for x in attrs]))
        self.allobj = allobj

        pk_attrs = flatten([o._pks for o in allobj])

        self.attrs = pk_attrs + [x for x in attrs if isinstance(x,Attr)]
        self.constraints = constraints + [o.deleted==0 for o in allobj]
        c_attrs = flatten([list(c.attrs()) for c in constraints])
        all_attr = self.attrs + c_attrs

        self._from = self.mkFrom(all_attr)

        for j in self._from.joins:
            if j.fk._to in mbNull:
                j.kind = "LEFT"


    def __str__(self)->str:
        cols   = '\n\t,'.join([str(a) for a in self.attrs])
        consts = '\n\tAND '.join([str(c) for c in self.constraints])

        return 'SELECT %s\n%s\nWHERE %s'%(cols,self._from,consts or '1')


    def mkFrom(self,attrs:List[Attr])->From:
        """
        Construct a FROM clause that joins the right tables in order to get
        access to a set of attributes mentioned by some query
        """
        objects  = set([a.obj for a in attrs])

        found    = False
        for obj in objects:
            desc = descendants(self.graph,obj)
            if all([o in desc for o in objects if o is not obj]):
                found = True
                first = obj

        if not found:
            import pdb;pdb.set_trace()
            raise ValueError('You screwed up')

        joins = []
        for o in objects:
            if o != first:
                paths = self.path(first,o)
                lp    = len(paths)

                if lp != 1:
                    print("Warning, %d paths found between %s and %s"%(lp,first,o))
                path = paths[0]
                assert path[0] == first
                curr_obj = self.uni[first] # initialize with this

                for s in path[1:]: # first element = first._name
                    next_obj = self.uni[s]
                    fk = self.get_fk(curr_obj,next_obj)
                    joins.append(Join(next_obj,fk))
                    curr_obj = next_obj

        return From(self.uni[first],joins)

    def mk_graph(self)->DiGraph:
        """
        Given parent/component relationships between objects, create a Directed
        Graph that captures the possible flows of information.
        """
        G = DiGraph()
        G.add_nodes_from([o._name for o in self.objects])    # type: ignore
        for o1 in self.objects:        # type: ignore
            if not o1._many_to_one:     # type: ignore
                for o2 in o1._parents:   # type: ignore
                    G.add_edge(o2._name,o1._name)   # type: ignore
            for o2 in o1._parents + o1._components:   # type: ignore
                    G.add_edge(o1._name,o2._name)    # type: ignore
        return G

    def path(self,o:str,o2:str)->List[List[str]]:
        """
        All possible paths between two objects via FK propagation
        """
        paths = all_simple_paths(self.graph,o,o2)
        return sorted(list(paths),key=len)

    def get_fk(self,o1:Object,o2:Object)->FK:
        """
        Gets a FK between two Objects -- error if more/fewer are found
        """
        fks = [fk for fk in o1._fks if fk._to is o2]  + [fk for fk in o2._fks if fk._to is o1]    # type: ignore
        if len(fks) != 1:
            raise ValueError('%d many fks between %s and %s: %s'%(len(fks),o1,o2,fks))
        else:
            return fks[0]
