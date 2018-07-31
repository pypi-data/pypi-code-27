from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetTopologyMesh(Base):
	"""mesh topology
	"""

	_SDM_NAME = 'netTopologyMesh'

	def __init__(self, parent):
		super(NetTopologyMesh, self).__init__(parent)

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
	def Nodes(self):
		"""number of nodes

		Returns:
			number
		"""
		return self._get_attribute('nodes')
	@Nodes.setter
	def Nodes(self, value):
		self._set_attribute('nodes', value)

	def remove(self):
		"""Deletes a child instance of NetTopologyMesh on the server.

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
