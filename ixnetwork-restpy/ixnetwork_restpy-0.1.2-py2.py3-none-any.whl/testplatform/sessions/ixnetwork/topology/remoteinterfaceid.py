from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RemoteInterfaceId(Base):
	"""
	"""

	_SDM_NAME = 'remoteInterfaceId'

	def __init__(self, parent):
		super(RemoteInterfaceId, self).__init__(parent)

	@property
	def Count(self):
		"""total number of values

		Returns:
			number
		"""
		return self._get_attribute('count')

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
