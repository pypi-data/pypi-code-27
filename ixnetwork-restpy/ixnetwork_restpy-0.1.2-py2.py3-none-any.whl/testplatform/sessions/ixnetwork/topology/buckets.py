from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Buckets(Base):
	"""Bucket configuration
	"""

	_SDM_NAME = 'buckets'

	def __init__(self, parent):
		super(Buckets, self).__init__(parent)

	@property
	def ActionsProfile(self):
		"""Returns the one and only one ActionsProfile object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.actionsprofile.ActionsProfile)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.actionsprofile import ActionsProfile
		return self._read(ActionsProfile(self), None)

	@property
	def BucketDescription(self):
		"""A description for the bucket.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bucketDescription')

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
	def GroupIndex(self):
		"""Group Index

		Returns:
			list(str)
		"""
		return self._get_attribute('groupIndex')

	@property
	def GroupName(self):
		"""Parent Group Name

		Returns:
			str
		"""
		return self._get_attribute('groupName')

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
	def WatchGroup(self):
		"""A group whose state determines whether this bucket is live or not.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('watchGroup')

	@property
	def WatchPort(self):
		"""A Port whose state determines whether this bucket is live or not.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('watchPort')

	@property
	def Weight(self):
		"""Specify the weight of buckets. The permissible range is 0-65535.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('weight')

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
