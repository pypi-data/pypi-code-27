import  sys
if sys.version_info>=(3,0):
   from .seqmaster import *
else:
   from  seqmaster import *