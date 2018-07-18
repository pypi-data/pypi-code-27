# External Modules
from typing          import Optional,List,Dict,Any,Callable,Set
from abc             import abstractmethod
from time            import time
from pprint          import pformat
from multiprocessing import Pool,cpu_count
from traceback       import format_exc
from decimal         import Decimal
from tqdm            import tqdm                       # type: ignore
from sqlparse        import format as sql_format       # type: ignore
from networkx        import DiGraph                    # type: ignore

# Internal Modules
from dbgen.core.lists   import flatten,concat_map
from dbgen.core.parsing import btw
from dbgen.core.misc    import identity
from dbgen.core.numeric import safe_div

from dbgen.support.sqlparsing         import parse_dependencies
from dbgen.support.datatypes.table    import Table
from dbgen.support.datatypes.func     import Func
from dbgen.support.datatypes.misc     import ExternalError,Arg,noIndex
from dbgen.support.utils              import (sqlexecute,sqlselect,mkInsCmd,sqlite_execute
                                             ,namespaceCmd,func_to_ind,sqlite_select
                                             ,handle_to_ind,ConnectInfo,select_dict
                                             ,sqlexecutemany,addQs,topsort_with_dict)
#########################################################################################
################################################################################
class Const(object):
    """
    Embed a constant value of any type into the namespace for a given rule.
    """
    def __init__(self,val:Any)->None:
        self.val = val
    def __str__(self)->str:
        return pformat(self.__dict__)
    def __eq__(self,other : object)->bool:
        return self.__dict__==other.__dict__
    def get_datatype(self)->str:
        return str(self.val.__class__)

    def add_const(self
                 ,sqlite_pth : str
                 ,trans_id   : int
                 ,const_id   : int
                 ,const_name : str
                 ) -> None:
        """
        Add to meta.db
        """
        datatype = self.get_datatype()
        cols     = ['rule_id','const_id','name','datatype','val']
        q        = mkInsCmd('constants',cols,sqlite=True)
        sqlite_execute(sqlite_pth,q,[trans_id,const_id,const_name,datatype,str(self.val)])
################################################################################

class Block(object):
    """
    Either a PBlock or an SBlock
    """
    # Common Properties of all Blocks
    #-------------------------------
    name = ''
    args = []    # type: List[Arg]
    deps = set() # type: Set[str]
    @abstractmethod
    def __init__(self)->None:
        raise NotImplementedError

    @abstractmethod
    def apply(self
             ,curr_dict : Dict[str,Any]
             ,cxn       : Optional[ConnectInfo] = None
             ) -> Any:
        raise NotImplementedError

################################################################################
class SqlBlock(Block):
    """
    SQL executing block
    """
    # Class constants
    #----------------
    valid_types = (int,str,float,list,bytes,Decimal,type(None))
    type_err    = "Arg (%s) BAD DATATYPE %s IN NAMESPACE "
    broad_err   = "Can't broadcast: maxlen = %d, len a = %d (%s)"
    sql_err     = 'SBlock needs a SQL connection'

    def __init__(self
                ,text : str
                ,name : Optional[str] = None
                ,args : List[Arg]     = []
                ,deps : List[str]     = []
                ) -> None:
        assert isinstance(text,str), 'Not str: '+str(text)
        if name is None:
            name = text
        self.text = text
        self.name = name
        self.args = args
        self.deps = set(deps)

        self.is_select = text[:6].lower()=='select'

    def apply(self
             ,curr_dict : Dict[str,Any]
             ,cxn       : Optional[ConnectInfo] = None
             ) -> Any:
        """
        Creates a function which takes in a namespace dictionary and executes its
        block script (possibly using the namespace for inputs). Its result will
        get added to the namespace.
        """
        assert cxn,self.sql_err
        args   = [arg.arg_get(curr_dict) for arg in self.args]
        maxlen = 1

        for a in args:
            assert isinstance(a,self.valid_types), self.type_err%(a,a.__class__)
            if isinstance(a,list):
                if maxlen != 1: # variable has been set
                    try:
                        assert(len(a) in [1,maxlen]), self.broad_err%(maxlen,len(a),str(a)) # preconditions for broadcasting
                    except:
                        import pdb;pdb.set_trace()
                else:
                    maxlen = len(a)

        def process_arg(x:Any)->list:
            if isinstance(x,list) and len(x)!=maxlen:
                return maxlen*x # broadcast
            elif not isinstance(x,list):
                return  maxlen * [x]
            else:
                return x

        # now all args should be lists of the same length
        broadcasted = [process_arg(x) for x in args]

        binds = list(zip(*broadcasted))

        if self.is_select:
            # we're probably selecting to get a PK, take the first result no matter what
            def app(x:tuple)->List[tuple]:
                    return sqlselect(cxn,self.text,x)[0] # type: ignore

            def mbBox(x:tuple)->Any:
                if len(x)==1: return x[0]
                else: return x
            uniqbinds = list(set(binds))
            try:
                output = {b:mbBox(app(b)) for b in uniqbinds} # type: ignore
            except IndexError:
                    print('failed to find a result after query failed:\n'+self.text)
                    print('binds are : '+pformat(list(zip(self.args,uniqbinds[0]))))
                    import pdb;pdb.set_trace()
                    return []

            return [output.get(x) for x in binds] # type: ignore
        else:
            if len(self.args)==0:
                sqlexecute(cxn,self.text)
            else:
                sqlexecutemany(cxn,self.text,binds)
            return None

# SBlock Shortcuts
#----------------
def PureSQL(strs : List[str])->List[Block]:
    """Execute a series of SQL statements"""
    return [SqlBlock(text=s,name="pure sql #%d"%i) for i,s in enumerate(strs)]

def SimpleInsert(tab:Table,cols:List[str]) -> List[Block]:
    """
    Assume that the insert columns have corresponding variables in the namespace
    """
    assert cols, 'Cannot insert with no columns'
    args     = noIndex(cols)
    qmarks   = ','.join(['%s']*len(cols))
    fmt_args = [tab.name,','.join(cols),qmarks,cols[0]]
    ins = SqlBlock(text = """INSERT INTO {0} ({1}) VALUES ({2})
                            ON DUPLICATE KEY UPDATE {3} = {3}""".format(*fmt_args)
                ,name = 'insert_'+tab.name,args = args) # type: Block

    pk_cols   = [c.name for c in tab.cols if c.pk == True]
    fmt_args2 = [','.join(pk_cols),tab.name,addQs(cols,' AND ')]
    q   = SqlBlock(text="""SELECT {0} FROM {1} WHERE {2}""".format(*fmt_args2)
                ,name = 'select_'+tab.name,args=args,deps=[ins.name]) # type: Block
    u   = Unpack('select_'+tab.name,[tab.name+'_'+c for c in pk_cols])
    return [ins]#,q]+u

def SimpleUpdate(tab:Table,cols:List[str]) -> Block:
    """
    Assume that the insert columns AND primary keys have corresponding variables
    in the namespace
    """
    pk_cols = [c.name for c in tab.cols if c.pk == True]
    args    = noIndex(cols+pk_cols)
    set     = addQs(cols,',')
    where   = addQs(pk_cols,' AND ')

    return SqlBlock(text='UPDATE %s SET %s WHERE %s'%(tab.name,set,where)
                 ,name='update_'+tab.name,args=args)

def SimpleUpsert(ins_tab   : Table
                ,ins_cols  : List[str]
                ,fk_tab    : Table
                ) -> List[Block]:
    """
    Let's say we compute an entity (A) associated with another entity (B).
    - We want to insert the A instance into the A table (if it doesn't exist).
    - We want to record the PK of this A instance an store it as a FK in B table.

    ins_tab   - 'A' table described above
    cols       - properties with which to insert an A instance
    fk_tab    - name of the 'B' table described above

    We assume that:
        - there exists exactly one foreign key from B to A
        - whatever was inserted will uniquely identify an A object (e.g. 'raw'
            for structure, possibly not necessarily the PKs of A)
        - namespace has appropriate column names

    WARNING THIS WILL BE A PROBLEM IF THERE'S A NAMESPACE COLLISION IN KEY NAMES

    SAFER WOULD BE TO MAKE THE 'key' FOR COLUMNS TO BE '<table>.<column>'
    """

    insert_args   = noIndex(ins_cols)
    ins_select    = SimpleInsert(ins_tab,ins_cols)

    ins_pks = [c.name for c in ins_tab.cols if c.pk]
    where  = addQs(ins_cols,' AND ')
    fmt_args1 = [','.join(ins_pks),ins_tab.name,where]
    get_id_block = SqlBlock('SELECT {0} FROM {1} WHERE {2}'.format(*fmt_args1)
                          ,'get_id_'+ins_tab.name,insert_args,[ins_select[0].name])

    fk         = fk_tab.get_fk(ins_tab)
    fk_pks     = [c.name for c in fk_tab.cols if c.pk]
    setvals    = addQs(fk.column,' , ')
    whereagain = addQs(fk_pks,' AND ')
    args       = [Arg(get_id_block.name,i) for i in range(len(fk.column))]
    fmt_args2  = [fk_tab.name,setvals,whereagain]
    args.extend(noIndex(fk_pks))

    update_block = SqlBlock('UPDATE {0} SET {1} WHERE {2}'.format(*fmt_args2)
                         ,'update',args)

    return ins_select + [get_id_block,update_block]

################################################################################
class PyBlock(Block):
    """
    A computational block that executes Python code
    """
    def __init__(self
                ,func : Callable
                ,name : Optional[str] = None
                ,args : List[Arg]     = []
                ) -> None:
        assert callable(func), 'Not a func: '+str(func)
        self.func     = Func(func)

        if name is None:
            name = self.func.name

        self.name     = name
        self.args     = args

    def apply(self
             ,curr_dict : Dict[str,Any]
             ,cxn       : Optional[ConnectInfo] = None
             ) -> Any:
        """
        Take a TempFunc's function and wrap it such that it can accept a namespace
            dictionary. The information about how the function interacts with the
            namespace is contained in the TempFunc's args.
        """
        assert cxn is None

        inputvars = [arg.arg_get(curr_dict) for arg in self.args]

        try:
            return self.func.apply(*inputvars)
        except Exception as e:
            msg = '\tApplying func %s in tempfunc %s:\n\t'%(self.func.name,self.name)
            raise ExternalError(msg + format_exc())

# PBlock Shortcuts

def Rename(a:str,b:str)-> Block:
    return PyBlock(identity,b,[Arg(a)])

def Unpack(a:str,b:List[str])-> List[Block]:
    return [PyBlock(identity,b[i],[Arg(a,i)]) for i in range(len(b))]

def SimpleFunc(func    : Callable
              ,inputs  : List[str] = []
              ,outputs : List[str] = []
              ) -> List[Block]:
    """
    For a rule that has one function in its template
    """
    main_func = PyBlock(func,'main',args=[Arg(x) for x in inputs]) # type: Block
    if len(outputs)==1:
        exported = [PyBlock(identity,outputs[0],[Arg('main')])] # type: List[Block]
    else:
        exported  = [PyBlock(identity,x,[Arg('main',i)])
                        for i,x in enumerate(outputs)]
    return [main_func]+exported

def SimplePipe(funcs   : List[Callable]
              ,inputs  : List[str]
              ,outputs : List[str]
              ,const   : Dict[str,Const] = {}
              ) -> List[Block]:
    """
    A series of functions where the output of each function is fed to the
    following function in the pipeline. You must specify the names of the
    inputs and outputs to the whole process
    """
    init_func = PyBlock(funcs[0],args=[Arg(x) for x in inputs])  # type: Block
    remaining = [PyBlock(funcs[i],args=[Arg(funcs[i-1].__name__)]) for i in range(1,len(funcs))]   # type: List[Block]
    if len(outputs)==1:
        exported = [PyBlock(identity,outputs[0],[Arg(funcs[-1].__name__)])]  # type: List[Block]
    else:
        exported  = [PyBlock(identity,x,[Arg(funcs[-1].__name__,i)])
                        for i,x in enumerate(outputs)]
    return  [init_func] + remaining + exported
################################################################################

class Plan(object):
    """

    """
    def __init__(self
                ,blocks : List[Block]
                ,consts : Dict[str,Const] = {}
                ) -> None:
        self.blocks = self.order_blocks(blocks)
        self.consts = consts

    def apply(self,query_dic:Dict[str,Any],cxn:ConnectInfo)->None:
        consts = {k:v.val for k,v in self.consts.items()}
        dic    = {**consts,**query_dic} # MERGE
        for b in self.blocks:
            c = None if isinstance(b,PyBlock) else cxn # don't give python cxnInfo
            dic[b.name] = b.apply(dic,c) #type: ignore

    def add_plan(self,sqlite_pth:str,id:int)->None:
        raise NotImplementedError

    @staticmethod
    def order_blocks(bs:List[Block])->List[Block]:
        """
        Prior to storing the list of blocks as a field of the Plan,
        order them such that any block that calls some other block occurs afterwards

        DO WE NEED A HEURISTIC TO HELP WITH INSERT -> SELECT ORDERING?
        OR SHOULD SELECT STATEMENTS ADD "ARTIFICIAL" DEPENDENCIES?
        OR SHOULD S-BLOCKS HAVE AN OPTIONAL 'deps' FIELD WITH SBLOCK NAMES?
        """
        G = DiGraph() # each template has a DAG, with tempfuncs as nodes
        G.add_nodes_from([b.name for b in bs])

        b_dict = {b.name : b for b in bs}

        for b in bs:
            for ba in b.args:
                if ba.name in b_dict.keys():
                    G.add_edge(ba.name,b.name)
            for d in b.deps:
                G.add_edge(d,b.name)
        return topsort_with_dict(G,b_dict)
################################################################################

class Applier(object):
    """
    Class needed for parallel mapping (cannot parallel map lambda functions)
    """
    fail = '%s failed with inputs %s \n%s'

    def __init__(self, rule:'Rule',cxn:ConnectInfo)->None:
        self.rule = rule
        self.cxn  = cxn

    def __call__(self, row:dict)->None:
        try:
            self.rule.plan.apply(row,self.cxn)
        except ExternalError as e:
            row_ = {k:self.abbreviate(v) for k,v in row.items()}
            raise ExternalError(self.fail%(self.rule.name,row_,e))

    @staticmethod
    def abbreviate(x:Any)->Any:
        if isinstance(x,str) and len(x) > 1000:
            return x[:1000]+'...'
        else:
            return x
################################################################################
class Rule(object):
    """
    Information required to transform the database

    Generally, one must provide:
        - a unique name by which this action can be referred (method_name)
        - how to get the required information for the rule (query)
        - a procedure for processing the info and putting it back in the DB (plan)
    """

    def __init__(self
                ,name   : str
                ,query  : Optional[str] = None
                ,plan   : Plan          = Plan([])
                ,stream : bool          = False
                ) -> None:

        if query is not None:
            query = sql_format(query, reindent=True).strip()
            query = sql_format(query, reindent=True) # indempotency

        self.name   = name
        self.query  = query
        self.plan   = plan
        self.stream = stream

        # Precompute dependencies of all SQL commands
        #--------------------------------------------
        mbQuery     = [] if self.query is None else [self.query]
        allsql      = mbQuery + [b.text for b in self.plan.blocks if isinstance(b,SqlBlock)]
        self.deps   = parse_dependencies(allsql)

    def __str__(self)->str:
        return pformat(self.__dict__)

    def __repr__(self)->str:
        return str(self)

    def __eq__(self,other : object)->bool:
        return self.__dict__==other.__dict__

    def dependency_failed(self,conn : ConnectInfo) -> Any:
        q = """SELECT child
                FROM META_dependencies
                JOIN META_rule ON parent = method
                WHERE child =%s AND status like '%%failed%%'"""
        output = sqlselect(conn,q,[self.name])
        return True if len(output) == 0 else output

    def run_rule(self
                ,cxn      : ConnectInfo
                ,parallel : bool = True
                ) -> None:
        """
        Executes a SQL query, then maps each output over a processing function
        which modifies the database.
        """

        try:
            start = time()
            tot   = 0

            if self.query is None:
                inputs = [{}] # type: List[dict]
                length = 1
            else:
                cur = select_dict(cxn,self.query)  # type: ignore
                if not self.stream:
                    inputs = list(cur)
                    length = len(inputs)
                    cur.close() # type: ignore
                else:
                    inputs = cur # type: ignore
                    length = -1

            applier = Applier(self,cxn) # type: ignore

            if parallel:
                cpus = cpu_count() # -1 or 1 # play safe, leave one free
                with Pool(cpus) as p: # catastrophic failure less likely if we use n-1 available nodes
                    for _ in tqdm(p.imap_unordered(applier,inputs),total=length):
                        tot+=1
            else:

                for _ in tqdm(map(applier,inputs),total=length): # type: ignore
                    tot+=1

            if self.stream:
                cur.close() # type: ignore

            self.update_status(cxn,'completed')
            tot_time = time()-start
            self.update_time(cxn,tot_time/60,safe_div(tot_time,tot))

        except ExternalError as e:
            err = str(e).replace('\\n','\n')
            msg = 'Error when running rule %s\n'%self.name
            print(msg + err)
            self.log_error(cxn,msg + err)

    def log_error(self
                 ,conn : ConnectInfo
                 ,err  : str
                 ) -> None:
        self.update_status(conn,'failed')
        q = "UPDATE META_rule SET error=%s WHERE method=%s"
        sqlexecute(conn,q,[err,self.name])

    def update_status(self
                     ,conn : ConnectInfo
                     ,stat : str
                     ) -> None:
        q = "UPDATE META_rule SET status=%s WHERE method=%s"
        sqlexecute(conn,q,[stat,self.name])

    def update_time(self
                   ,conn     : ConnectInfo
                   ,duration : float
                   ,rate     : float
                   ) -> None:
        q = "UPDATE META_rule SET runtime=%s,rate=%s WHERE method=%s"
        sqlexecute(conn,q,[duration,rate,self.name])

    def add_rule(self,sqlite_pth : str) -> None:
        """
        Insert a Rule to the meta.db
        """
        cmd   = mkInsCmd('rule',['name','query'],sqlite=True)
        sqlite_execute(sqlite_pth,cmd,[self.name,self.query])
        sqlite_execute(sqlite_pth,namespaceCmd,[self.name,'Rule'])
        t_id = handle_to_ind(sqlite_pth,self.name)
        self.plan.add_plan(sqlite_pth,t_id)
