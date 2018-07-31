from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Data(Base):
	"""
	"""

	_SDM_NAME = 'data'

	def __init__(self, parent):
		super(Data, self).__init__(parent)

	def Egress(self):
		"""Gets child instances of Egress from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Egress will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.egress.egress.Egress))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.egress.egress import Egress
		return self._select(Egress(self), locals())

	@property
	def EgressRxCondition(self):
		"""Returns the one and only one EgressRxCondition object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.egressrxcondition.egressrxcondition.EgressRxCondition)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.egressrxcondition.egressrxcondition import EgressRxCondition
		return self._read(EgressRxCondition(self), None)

	@property
	def AllowPaging(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('allowPaging')

	@property
	def ColumnCaptions(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('columnCaptions')

	@property
	def ColumnCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('columnCount')

	@property
	def CurrentPage(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('currentPage')
	@CurrentPage.setter
	def CurrentPage(self, value):
		self._set_attribute('currentPage', value)

	@property
	def EgressMode(self):
		"""

		Returns:
			str(conditional|paged)
		"""
		return self._get_attribute('egressMode')
	@EgressMode.setter
	def EgressMode(self, value):
		self._set_attribute('egressMode', value)

	@property
	def EgressPageSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('egressPageSize')
	@EgressPageSize.setter
	def EgressPageSize(self, value):
		self._set_attribute('egressPageSize', value)

	@property
	def IsBlocked(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isBlocked')

	@property
	def IsReady(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isReady')

	@property
	def PageSize(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('pageSize')
	@PageSize.setter
	def PageSize(self, value):
		self._set_attribute('pageSize', value)

	@property
	def PageValues(self):
		"""Returns the values in the current page. The ingress row is grouped with its corresponding egress rows

		Returns:
			list(list[list[str]])
		"""
		return self._get_attribute('pageValues')

	@property
	def RowCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rowCount')

	@property
	def RowValues(self):
		"""

		Returns:
			dict(arg1:list[list[list[str]]])
		"""
		return self._get_attribute('rowValues')

	@property
	def Timestamp(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('timestamp')

	@property
	def TotalPages(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('totalPages')

	@property
	def TotalRows(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('totalRows')
