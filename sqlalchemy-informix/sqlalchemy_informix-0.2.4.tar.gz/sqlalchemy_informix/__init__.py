__version__ = '0.2.4'

import os
from sqlalchemy.dialects import registry

os.environ['DELIMIDENT'] = 'y'

registry.register("informix", "sqlalchemy_informix.ibmdb", "InformixDialect")
