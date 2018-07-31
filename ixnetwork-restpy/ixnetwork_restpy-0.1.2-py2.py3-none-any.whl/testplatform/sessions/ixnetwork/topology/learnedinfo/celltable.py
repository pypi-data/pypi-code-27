from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CellTable(Base):
	"""The node where learned information is grouped into tables or columns and rows.
	"""

	_SDM_NAME = 'cellTable'

	def __init__(self, parent):
		super(CellTable, self).__init__(parent)

	def Col(self, Value=None):
		"""Gets child instances of Col from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Col will be returned.

		Args:
			Value (str): A learned information value

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.col.Col))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.col import Col
		return self._select(Col(self), locals())

	@property
	def Actions(self):
		"""The list of actions allowed on the learned information table

		Returns:
			list(str)
		"""
		return self._get_attribute('actions')

	@property
	def Columns(self):
		"""The list of columns in the learned information table

		Returns:
			list(str)
		"""
		return self._get_attribute('columns')

	@property
	def Type(self):
		"""Description of the learned information type

		Returns:
			str
		"""
		return self._get_attribute('type')

	@property
	def Values(self):
		"""A list of rows of learned information values

		Returns:
			list(list[str])
		"""
		return self._get_attribute('values')

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
