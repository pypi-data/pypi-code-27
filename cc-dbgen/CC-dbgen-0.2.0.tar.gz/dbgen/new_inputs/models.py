# Internal modules
from dbgen.support.datatypes.model  import Model
from dbgen.new_inputs.objects       import kris
from dbgen.new_inputs.relations     import relations

###############################################################################
if __name__=='__main__':
    from dbgen.main import parser
    args = parser.parse_args()
    m    = Model(kris,relations)
    m.run(reset   = args.reset
         ,catalog = args.catalog
         ,add     = args.add
         ,xclude  = args.xclude
         ,only    = args.only
         ,db      = args.db)
