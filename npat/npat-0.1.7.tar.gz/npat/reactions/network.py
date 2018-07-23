import sqlite3,numpy as np
from npat import isotope
from ast import literal_eval

class network(object):
	def __init__(self):
		pass

class chain(object):
	def __init__(self,parent):
		decays = ['BA','BN','B2N','2E','2P','BNA','E2P','B3A','2BN','EAP','BSF','A','B','E','P','EA','IT','N','ESF','B3N','2B','2N','EP','E3P','SF']
		for d in decays:
			dc = d
			print d
			while len(dc)>0:
				if dc.startswith('2'):
					print '2'
					dc = dc[1:]
				elif dc.startswith('3'):
					print '3'
					dc = dc[1:]
				else:
					for t in ['B','N','E','P','IT','SF','A']:
						if dc.startswith(t):
							print t
							dc = dc[len(t):]

		self.parent = isotope(parent) if type(parent)==str else parent
		print self.parent.decay_mode

class branch(object):
	def __init__(self):
		pass

# _db = isotope('1H').db
# print set([f[h] for f in [e for d in [literal_eval(str(i[0])) for i in _db.execute('SELECT decay_mode FROM chart')] for e in d] for h in f])

ch = chain('135CEm')