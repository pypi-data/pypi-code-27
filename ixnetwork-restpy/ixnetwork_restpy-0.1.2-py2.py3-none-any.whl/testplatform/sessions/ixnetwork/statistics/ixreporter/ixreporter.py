from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ixreporter(Base):
	"""Specifies the statistics for IxReporter.
	"""

	_SDM_NAME = 'ixreporter'

	def __init__(self, parent):
		super(Ixreporter, self).__init__(parent)

	@property
	def DataCollection(self):
		"""Returns the one and only one DataCollection object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.datacollection.datacollection.DataCollection)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.datacollection.datacollection import DataCollection
		return self._read(DataCollection(self), None)

	@property
	def ReportGeneration(self):
		"""Returns the one and only one ReportGeneration object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.reportgeneration.reportgeneration.ReportGeneration)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.ixreporter.reportgeneration.reportgeneration import ReportGeneration
		return self._read(ReportGeneration(self), None)
