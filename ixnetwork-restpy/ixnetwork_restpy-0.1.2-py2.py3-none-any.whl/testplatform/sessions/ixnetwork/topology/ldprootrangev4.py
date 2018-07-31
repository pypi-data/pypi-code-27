from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LdpRootRangeV4(Base):
	"""Ldp Targeted RootRange V4 Configuration
	"""

	_SDM_NAME = 'ldpRootRangeV4'

	def __init__(self, parent):
		super(LdpRootRangeV4, self).__init__(parent)

	def LdpTLVList(self, DescriptiveName=None, Name=None):
		"""Gets child instances of LdpTLVList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of LdpTLVList will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptlvlist.LdpTLVList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldptlvlist import LdpTLVList
		return self._select(LdpTLVList(self), locals())

	@property
	def ContinuousIncrementOVAcrossRoot(self):
		"""Continuous Increment Opaque Value Across Root

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('continuousIncrementOVAcrossRoot')

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
	def FilterOnGroupAddress(self):
		"""If selected, all the LSPs will belong to the same set of groups

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('filterOnGroupAddress')

	@property
	def GroupCountPerLSP(self):
		"""Group Count Per LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupCountPerLSP')

	@property
	def LspCountPerRoot(self):
		"""LSP Count Per Root

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lspCountPerRoot')

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
	def NumberOfTLVs(self):
		"""Number Of TLVs

		Returns:
			number
		"""
		return self._get_attribute('numberOfTLVs')
	@NumberOfTLVs.setter
	def NumberOfTLVs(self, value):
		self._set_attribute('numberOfTLVs', value)

	@property
	def RootAddress(self):
		"""Root Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rootAddress')

	@property
	def RootAddressCount(self):
		"""Root Address Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rootAddressCount')

	@property
	def RootAddressStep(self):
		"""Root Address Step

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rootAddressStep')

	@property
	def SourceAddressV4(self):
		"""IPv4 Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceAddressV4')

	@property
	def SourceAddressV6(self):
		"""IPv6 Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceAddressV6')

	@property
	def SourceCountPerLSP(self):
		"""Source Count Per LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceCountPerLSP')

	@property
	def StartGroupAddressV4(self):
		"""Start Group Address(V4)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startGroupAddressV4')

	@property
	def StartGroupAddressV6(self):
		"""Start Group Address(V6)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startGroupAddressV6')

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
