from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IsisL3SimulatedTopologyConfig(Base):
	"""ISIS-L3 Simulated Topology Configuration
	"""

	_SDM_NAME = 'isisL3SimulatedTopologyConfig'

	def __init__(self, parent):
		super(IsisL3SimulatedTopologyConfig, self).__init__(parent)

	@property
	def IsisL3ipv4NodeRouteList(self):
		"""Returns the one and only one IsisL3ipv4NodeRouteList object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3ipv4noderoutelist.IsisL3ipv4NodeRouteList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3ipv4noderoutelist import IsisL3ipv4NodeRouteList
		return self._read(IsisL3ipv4NodeRouteList(self), None)

	@property
	def IsisL3ipv6NodeRouteList(self):
		"""Returns the one and only one IsisL3ipv6NodeRouteList object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3ipv6noderoutelist.IsisL3ipv6NodeRouteList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3ipv6noderoutelist import IsisL3ipv6NodeRouteList
		return self._read(IsisL3ipv6NodeRouteList(self), None)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

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
	def EnableHostName(self):
		"""Enable Host Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableHostName')

	@property
	def HostName(self):
		"""Host Name

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hostName')

	@property
	def IsisL3Ipv4NodeRouteCount(self):
		"""Node Route Range Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('isisL3Ipv4NodeRouteCount')
	@IsisL3Ipv4NodeRouteCount.setter
	def IsisL3Ipv4NodeRouteCount(self, value):
		self._set_attribute('isisL3Ipv4NodeRouteCount', value)

	@property
	def IsisL3Ipv6NodeRouteCount(self):
		"""Node Route Range Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('isisL3Ipv6NodeRouteCount')
	@IsisL3Ipv6NodeRouteCount.setter
	def IsisL3Ipv6NodeRouteCount(self, value):
		self._set_attribute('isisL3Ipv6NodeRouteCount', value)

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

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start Isis Simulated Topology

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisL3SimulatedTopologyConfig object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start Isis Simulated Topology

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisL3SimulatedTopologyConfig object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start Isis Simulated Topology

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisL3SimulatedTopologyConfig object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Stop Isis Simulated Topology

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisL3SimulatedTopologyConfig object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop Isis Simulated Topology

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisL3SimulatedTopologyConfig object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop Isis Simulated Topology

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisL3SimulatedTopologyConfig object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
