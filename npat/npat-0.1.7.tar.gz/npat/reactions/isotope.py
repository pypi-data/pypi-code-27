import os,sqlite3,re,numpy as np
from ast import literal_eval
_db_connection = sqlite3.connect('/'.join(os.path.realpath(__file__).split('/')[:-2])+'/data/decay_data/decay.db')
_db = _db_connection.cursor()

class isotope(object):
	def __init__(self,istp):
		self.db = _db
		if istp=='1n':
			self.element,self.A,self.isomer = 'n',1,'g'
		else:
			self.element = ''.join(re.findall('[A-Z]+',istp))
			self.A,self.isomer =  int(istp.split(self.element)[0]),istp.split(self.element)[1]
		self.isotope = str(self.A)+self.element
		if self.isomer=='':
			self.isomer = 'g'
		if self.isomer=='m':
			self.isomer = 'm1'
		self.name = self.isotope+self.isomer
		self.N_states = len([i[1] for i in self.db.execute('SELECT * FROM chart WHERE isotope=?',(self.isotope,))])
		c = map(list,self.db.execute('SELECT * FROM chart WHERE isotope=? AND isomer=?',(self.isotope,self.isomer)))[0]
		self.E_level,self.J_pi,self.Z,self.N,self.stable = c[2],str(c[4]),c[6],c[7],bool(c[9])
		self.t_half,self.unc_t_half,self.abundance,self.unc_abundance = c[10],c[11],c[12],c[13]
		self.amu,self.Delta,self.decay_mode = c[14],c[15],literal_eval(str(c[16]))
		self.gm,self.el,self.bm,self.bp,self.al = None,None,None,None,None
	def TeX(self):
		state = '' if self.N_states==1 else self.isomer
		if self.N_states==2:
			state = state[0]
		return r'$^{'+str(self.A)+state+r'}$'+self.element.title()
	def half_life(self,units='s',unc=False):
		if self.stable:
			return (np.inf,0.0) if unc else np.inf
		half_conv = {'ns':1e-9,'us':1e-6,'ms':1e-3,'s':1.0,'m':60.0,'h':3600.0,'d':86400.0,'y':31557600.0}[units]
		if unc:
			return self.t_half/half_conv,self.unc_t_half/half_conv
		return self.t_half/half_conv
	def decay_const(self,units='s',unc=False):
		if self.stable:
			return (0.0,0.0) if unc else 0.0
		if unc:
			T2,uT2 = self.half_life(units,unc)
			return np.log(2.0)/T2,np.log(2.0)*uT2/T2**2
		return np.log(2.0)/self.half_life(units)
	def optimum_units(self):
		opt = ['ns']
		for units in ['us','ms','s','m','h','d','y']:
			if self.half_life(units)>1.0:
				opt.append(units)
		return opt[-1]
	def gammas(self,I_lim=[None,None],E_lim=[None,None],xrays=False):
		if self.gm is None:
			self.gm = [[float(i[3]),float(i[4]),float(i[5]),str(i[6])] for i in self.db.execute('SELECT * FROM gammas WHERE isotope=? AND isomer=?',(self.isotope,self.isomer))]
		gammas = list(self.gm)
		for n,L in enumerate([E_lim,I_lim]):
			if L[0] is not None:
				gammas = [g for g in gammas if g[n]>=L[0]]
			if L[1] is not None:
				gammas = [g for g in gammas if g[n]<=L[1]]
		if not xrays:
			gammas = [g for g in gammas if g[3]=='' and abs(g[0]-511.0)>4.0]
		return {l:[g[n] for g in gammas] for n,l in enumerate(['E','I','dI','notes'])}
	def electrons(self,I_lim=(None,None),E_lim=(None,None),CE_only=False,Auger_only=False):
		if self.el is None:
			self.el = [[float(i[3]),float(i[4]),float(i[5]),str(i[6])] for i in self.db.execute('SELECT * FROM electrons WHERE isotope=? AND isomer=?',(self.isotope,self.isomer))]
		electrons = list(self.el)
		for n,L in enumerate([E_lim,I_lim]):
			if L[0] is not None:
				electrons = [e for e in electrons if e[n]>=L[0]]
			if L[1] is not None:
				electrons = [e for e in electrons if e[n]<=L[1]]
		if CE_only:
			electrons = [e for e in electrons if e[3].startswith('CE')]
		if Auger_only:
			electrons = [e for e in electrons if e[3].startswith('Aug')]
		return {l:[e[n]for e in electrons] for n,l in enumerate(['E','I','dI','notes'])}
	def beta_minus(self,I_lim=(None,None),Endpoint_lim=(None,None)):
		if self.bm is None:
			self.bm = [[float(i[3]),float(i[4]),float(i[5]),float(i[6])] for i in self.db.execute('SELECT * FROM beta_minus WHERE isotope=? AND isomer=?',(self.isotope,self.isomer))]
		betas = list(self.bm)
		for n,L in zip([3,1],[Endpoint_lim,I_lim]):
			if L[0] is not None:
				betas = [b for b in betas if b[n]>=L[0]]
			if L[1] is not None:
				betas = [b for b in betas if b[n]<=L[1]]
		return {l:[b[n] for b in betas] for n,l in enumerate(['muE','I','dI','endE'])}
	def beta_plus(self,I_lim=(None,None),Endpoint_lim=(None,None)):
		if self.bp is None:
			self.bp = [[float(i[3]),float(i[4]),float(i[5]),float(i[6])] for i in self.db.execute('SELECT * FROM beta_plus WHERE isotope=? AND isomer=?',(self.isotope,self.isomer))]
		betas = list(self.bp)
		for n,L in zip([3,1],[Endpoint_lim,I_lim]):
			if L[0] is not None:
				betas = [b for b in betas if b[n]>=L[0]]
			if L[1] is not None:
				betas = [b for b in betas if b[n]<=L[1]]
		return {l:[b[n] for b in betas] for n,l in enumerate(['muE','I','dI','endE'])}
	def alphas(self,I_lim=(None,None),E_lim=(None,None)):
		if self.al is None:
			self.al = [[float(i[3]),float(i[4]),float(i[5])] for i in self.db.execute('SELECT * FROM alphas WHERE isotope=? AND isomer=?',(self.isotope,self.isomer))]
		alphas = list(self.al)
		for n,L in enumerate([E_lim,I_lim]):
			if L[0] is not None:
				alphas = [a for a in alphas if b[n]>=L[0]]
			if L[1] is not None:
				alphas = [a for a in betas if b[n]<=L[1]]
		return {l:[a[n] for a in alphas] for n,l in enumerate(['E','I','dI'])}

