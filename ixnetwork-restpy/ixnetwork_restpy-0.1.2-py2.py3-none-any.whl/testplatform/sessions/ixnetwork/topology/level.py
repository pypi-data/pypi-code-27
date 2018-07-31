from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Level(Base):
	"""Fat Tree Topology - Per Level Info
	"""

	_SDM_NAME = 'level'

	def __init__(self, parent):
		super(Level, self).__init__(parent)

	@property
	def NodeCount(self):
		"""Number of Nodes Per Level

		Returns:
			number
		"""
		return self._get_attribute('nodeCount')
	@NodeCount.setter
	def NodeCount(self, value):
		self._set_attribute('nodeCount', value)

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
