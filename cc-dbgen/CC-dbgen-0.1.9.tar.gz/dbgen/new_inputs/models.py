# Internal modules
from dbgen.support.datatypes.model      import Model
from dbgen.support.datatypes.func       import Func
from dbgen.support.datatypes.object     import Object
from dbgen.new_inputs.relations        import relations

###############################################################################
if __name__=='__main__':
    from dbgen.main import parser
    args = parser.parse_args()
    m = Model(Object.universe,relations)
    m.run(reset   = args.reset
         ,catalog = args.catalog
         ,add     = args.add
         ,xclude  = args.xclude
         ,only    = args.only)
