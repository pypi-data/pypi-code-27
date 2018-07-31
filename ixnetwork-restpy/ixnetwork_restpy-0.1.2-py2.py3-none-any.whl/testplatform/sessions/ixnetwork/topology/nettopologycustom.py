from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetTopologyCustom(Base):
	"""Custom, user defined topology.
	"""

	_SDM_NAME = 'netTopologyCustom'

	def __init__(self, parent):
		super(NetTopologyCustom, self).__init__(parent)

	@property
	def LinkTable(self):
		"""Returns the one and only one LinkTable object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.linktable.LinkTable)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.linktable import LinkTable
		return self._read(LinkTable(self), None)

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
	def NumberOfNodes(self):
		"""Number Of Nodes

		Returns:
			number
		"""
		return self._get_attribute('numberOfNodes')

	def remove(self):
		"""Deletes a child instance of NetTopologyCustom on the server.

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
