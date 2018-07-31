from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LinkTable(Base):
	"""Topology Link Table. sizes of fromNodeIndex and toNodeIndex are the same.
	"""

	_SDM_NAME = 'linkTable'

	def __init__(self, parent):
		super(LinkTable, self).__init__(parent)

	@property
	def FromNodeIndex(self):
		"""from node index.

		Returns:
			list(str)
		"""
		return self._get_attribute('fromNodeIndex')
	@FromNodeIndex.setter
	def FromNodeIndex(self, value):
		self._set_attribute('fromNodeIndex', value)

	@property
	def ToNodeIndex(self):
		"""to node index.

		Returns:
			list(str)
		"""
		return self._get_attribute('toNodeIndex')
	@ToNodeIndex.setter
	def ToNodeIndex(self, value):
		self._set_attribute('toNodeIndex', value)

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
