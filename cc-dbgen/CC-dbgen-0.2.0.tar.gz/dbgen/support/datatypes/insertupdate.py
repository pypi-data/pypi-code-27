#External Modules
from typing import List,Dict,Type,TYPE_CHECKING
if TYPE_CHECKING:
    from dbgen.support.datatypes.object import Object

from abc    import abstractmethod
#Internal Modules
from dbgen.support.datatypes.attr       import Attr
from dbgen.support.datatypes.rule       import Block,SBlock,PBlock,SimpleUpsert
from dbgen.support.datatypes.misc       import noIndex,Arg
from dbgen.support.utils                import addQs
################################################################################

class InsertUpdate(object):
    attrs = [] # type: List[Attr]
    @abstractmethod
    def mk_block(self)->List[Block]:
        raise NotImplementedError

class Insert(InsertUpdate):
    """
    Take items in a namespace and store them as attributes on objects
    in the database
    """
    def __init__(self
                ,uni    : Dict[str,'Object']
                ,attrs  : List[Attr]
                ) -> None:
        self.obj = uni[attrs[0].obj]
        assert all([a.obj == self.obj._name for a in attrs])
        self.attrs = attrs
        self.n     = len(attrs)
        self.colnames = [a.name for a in self.attrs]
        self.args  = noIndex(self.colnames)

    def mk_block(self)->List[Block]:
        """

        """
        qs       = ','.join(['%s']*self.n)
        name     = 'insert_%s_%s'%(self.obj._name,'-'.join(self.colnames))
        text     = 'INSERT INTO %s (%s) VALUES (%s)'%(self.obj._name
                                                   ,','.join(self.colnames)
                                                   ,qs)
        dup      = ' ON DUPLICATE KEY UPDATE {0} = {0}'.format(self.colnames[0])

        return [SqlBlock(name = name
                     ,text = text + dup
                     ,args = self.args)
                ,self.mkSelectBlock()]

    def mkSelectBlock(self)->Block:
        """
        Given any insertion, we can construct a block that queries which ID
        """
        where    = addQs([str(a) for a in self.attrs],' AND ')
        fmt_args = [','.join(map(str,self.obj._pks)),self.obj._name,where]

        return SqlBlock(name = 'select_'+self.obj._name  # type: ignore
                     ,text = 'SELECT {0} FROM {1} WHERE {2}'.format(*fmt_args)
                     ,args = self.args)


class Update(InsertUpdate):
    """
    Update attributes of an object
    """
    def __init__(self
                ,uni   : Dict[str,'Object']
                ,attrs : List[Attr]
                ) -> None:
        self.obj = uni[attrs[0].obj]                        # type: ignore
        assert all([a.obj == self.obj._name for a in attrs]) # type: ignore
        self.attrs = attrs

    def mk_block(self)->List[Block]:
        colnames = [a.name for a in self.attrs]
        pk_cols  = [a.name for a in self.obj._pks]  # type: ignore
        name     = 'update_%s_%s'%(self.obj._name,','.join(colnames))   # type: ignore
        setstr   = addQs(colnames,',')
        where    = addQs(pk_cols,' AND ')
        text     = 'UPDATE %s SET %s WHERE %s'%(self.obj._name,setstr,where)   # type: ignore
        args = noIndex(colnames+pk_cols)
        return [SqlBlock(name = name
                    ,text = text
                    ,args = args)]

class InsertFK(InsertUpdate):
    def __init__(self
                ,uni      : Dict[str,'Object']
                ,ins_cols : List[Attr]
                ,fk_tab   : Type['Object']
                ) -> None:
        self.uni      = uni
        self.ins_cols = ins_cols
        self.fk_tab   = fk_tab

    def mk_block(self)->List[Block]:

        ins_obj = self.uni[self.ins_cols[0].obj]
        cols    = [x.name for x in self.ins_cols]
        return SimpleUpsert(ins_obj._mkTable(),cols,self.fk_tab._mkTable()) # type: ignore
        # fk      = [f for f in self.fk_tab._fks if f._to is ins_obj][0]   # type: ignore
        # fk_cols = fk.from_attr
        # pk_cols = fk.to_attr
        # n       = len(fk_cols)
        # insert_block = Insert(self.uni,self.ins_cols).mk_block()[0]
        #
        # where    = addQs(map(str,self.ins_cols),' AND ')                # type: ignore
        # fmt_args = [','.join(map(str,pk_cols)),ins_obj._name,where]     # type: ignore
        #
        #
        # get_id_block = SqlBlock(text = 'SELECT {0} FROM {1} WHERE {2}'.format(*fmt_args)
        #                     ,name = 'select_'+self.name
        #                     ,args = insert_block.args)
        #
        # update_block = Update(self.uni,fk_cols).mk_block()[0]
        # update_block.args[:n] = [Arg('select_'+self.name,i) for i in range(n)]
        #
        # return [insert_block, get_id_block, update_block]
