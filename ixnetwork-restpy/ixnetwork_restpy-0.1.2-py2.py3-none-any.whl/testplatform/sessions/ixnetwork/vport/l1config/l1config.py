from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class L1Config(Base):
	"""Layer 1 (physical) configuration.
	"""

	_SDM_NAME = 'l1Config'

	def __init__(self, parent):
		super(L1Config, self).__init__(parent)

	@property
	def OAM(self):
		"""Returns the one and only one OAM object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.oam.oam.OAM)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.oam.oam import OAM
		return self._read(OAM(self), None)

	@property
	def AtlasFourHundredGigLan(self):
		"""Returns the one and only one AtlasFourHundredGigLan object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.atlasfourhundredgiglan.atlasfourhundredgiglan.AtlasFourHundredGigLan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.atlasfourhundredgiglan.atlasfourhundredgiglan import AtlasFourHundredGigLan
		return self._read(AtlasFourHundredGigLan(self), None)

	@property
	def Atm(self):
		"""Returns the one and only one Atm object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.atm.atm.Atm)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.atm.atm import Atm
		return self._read(Atm(self), None)

	@property
	def Ethernet(self):
		"""Returns the one and only one Ethernet object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernet.ethernet.Ethernet)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernet.ethernet import Ethernet
		return self._read(Ethernet(self), None)

	@property
	def EthernetImpairment(self):
		"""Returns the one and only one EthernetImpairment object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernetimpairment.ethernetimpairment.EthernetImpairment)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernetimpairment.ethernetimpairment import EthernetImpairment
		return self._read(EthernetImpairment(self), None)

	@property
	def Ethernetvm(self):
		"""Returns the one and only one Ethernetvm object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernetvm.ethernetvm.Ethernetvm)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.ethernetvm.ethernetvm import Ethernetvm
		return self._read(Ethernetvm(self), None)

	@property
	def Fc(self):
		"""Returns the one and only one Fc object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.fc.fc.Fc)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.fc.fc import Fc
		return self._read(Fc(self), None)

	@property
	def FortyGigLan(self):
		"""Returns the one and only one FortyGigLan object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.fortygiglan.fortygiglan.FortyGigLan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.fortygiglan.fortygiglan import FortyGigLan
		return self._read(FortyGigLan(self), None)

	@property
	def FramePreemption(self):
		"""Returns the one and only one FramePreemption object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.framepreemption.framepreemption.FramePreemption)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.framepreemption.framepreemption import FramePreemption
		return self._read(FramePreemption(self), None)

	@property
	def HundredGigLan(self):
		"""Returns the one and only one HundredGigLan object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.hundredgiglan.hundredgiglan.HundredGigLan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.hundredgiglan.hundredgiglan import HundredGigLan
		return self._read(HundredGigLan(self), None)

	@property
	def KrakenFourHundredGigLan(self):
		"""Returns the one and only one KrakenFourHundredGigLan object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.krakenfourhundredgiglan.krakenfourhundredgiglan.KrakenFourHundredGigLan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.krakenfourhundredgiglan.krakenfourhundredgiglan import KrakenFourHundredGigLan
		return self._read(KrakenFourHundredGigLan(self), None)

	@property
	def NovusHundredGigLan(self):
		"""Returns the one and only one NovusHundredGigLan object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.novushundredgiglan.novushundredgiglan.NovusHundredGigLan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.novushundredgiglan.novushundredgiglan import NovusHundredGigLan
		return self._read(NovusHundredGigLan(self), None)

	@property
	def NovusTenGigLan(self):
		"""Returns the one and only one NovusTenGigLan object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.novustengiglan.novustengiglan.NovusTenGigLan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.novustengiglan.novustengiglan import NovusTenGigLan
		return self._read(NovusTenGigLan(self), None)

	@property
	def Pos(self):
		"""Returns the one and only one Pos object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.pos.pos.Pos)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.pos.pos import Pos
		return self._read(Pos(self), None)

	@property
	def RxFilters(self):
		"""Returns the one and only one RxFilters object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.rxfilters.rxfilters.RxFilters)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.rxfilters.rxfilters import RxFilters
		return self._read(RxFilters(self), None)

	@property
	def TenFortyHundredGigLan(self):
		"""Returns the one and only one TenFortyHundredGigLan object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tenfortyhundredgiglan.tenfortyhundredgiglan.TenFortyHundredGigLan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tenfortyhundredgiglan.tenfortyhundredgiglan import TenFortyHundredGigLan
		return self._read(TenFortyHundredGigLan(self), None)

	@property
	def TenGigLan(self):
		"""Returns the one and only one TenGigLan object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.tengiglan.TenGigLan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengiglan.tengiglan import TenGigLan
		return self._read(TenGigLan(self), None)

	@property
	def TenGigWan(self):
		"""Returns the one and only one TenGigWan object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengigwan.tengigwan.TenGigWan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.tengigwan.tengigwan import TenGigWan
		return self._read(TenGigWan(self), None)

	@property
	def CurrentType(self):
		"""Indicates the five types of ports for configuration to choose from.

		Returns:
			str(atlasFourHundredGigLan|atlasFourHundredGigLanFcoe|atm|ethernet|ethernetFcoe|ethernetImpairment|ethernetvm|fc|fortyGigLan|fortyGigLanFcoe|hundredGigLan|hundredGigLanFcoe|krakenFourHundredGigLan|novusHundredGigLan|novusHundredGigLanFcoe|novusTenGigLan|novusTenGigLanFcoe|pos|tenFortyHundredGigLan|tenFortyHundredGigLanFcoe|tenGigLan|tenGigLanFcoe|tenGigWan|tenGigWanFcoe)
		"""
		return self._get_attribute('currentType')
	@CurrentType.setter
	def CurrentType(self, value):
		self._set_attribute('currentType', value)
