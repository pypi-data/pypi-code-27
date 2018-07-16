from typing import List,FrozenSet,Dict
from dbgen.support.datatypes.relation   import Relation
from dbgen.support.datatypes.func       import Func
from dbgen.support.datatypes.dbg        import DBG
from dbgen.support.datatypes.misc       import ConnectInfo

################################################################################
class Model(object):
    def __init__(self
                ,schema    : Dict[str,type]
                ,relations : List[Relation]
                ) -> None:
        self.schema    = schema
        self.relations = relations
        self.objects   = schema.values()

    def createDBG(self)->DBG:
        tables = [o._mkTable() for o in self.objects]  # type: ignore
        rules  = [r.mk_rule() for r in self.relations]
        return DBG(tables=tables,rules=rules)

    def run(self
           ,reset   : bool      = False
           ,catalog : bool      = False
           ,add     : bool      = False
           ,xclude  : str       = ''
           ,only    : str       = ''
           ) -> None:
        db = ConnectInfo()

        onl = set(only.split())

        x  = set() if catalog else {'catalog'}
        self.createDBG().run_all(db
                                ,reset    = reset
                                ,xclude   = x | set(xclude.split())
                                ,add      = add
                                ,parallel = False
                                ,only     = onl)
