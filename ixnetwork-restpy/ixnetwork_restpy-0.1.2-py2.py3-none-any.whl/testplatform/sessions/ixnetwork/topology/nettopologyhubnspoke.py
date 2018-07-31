from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetTopologyHubNSpoke(Base):
	"""hub-n-spoke topology
	"""

	_SDM_NAME = 'netTopologyHubNSpoke'

	def __init__(self, parent):
		super(NetTopologyHubNSpoke, self).__init__(parent)

	@property
	def EnableLevel2Spokes(self):
		"""Enable Level 2 Spokes

		Returns:
			bool
		"""
		return self._get_attribute('enableLevel2Spokes')
	@EnableLevel2Spokes.setter
	def EnableLevel2Spokes(self, value):
		self._set_attribute('enableLevel2Spokes', value)

	@property
	def IncludeEntryPoint(self):
		"""if true, entry node belongs to ring topology, otherwise it is outside of ring

		Returns:
			bool
		"""
		return self._get_attribute('includeEntryPoint')
	@IncludeEntryPoint.setter
	def IncludeEntryPoint(self, value):
		self._set_attribute('includeEntryPoint', value)

	@property
	def LinkMultiplier(self):
		"""number of links between two nodes

		Returns:
			number
		"""
		return self._get_attribute('linkMultiplier')
	@LinkMultiplier.setter
	def LinkMultiplier(self, value):
		self._set_attribute('linkMultiplier', value)

	@property
	def NumberOfFirstLevelSpokes(self):
		"""Number of First Level Spokes

		Returns:
			number
		"""
		return self._get_attribute('numberOfFirstLevelSpokes')
	@NumberOfFirstLevelSpokes.setter
	def NumberOfFirstLevelSpokes(self, value):
		self._set_attribute('numberOfFirstLevelSpokes', value)

	@property
	def NumberOfSecondLevelSpokes(self):
		"""Number of Second Level Spokes

		Returns:
			number
		"""
		return self._get_attribute('numberOfSecondLevelSpokes')
	@NumberOfSecondLevelSpokes.setter
	def NumberOfSecondLevelSpokes(self, value):
		self._set_attribute('numberOfSecondLevelSpokes', value)

	def remove(self):
		"""Deletes a child instance of NetTopologyHubNSpoke on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

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
