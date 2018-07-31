from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ExternalLink(Base):
	"""Links to NetTopologies with each other
	"""

	_SDM_NAME = 'externalLink'

	def __init__(self, parent):
		super(ExternalLink, self).__init__(parent)

	@property
	def FromNodeIndex(self):
		"""Index of the originating node as defined in fromNetworkTopology

		Returns:
			number
		"""
		return self._get_attribute('fromNodeIndex')
	@FromNodeIndex.setter
	def FromNodeIndex(self, value):
		self._set_attribute('fromNodeIndex', value)

	@property
	def ToNetworkTopology(self):
		"""Network Topology this link is pointing to

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)
		"""
		return self._get_attribute('toNetworkTopology')
	@ToNetworkTopology.setter
	def ToNetworkTopology(self, value):
		self._set_attribute('toNetworkTopology', value)

	@property
	def ToNodeIndex(self):
		"""Index of the target node as defined in toNetworkTopology

		Returns:
			number
		"""
		return self._get_attribute('toNodeIndex')
	@ToNodeIndex.setter
	def ToNodeIndex(self, value):
		self._set_attribute('toNodeIndex', value)

	def remove(self):
		"""Deletes a child instance of ExternalLink on the server.

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
