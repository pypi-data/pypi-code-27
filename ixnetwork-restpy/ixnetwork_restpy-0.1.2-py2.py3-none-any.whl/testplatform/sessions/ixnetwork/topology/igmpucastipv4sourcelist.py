from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IgmpUcastIPv4SourceList(Base):
	"""IGMP Unicast IPv4 Source
	"""

	_SDM_NAME = 'igmpUcastIPv4SourceList'

	def __init__(self, parent):
		super(IgmpUcastIPv4SourceList, self).__init__(parent)

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
	def StartUcastAddr(self):
		"""Start Multicast Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startUcastAddr')

	@property
	def State(self):
		"""Indicates the state of the groups in the range

		Returns:
			list(str[iptv|joined|notJoined|notStarted])
		"""
		return self._get_attribute('state')

	@property
	def UcastAddrIncr(self):
		"""Source Address Increment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ucastAddrIncr')

	@property
	def UcastSrcAddrCnt(self):
		"""Source Address Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ucastSrcAddrCnt')

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

	def IgmpJoinSource(self, Arg1):
		"""Executes the igmpJoinSource operation on the server.

		Join Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpUcastIPv4SourceList object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpJoinSource', payload=locals(), response_object=None)

	def IgmpJoinSource(self, Arg1, SessionIndices):
		"""Executes the igmpJoinSource operation on the server.

		Join Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpUcastIPv4SourceList object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpJoinSource', payload=locals(), response_object=None)

	def IgmpJoinSource(self, Arg1, SessionIndices):
		"""Executes the igmpJoinSource operation on the server.

		Join Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpUcastIPv4SourceList object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpJoinSource', payload=locals(), response_object=None)

	def IgmpLeaveSource(self, Arg1):
		"""Executes the igmpLeaveSource operation on the server.

		Leave Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpUcastIPv4SourceList object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpLeaveSource', payload=locals(), response_object=None)

	def IgmpLeaveSource(self, Arg1, SessionIndices):
		"""Executes the igmpLeaveSource operation on the server.

		Leave Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpUcastIPv4SourceList object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpLeaveSource', payload=locals(), response_object=None)

	def IgmpLeaveSource(self, Arg1, SessionIndices):
		"""Executes the igmpLeaveSource operation on the server.

		Leave Source

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpUcastIPv4SourceList object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpLeaveSource', payload=locals(), response_object=None)

	def Join(self, Arg2):
		"""Executes the join operation on the server.

		Sends a Join on selected Source Ranges

		Args:
			Arg2 (list(number)): List of indices into the source range grid

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('join', payload=locals(), response_object=None)

	def Leave(self, Arg2):
		"""Executes the leave operation on the server.

		Sends a Leave on selected Source Range

		Args:
			Arg2 (list(number)): List of indices into the source range grid

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('leave', payload=locals(), response_object=None)
