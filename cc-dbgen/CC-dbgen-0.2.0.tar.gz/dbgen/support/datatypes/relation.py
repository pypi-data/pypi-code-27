#External Modules
from typing import Callable,List,Optional,Union,Dict
#Internal Modules
from dbgen.support.datatypes.object         import View
from dbgen.support.datatypes.insertupdate   import InsertUpdate

from dbgen.support.datatypes.rule       import Rule,Plan,Const,PBlock,Block
from dbgen.support.datatypes.misc       import Arg
from dbgen.core.lists                   import flatten


Actions = List[Union[PBlock,List[PBlock]
              ,Block,List[Block]
              ,InsertUpdate,List[InsertUpdate]]]
Action = Union[PBlock,Block,InsertUpdate]
################################################################################

class Relation(object):
    """
    Relate attributes of objects via triples of:
    -select:  Extracting info from the current state of the world
    -inserts: putting information back into the DB
    """
    def __init__(self
                ,name    : str
                ,view    : Optional[View] = None
                ,actions : Actions   = []
                ,consts  : Dict[str,Const] = {}
                ) -> None:
        self.name    = name
        self.view    = view
        self.uni     = view.uni if view else {}
        self.consts  = consts

        # Take mixed singles + lists and make one list
        #---------------------------------------------
        acts = [] # type: List[Action]
        for a in actions:
            if isinstance(a,list):
                acts.extend(a)
            else:
                acts.append(a)
        self.actions = acts

    def mk_rule(self)->Rule:
        """

        """

        # Scenario: we want to insert into a table that is not mentioned in FROM
        # but is related by a FK (so we need identity "job_id = job_job_id")
        extra_fks = []
        if self.view:
            for o in self.view.allobj:
                if o not in self.view._from.allobj:
                    # This Object was not mentioned in FROM clause
                    # Search for any FKs linking this Object to any Object in FROM
                    for o2 in self.view._from.allobj:
                        try:
                            fk = self.view.get_fk(o,o2)
                            extra_fks.append(fk)
                        except ValueError:
                            pass

        # Need to include tempfuncs that capture equality across FKs
        if self.view:
            join_tfs = [j.fk.rename() for j in self.view._from.joins]
            xtra_tfs = [fk.rename() for fk in extra_fks]
            self.actions.extend(flatten(join_tfs)+flatten(xtra_tfs))

        blocks = [] # type: List[Block]
        for a in self.actions:
            if isinstance(a,Block):
                blocks.append(a)
            elif isinstance(a,InsertUpdate):
                blocks.extend(a.mk_block())

        return Rule(name     = self.name
                   ,query    = str(self.view) if self.view else None
                   ,plan     = Plan(blocks = blocks
                                   ,consts = self.consts))
