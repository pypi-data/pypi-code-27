from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetTopologyGrid(Base):
	"""grid topology
	"""

	_SDM_NAME = 'netTopologyGrid'

	def __init__(self, parent):
		super(NetTopologyGrid, self).__init__(parent)

	@property
	def Columns(self):
		"""number of columns

		Returns:
			number
		"""
		return self._get_attribute('columns')
	@Columns.setter
	def Columns(self, value):
		self._set_attribute('columns', value)

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
	def Rows(self):
		"""number of rows

		Returns:
			number
		"""
		return self._get_attribute('rows')
	@Rows.setter
	def Rows(self, value):
		self._set_attribute('rows', value)

	def remove(self):
		"""Deletes a child instance of NetTopologyGrid on the server.

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
