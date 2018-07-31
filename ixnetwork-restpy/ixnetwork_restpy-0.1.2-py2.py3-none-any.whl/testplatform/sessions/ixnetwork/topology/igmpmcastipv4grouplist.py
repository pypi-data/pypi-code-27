from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IgmpMcastIPv4GroupList(Base):
	"""IGMP Multicast IPv4 Groups
	"""

	_SDM_NAME = 'igmpMcastIPv4GroupList'

	def __init__(self, parent):
		super(IgmpMcastIPv4GroupList, self).__init__(parent)

	@property
	def IgmpUcastIPv4SourceList(self):
		"""Returns the one and only one IgmpUcastIPv4SourceList object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmpucastipv4sourcelist.IgmpUcastIPv4SourceList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.igmpucastipv4sourcelist import IgmpUcastIPv4SourceList
		return self._read(IgmpUcastIPv4SourceList(self), None)

	def Tag(self, Name=None):
		"""Gets child instances of Tag from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Tag will be returned.

		Args:
			Name (str): specifies the name of the tag the entity will be part of

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return self._select(Tag(self), locals())

	def add_Tag(self, Enabled="False", Name=None):
		"""Adds a child instance of Tag on the server.

		Args:
			Enabled (bool): Enables/disables tags
			Name (str): specifies the name of the tag the entity will be part of

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return self._create(Tag(self), locals())

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
	def McastAddrCnt(self):
		"""Multicast Address Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mcastAddrCnt')

	@property
	def McastAddrIncr(self):
		"""Multicast Address Increment

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mcastAddrIncr')

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
	def NoOfSrcRanges(self):
		"""Sources per Multicast Group (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('noOfSrcRanges')
	@NoOfSrcRanges.setter
	def NoOfSrcRanges(self, value):
		self._set_attribute('noOfSrcRanges', value)

	@property
	def SourceMode(self):
		"""Specifies the IGMP/MLD Source Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceMode')

	@property
	def StartMcastAddr(self):
		"""Start Multicast Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('startMcastAddr')

	@property
	def State(self):
		"""Indicates the state of the groups in the range

		Returns:
			list(str[iptv|joined|notJoined|notStarted])
		"""
		return self._get_attribute('state')

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

	def IgmpJoinGroup(self, Arg1):
		"""Executes the igmpJoinGroup operation on the server.

		Join Group

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpMcastIPv4GroupList object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpJoinGroup', payload=locals(), response_object=None)

	def IgmpJoinGroup(self, Arg1, SessionIndices):
		"""Executes the igmpJoinGroup operation on the server.

		Join Group

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpMcastIPv4GroupList object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpJoinGroup', payload=locals(), response_object=None)

	def IgmpJoinGroup(self, Arg1, SessionIndices):
		"""Executes the igmpJoinGroup operation on the server.

		Join Group

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpMcastIPv4GroupList object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpJoinGroup', payload=locals(), response_object=None)

	def IgmpLeaveGroup(self, Arg1):
		"""Executes the igmpLeaveGroup operation on the server.

		Leave Group

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpMcastIPv4GroupList object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpLeaveGroup', payload=locals(), response_object=None)

	def IgmpLeaveGroup(self, Arg1, SessionIndices):
		"""Executes the igmpLeaveGroup operation on the server.

		Leave Group

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpMcastIPv4GroupList object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpLeaveGroup', payload=locals(), response_object=None)

	def IgmpLeaveGroup(self, Arg1, SessionIndices):
		"""Executes the igmpLeaveGroup operation on the server.

		Leave Group

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./igmpMcastIPv4GroupList object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('igmpLeaveGroup', payload=locals(), response_object=None)

	def Join(self, Arg2):
		"""Executes the join operation on the server.

		Sends a Join on selected Group Ranges

		Args:
			Arg2 (list(number)): List of indices into the group range grid

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

		Sends a Leave on selected Group Ranges

		Args:
			Arg2 (list(number)): List of indices into the group range grid

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('leave', payload=locals(), response_object=None)
