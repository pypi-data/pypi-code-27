from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Egress(Base):
	"""
	"""

	_SDM_NAME = 'egress'

	def __init__(self, parent):
		super(Egress, self).__init__(parent)

	def FlowCondition(self):
		"""Gets child instances of FlowCondition from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of FlowCondition will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.egress.flowcondition.flowcondition.FlowCondition))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.egress.flowcondition.flowcondition import FlowCondition
		return self._select(FlowCondition(self), locals())

	def add_FlowCondition(self, Operator=None, ShowFirstMatchingSet=None, TrackingFilterId=None, Values=None):
		"""Adds a child instance of FlowCondition on the server.

		Args:
			Operator (str(isBetween|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isSmaller)): 
			ShowFirstMatchingSet (bool): 
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): 
			Values (list(number)): 

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.egress.flowcondition.flowcondition.FlowCondition)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.data.egress.flowcondition.flowcondition import FlowCondition
		return self._create(FlowCondition(self), locals())

	@property
	def CommitEgressPage(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('commitEgressPage')
	@CommitEgressPage.setter
	def CommitEgressPage(self, value):
		self._set_attribute('commitEgressPage', value)

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
	def RowCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('rowCount')

	@property
	def TotalPages(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('totalPages')
