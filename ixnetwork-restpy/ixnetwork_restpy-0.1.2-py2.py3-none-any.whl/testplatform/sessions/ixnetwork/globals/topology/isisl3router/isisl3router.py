from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IsisL3Router(Base):
	"""ISIS-L3 Port Configuration
	"""

	_SDM_NAME = 'isisL3Router'

	def __init__(self, parent):
		super(IsisL3Router, self).__init__(parent)

	@property
	def StartRate(self):
		"""Returns the one and only one StartRate object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisl3router.startrate.startrate.StartRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisl3router.startrate.startrate import StartRate
		return self._read(StartRate(self), None)

	@property
	def StopRate(self):
		"""Returns the one and only one StopRate object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisl3router.stoprate.stoprate.StopRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisl3router.stoprate.stoprate import StopRate
		return self._read(StopRate(self), None)

	@property
	def BIERInfoSubTLVType(self):
		"""BIER Info Sub-TLV Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bIERInfoSubTLVType')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NoOfLSPsOrMgroupPDUsPerInterval(self):
		"""LSPs/MGROUP-PDUs per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('noOfLSPsOrMgroupPDUsPerInterval')

	@property
	def RateControlInterval(self):
		"""Rate Control Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rateControlInterval')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	@property
	def SendP2PHellosToUnicastMAC(self):
		"""Send P2P Hellos To Unicast MAC

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendP2PHellosToUnicastMAC')

	@property
	def SrDraftExtension(self):
		"""This refers to the TLV structure of SRGB as per the Segment Routing draft version

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srDraftExtension')

	@property
	def SrlbSubTlvType(self):
		"""This specifies the type of Segment Routing Local Block sub tlv, suggested value is 22.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srlbSubTlvType')

	@property
	def SrmsPreferenceSubTlvType(self):
		"""This specifies the type of SRMS Preference sub tlv, suggested value is 23.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srmsPreferenceSubTlvType')

	@property
	def Srv6AdjSIDSubTlvType(self):
		"""This specifies the type of SRv6 Adjacency-SID sub-TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srv6AdjSIDSubTlvType')

	@property
	def Srv6CapabilitiesSubTlvType(self):
		"""This specifies the type of SRv6 Capabilities sub-TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srv6CapabilitiesSubTlvType')

	@property
	def Srv6LANAdjSIDSubTlvType(self):
		"""This specifies the type of SRv6 LAN Adjacency-SID sub-TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srv6LANAdjSIDSubTlvType')

	@property
	def Srv6NodeSIDTlvType(self):
		"""This specifies the type of SRv6 Node SID TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srv6NodeSIDTlvType')

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('fetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)
