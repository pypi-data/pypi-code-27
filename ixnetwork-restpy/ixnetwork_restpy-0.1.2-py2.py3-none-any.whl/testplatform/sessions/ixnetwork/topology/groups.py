from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Groups(Base):
	"""Openflow Groups Configuration
	"""

	_SDM_NAME = 'groups'

	def __init__(self, parent):
		super(Groups, self).__init__(parent)

	def Buckets(self, DescriptiveName=None, GroupName=None, Name=None):
		"""Gets child instances of Buckets from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Buckets will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			GroupName (str): Parent Group Name
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.buckets.Buckets))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.buckets import Buckets
		return self._select(Buckets(self), locals())

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def ChannelName(self):
		"""Parent Channel Name

		Returns:
			str
		"""
		return self._get_attribute('channelName')

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
	def GroupAdvertise(self):
		"""If selected, group is advertised when the OpenFlow channel comes up.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupAdvertise')

	@property
	def GroupDescription(self):
		"""A description of the group.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupDescription')

	@property
	def GroupId(self):
		"""A 32-bit integer uniquely identifying the group.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupId')

	@property
	def GroupType(self):
		"""Select the type of group to determine the group semantics.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupType')

	@property
	def Multiplier(self):
		"""Number of instances per parent instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

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
	def NumberOfBuckets(self):
		"""Specify the number of Buckets.

		Returns:
			number
		"""
		return self._get_attribute('numberOfBuckets')
	@NumberOfBuckets.setter
	def NumberOfBuckets(self, value):
		self._set_attribute('numberOfBuckets', value)

	@property
	def OfChannel(self):
		"""The OF Channel to which the group belongs.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ofChannel')

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

	def SendAllGroupAdd(self):
		"""Executes the sendAllGroupAdd operation on the server.

		Sends a Group Add on all groups.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendAllGroupAdd', payload=locals(), response_object=None)

	def SendAllGroupRemove(self):
		"""Executes the sendAllGroupRemove operation on the server.

		Sends a Group Remove on all groups.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendAllGroupRemove', payload=locals(), response_object=None)

	def SendGroupAdd(self, Arg2):
		"""Executes the sendGroupAdd operation on the server.

		Sends a Group Add on selected Group.

		Args:
			Arg2 (list(number)): List of indices into the group range grid

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendGroupAdd', payload=locals(), response_object=None)

	def SendGroupRemove(self, Arg2):
		"""Executes the sendGroupRemove operation on the server.

		Sends a Group Remove on selected Group.

		Args:
			Arg2 (list(number)): List of indices into the group range grid

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendGroupRemove', payload=locals(), response_object=None)
