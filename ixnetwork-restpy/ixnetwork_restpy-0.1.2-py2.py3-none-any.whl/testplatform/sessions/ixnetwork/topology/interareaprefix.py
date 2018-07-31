from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class InterAreaPrefix(Base):
	"""Simulated Router Information
	"""

	_SDM_NAME = 'interAreaPrefix'

	def __init__(self, parent):
		super(InterAreaPrefix, self).__init__(parent)

	@property
	def Active(self):
		"""Whether this is to be advertised or not

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def LABit(self):
		"""Options-LA Bit(Local Address)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lABit')

	@property
	def LinkStateId(self):
		"""Link State Id of the simulated IPv6 network

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('linkStateId')

	@property
	def LinkStateIdStep(self):
		"""Link State Id Step for the LSAs to be generated for this set of IPv6 Inter-Area networks.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('linkStateIdStep')

	@property
	def MCBit(self):
		"""Options-MC Bit(Multicast)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mCBit')

	@property
	def Metric(self):
		"""Metric

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metric')

	@property
	def NUBit(self):
		"""Options-NU Bit(No Unicast)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nUBit')

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
	def NetworkAddress(self):
		"""Prefixes of the simulated IPv6 network

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('networkAddress')

	@property
	def PBit(self):
		"""Options-P Bit(Propagate)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pBit')

	@property
	def Prefix(self):
		"""Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefix')

	@property
	def RangeSize(self):
		"""Range Size

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rangeSize')

	@property
	def UnusedBit4(self):
		"""Options-(4)Unused

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('unusedBit4')

	@property
	def UnusedBit5(self):
		"""Options-(5)Unused

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('unusedBit5')

	@property
	def UnusedBit6(self):
		"""Options-(6)Unused

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('unusedBit6')

	@property
	def UnusedBit7(self):
		"""Options-(7)Unused

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('unusedBit7')

	def Advertise(self, Arg1):
		"""Executes the advertise operation on the server.

		Advertise selected routes

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./interAreaPrefix object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('advertise', payload=locals(), response_object=None)

	def Advertise(self, Arg1, SessionIndices):
		"""Executes the advertise operation on the server.

		Advertise selected routes

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./interAreaPrefix object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('advertise', payload=locals(), response_object=None)

	def Advertise(self, Arg1, SessionIndices):
		"""Executes the advertise operation on the server.

		Advertise selected routes

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./interAreaPrefix object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('advertise', payload=locals(), response_object=None)

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

	def Start(self, Targets):
		"""Executes the start operation on the server.

		Start CPF control plane (equals to promote to negotiated state).

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./interAreaPrefix object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Targets):
		"""Executes the stop operation on the server.

		Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./interAreaPrefix object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Withdraw(self, Arg1):
		"""Executes the withdraw operation on the server.

		Withdraw selected routes

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./interAreaPrefix object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('withdraw', payload=locals(), response_object=None)

	def Withdraw(self, Arg1, SessionIndices):
		"""Executes the withdraw operation on the server.

		Withdraw selected routes

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./interAreaPrefix object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('withdraw', payload=locals(), response_object=None)

	def Withdraw(self, Arg1, SessionIndices):
		"""Executes the withdraw operation on the server.

		Withdraw selected routes

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./interAreaPrefix object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('withdraw', payload=locals(), response_object=None)
