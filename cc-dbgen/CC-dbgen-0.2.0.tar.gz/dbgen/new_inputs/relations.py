# External
from typing import Union,List
# Internal Modules
from dbgen.support.datatypes.sqltypes     import Varchar,Date
from dbgen.support.datatypes.relation     import Relation
from dbgen.support.datatypes.insertupdate import Insert,InsertUpdate
from dbgen.support.datatypes.misc         import Arg,noIndex
from dbgen.support.datatypes.constraint   import NULL,IN
from dbgen.support.datatypes.rule         import Const,SimplePipe,PyBlock,Rename,Unpack,SimpleFunc,Block

from dbgen.new_inputs.objects import *
from dbgen.core.lists         import flatten

from dbgen.scripts.IO.anytraj                   import anytraj
from dbgen.scripts.IO.parse_mendeleev           import parse_mendeleev
from dbgen.scripts.IO.get_job_metadata          import get_job_metadata
from dbgen.scripts.IO.populate_storage          import populate_storage
from dbgen.scripts.IO.get_catalog_logfiles      import get_catalog_logfiles

from dbgen.scripts.Pure.Misc.map_               import map_
from dbgen.scripts.Pure.Misc.hash_              import hash_
from dbgen.scripts.Pure.Misc.unzip              import unzip
from dbgen.scripts.Pure.Misc.triple             import triple
from dbgen.scripts.Pure.Misc.identity           import identity
from dbgen.scripts.Pure.Misc.concat_map         import concat_map
from dbgen.scripts.Pure.Misc.dftcode_dependent  import dftcode_dependent

from dbgen.scripts.Pure.Atoms.cell_info          import cell_info
from dbgen.scripts.Pure.Atoms.json_to_traj       import json_to_traj
from dbgen.scripts.Pure.Atoms.traj_to_json       import traj_to_json
from dbgen.scripts.Pure.Atoms.get_system_type    import get_system_type
from dbgen.scripts.Pure.Atoms.get_cell           import get_cell
from dbgen.scripts.Pure.Atoms.get_atom           import get_atom
from dbgen.scripts.Pure.Atoms.get_traj_gpaw_lazy import get_traj_gpaw_lazy
from dbgen.scripts.Pure.Atoms.get_traj_qe_lazy   import get_traj_qe_lazy
from dbgen.scripts.Pure.Atoms.get_traj_vasp_lazy import get_traj_vasp_lazy

from dbgen.scripts.Pure.Load.parse_pw_gpaw      import parse_pw_gpaw
from dbgen.scripts.Pure.Load.parse_pw_qe        import parse_pw_qe
from dbgen.scripts.Pure.Load.parse_pw_vasp      import parse_pw_vasp
from dbgen.scripts.Pure.Load.parse_xc_gpaw      import parse_xc_gpaw
from dbgen.scripts.Pure.Load.parse_xc_qe        import parse_xc_qe
from dbgen.scripts.Pure.Load.parse_xc_vasp      import parse_xc_vasp
from dbgen.scripts.Pure.Load.parse_psp_gpaw     import parse_psp_gpaw
from dbgen.scripts.Pure.Load.parse_psp_qe       import parse_psp_qe
from dbgen.scripts.Pure.Load.parse_psp_vasp     import parse_psp_vasp
from dbgen.scripts.Pure.Load.normalize_xc       import normalize_xc
from dbgen.scripts.Pure.Load.normalize_psp      import normalize_psp

Actions = List[Union[PyBlock,List[PyBlock]
              ,Block,List[Block]
              ,InsertUpdate,List[InsertUpdate]]]
Action = Union[PyBlock,Block,InsertUpdate]

##############################################################################
# Constants
#----------
pop_job_cols = ['stordir','logfile','code','log','pwinp'
               ,'potcar','poscar','kptcar','paramdict']

mdata_input = ['stordir','code','paramdict']
mdata_cols  = ['user','timestamp','working_directory'
              ,'job_type','job_name']

elem_cols  =  [ 'element_id', 'symbol', 'name', 'atomic_weight','atomic_radius'
              , 'phase','evaporation_heat', 'pointgroup','spacegroup'
              , 'melting_point', 'metallic_radius', 'vdw_radius'
              , 'density', 'en_allen', 'is_radioactive'
              , 'lattice_struct' , 'fusion_heat'
              , 'econf', 'period', 'covalent_radius_bragg'
              , 'geochemical_class', 'abundance_crust', 'heat_of_formation'
              , 'electron_affinity', 'atomic_volume',  'boiling_point'
              , 'proton_affinity', 'covalent_radius_slater'
              , 'lattice_constant', 'dipole_polarizability'
              , 'en_ghosh', 'thermal_conductivity', 'group_id', 'en_pauling'
              , 'gas_basicity','abundance_sea']

cell_cols = ['a0','a1','a2','b0','b1','b2','c0','c1','c2']


dfts       = ['gpaw','qe','vasp']
parsed     = ['pw',  'xc','psp']

calc_funcs = [parse_pw_gpaw,parse_pw_qe,parse_pw_vasp # type: ignore
             ,parse_xc_gpaw,parse_xc_qe,parse_xc_vasp
             ,parse_psp_gpaw,parse_psp_qe,parse_psp_vasp
             ,normalize_xc,normalize_psp,identity]

traj_funcs = [get_traj_gpaw_lazy,get_traj_qe_lazy,get_traj_vasp_lazy,identity
             ,unzip,traj_to_json,get_atom,get_cell,hash_]

##############################################################################
# Complicated Functions
#----------------------

relax_calc_acts = [PyBlock(func = dftcode_dependent
                          ,name = x
                          ,args = noIndex(['dftcode'
                                          ,'log'
                                          ,'parse_%s_gpaw'%x
                                          ,'parse_%s_qe'%x
                                          ,'parse_%s_vasp'%x
                                          ,'identity'
                                          ,'identity' if x =='pw' else 'normalize_%s'%x]))
                    for x in parsed] + [PyBlock(identity,'dftcode',[Arg('code')])]



traj_acts = [PyBlock(triple
                   ,'anytraj_log_poscar'
                   ,args = noIndex(['anytraj','log','poscar']))

            ,PyBlock(dftcode_dependent
                   ,name = 'get_traj'
                   ,args = noIndex(['code'
                                   ,'anytraj_log_poscar'
                                   ,'get_traj_gpaw_lazy'
                                   ,'get_traj_qe_lazy'
                                   ,'get_traj_vasp_lazy'
                                   ,'identity'
                                   ,'unzip'])) # returns ([ASEATOMS]m,[STEPNUM]m,[ENERGY]m,[TRAJATOMLIST]m)
            ,PyBlock(map_
                    ,name = 'cell'
                    ,args = noIndex(['get_cell','structs_few'])) # returns ([ax]m,[ay]m,...)

           ,PyBlock(map_
                    ,name = 'structs_few'
                    ,args = [Arg('traj_to_json')
                            ,Arg('get_traj', 0)]) # returns [raw_json]m
           ,PyBlock(map_
                    ,name = 'rawhash'
                    ,args = [Arg('hash_')
                            ,Arg('structs_few')]) # returns [hashed raw_json]m

           ,PyBlock(concat_map
                  ,name = 'atoms'
                  ,args = noIndex(['get_atom','structs_few'])) # returns ([ASEATOMS]n,[Ind]n,[ELEMENT]n,[X]n,[Y]n,...)

           ,PyBlock(identity
                ,name = 'structs_many'
                ,args = [Arg('atoms', 0)])# returns [raw_json]n


           ,PyBlock(flatten
                 ,name = 'flattened_trajatoms'
                 ,args = [Arg('get_traj',3)])  # [STEPNUM,Ind,FX,FY,FZ]n

           ,PyBlock(unzip
                     ,'trajatoms'
                     ,args=[Arg('flattened_trajatoms')])

           ,Rename('structs_few','raw')     # ([STEPNUM]n,[Ind]n,[FX]n,[FY]n,[FZ]n)
           ,Unpack('cell',cell_cols)
           ,Cell.insert(cell_cols)
           ,Struct.insert(['raw','rawhash'])
           ,Struct.update_component(Cell.select(cell_cols))] # type: Actions

########################################################################
# Relations
#----------
loading_relations = [
    Relation(name    = 'catalog'
            ,view    = view(attr  = [Roots.root]                    # type: ignore
                           ,const = [Roots.label  == "'catalog'"    # type: ignore
                                    ,Roots.active == 1])      # type: ignore
            ,actions = [SimpleFunc(func    = get_catalog_logfiles
                                 ,inputs  = ['root']
                                 ,outputs = pop_job_cols)
                        ,Job.insert(pop_job_cols)])

   ,Relation(name    = 'populate_storage'
            ,actions = [SimpleFunc(func    = populate_storage
                                  ,outputs = ['root','code','label'])
                       ,Roots.insert(['root','code','label'])])

   ,Relation(name    = 'job_metadata'
            ,view    = view(attr  = Job.select(mdata_input)         # type: ignore
                           ,const = [NULL(Job.user)])               # type: ignore
            ,actions = [SimpleFunc(func    = get_job_metadata
                                 ,inputs  = mdata_input
                                 ,outputs = mdata_cols)
                       ,Job.update(mdata_cols)])

   ,Relation(name   = 'anytraj'
            ,view   = view(attr  = Job.select(['stordir']) # type: ignore
                          ,const = [NULL(Job.anytraj)])  # type: ignore
            ,actions   = [SimpleFunc(anytraj,['stordir'],['anytraj'])
                         ,Job.update(['anytraj'])])

    ,Relation(name = 'mendeleev'
             ,actions = [SimpleFunc(parse_mendeleev,outputs = elem_cols)
                        ,Element.insert(elem_cols)])

    ,Relation(name    = 'cell_info'
             ,view    = view(attr =Cell.select(cell_cols)) # type: ignore
             ,actions = [SimpleFunc(cell_info,cell_cols,['surface_area','volume'])
                        ,Cell.update(['surface_area','volume'])])

   ,Relation(name    = 'relax_calc'
            ,view    = view(attr =Job.select(['log','code'])         # type: ignore
                           ,const = [Relax_job._hasnt(Calc)])      # type: ignore
            ,consts  = {f.__name__:Const(f) for f in calc_funcs}
            ,actions = [Relax_job.update_component(
                            Calc.select(['dftcode','pw','xc','psp']))])

   ,Relation(name = 'systype'
            ,view =  view(attr  = [Struct.raw]                 # type: ignore
                         ,const = [NULL(Struct.system_type)])  # type: ignore
            ,actions = [SimplePipe([json_to_traj,get_system_type]
                               ,inputs  = ['raw']
                               ,outputs = ['system_type'])
                        ,Struct.update(['system_type'])])

   ,Relation(name    = 'relax_job'
            ,view  = view(attr  = Job.select()        # type: ignore
                         ,const = [IN(Job.job_type    # type: ignore
                                    ,["'relax'","'latticeopt'","'vcrelax'"])])
            ,actions = [Relax_job.insert()])

    ,Relation(name    = 'traj'
             ,view    = view(Job.select(['code','log','anytraj','poscar','stordir'])) # type: ignore
             ,consts  = {f.__name__:Const(f) for f in traj_funcs}
             ,actions = traj_acts )
#     ,metatemp = MetaTemp([
#         Block(name = 'insert_cell'
#              ,text = mkInsCmd('cell',cell_cols,sqlite=False)
#              ,args = cell_args)
#
#        ,Block(name = 'query_cell'
#              ,text = ('SELECT C.cell_id FROM cell AS C WHERE '
#                      +addQs(['C.%s'%x for x in cell_cols],' AND '))
#              ,args = cell_args)
#
#        ,Block(name = 'insert_struct'
#              ,text = """INSERT INTO struct (raw,rawhash,cell_id)
#                            VALUES (%s,SHA2(%s,512),%s)
#                         ON DUPLICATE KEY UPDATE cell_id=cell_id"""
#              ,args = [Arg('structs_few')
#                       ,Arg('structs_few')
#                      ,Arg('query_cell',0)])
#
#        ,Block(name = 'query_struct_few'
#              ,text = 'SELECT S.struct_id FROM struct AS S WHERE S.rawhash = SHA2(%s,512)'
#              ,args = [Arg('structs_few')])
#
#        ,Block(name = 'query_struct_many'
#              ,text = 'SELECT S.struct_id FROM struct AS S WHERE S.rawhash = SHA2(%s,512)'
#              ,args = [Arg('structs_many')])
#
#        ,Block(name = 'insert_atom'
#              ,text = mkInsCmd('atom',['struct_id','atom_id','element_id'
#                                   ,'x','y','z','constrained','magmom','tag']
#                             ,sqlite=False)
#              ,args = [Arg('query_struct_many')]
#                     +[Arg('atoms',i) for i in range(1,9)])
#
#      ,Block(name = 'insert_traj'
#            ,text = mkInsCmd('traj',['job_id','traj_id','struct_id','energy','final'],sqlite=False)
#            ,args = [Arg('job_id')
#                    ,Arg('get_traj',1)
#                    ,Arg('query_struct_few')
#                    ,Arg('get_traj',2)
#                    ,Arg('get_traj',4)])
#
#     ,Block(name = 'insert_trajatom'
#           ,text = mkInsCmd('trajatom',['job_id','traj_id','struct_id','atom_id','fx','fy','fz'],sqlite=False)
#           ,args = [Arg('job_id')
#                   ,Arg('trajatoms',0)
#                   ,Arg('query_struct_many')]
#                  +[Arg('trajatoms',i) for i in range(1,5)])]))


]


relations = loading_relations
