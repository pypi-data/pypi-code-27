from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LdpLeafRangeV6(Base):
	"""Ldp Targeted LeafRange V6 Configuration
	"""

	_SDM_NAME = 'ldpLeafRangeV6'

	def __init__(self, parent):
		super(LdpLeafRangeV6, self).__init__(parent)

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
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def GroupAddressV4(self):
		"""IPv4 Group Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupAddressV4')

	@property
	def GroupAddressV6(self):
		"""IPv6 Group Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupAddressV6')

	@property
	def GroupCountPerLsp(self):
		"""Group Count per LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupCountPerLsp')

	@property
	def LSPType(self):
		"""LSP Type

		Returns:
			str(p2MP)
		"""
		return self._get_attribute('lSPType')
	@LSPType.setter
	def LSPType(self, value):
		self._set_attribute('lSPType', value)

	@property
	def LabelValueStart(self):
		"""Label Value Start

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelValueStart')

	@property
	def LabelValueStep(self):
		"""Label Value Step

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelValueStep')

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

	def ActivateLeafRange(self, Arg1):
		"""Executes the activateLeafRange operation on the server.

		Activate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpLeafRangeV6 object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('activateLeafRange', payload=locals(), response_object=None)

	def ActivateLeafRange(self, Arg1, SessionIndices):
		"""Executes the activateLeafRange operation on the server.

		Activate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpLeafRangeV6 object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('activateLeafRange', payload=locals(), response_object=None)

	def ActivateLeafRange(self, Arg1, SessionIndices):
		"""Executes the activateLeafRange operation on the server.

		Activate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpLeafRangeV6 object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('activateLeafRange', payload=locals(), response_object=None)

	def ActivateLeafRange(self, Arg2):
		"""Executes the activateLeafRange operation on the server.

		Activate Multicast Leaf Range

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('activateLeafRange', payload=locals(), response_object=None)

	def DeactivateLeafRange(self, Arg1):
		"""Executes the deactivateLeafRange operation on the server.

		Deactivate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpLeafRangeV6 object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('deactivateLeafRange', payload=locals(), response_object=None)

	def DeactivateLeafRange(self, Arg1, SessionIndices):
		"""Executes the deactivateLeafRange operation on the server.

		Deactivate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpLeafRangeV6 object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('deactivateLeafRange', payload=locals(), response_object=None)

	def DeactivateLeafRange(self, Arg1, SessionIndices):
		"""Executes the deactivateLeafRange operation on the server.

		Deactivate Multicast Leaf Range

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpLeafRangeV6 object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('deactivateLeafRange', payload=locals(), response_object=None)

	def DeactivateLeafRange(self, Arg2):
		"""Executes the deactivateLeafRange operation on the server.

		Deactivate Multicast Leaf Range

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('deactivateLeafRange', payload=locals(), response_object=None)

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
