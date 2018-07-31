from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Row(Base):
	"""A row view of learned information.
	"""

	_SDM_NAME = 'row'

	def __init__(self, parent):
		super(Row, self).__init__(parent)

	@property
	def Value(self):
		"""A learned information value

		Returns:
			str
		"""
		return self._get_attribute('value')

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
