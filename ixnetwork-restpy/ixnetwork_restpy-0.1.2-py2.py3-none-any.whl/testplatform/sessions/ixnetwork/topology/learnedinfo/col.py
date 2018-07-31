from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Col(Base):
	"""A column view of learned information.
	"""

	_SDM_NAME = 'col'

	def __init__(self, parent):
		super(Col, self).__init__(parent)

	def CellTable(self, Type=None):
		"""Gets child instances of CellTable from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of CellTable will be returned.

		Args:
			Type (str): Description of the learned information type

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.celltable.CellTable))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.celltable import CellTable
		return self._select(CellTable(self), locals())

	def Row(self, Value=None):
		"""Gets child instances of Row from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Row will be returned.

		Args:
			Value (str): A learned information value

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.row.Row))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.row import Row
		return self._select(Row(self), locals())

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
