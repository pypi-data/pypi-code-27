import  sys
if sys.version_info>=(3,0):
   from .seqmastermng import SeqMasterMng
   from .seqmastermod import SeqMasterMod
   from .seqmastermod import SeqLineMod
else:
   from seqmastermng import SeqMasterMng
   from seqmastermod import SeqMasterMod
   from seqmastermod import SeqLineMod
