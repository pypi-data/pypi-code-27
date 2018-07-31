from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Egress(Base):
	"""SV settings for egress traking display. (fixed list, based on number of ingress rows)
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
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.egress.flowcondition.flowcondition.FlowCondition))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.egress.flowcondition.flowcondition import FlowCondition
		return self._select(FlowCondition(self), locals())

	def add_FlowCondition(self, Operator="isEqual", ShowFirstMatchingSet="False", TrackingFilterId=None, Values=None):
		"""Adds a child instance of FlowCondition on the server.

		Args:
			Operator (str(isBetween|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isSmaller)): The logical operation to be performed.
			ShowFirstMatchingSet (bool): If true, displays the first matching set.
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): Selected tracking filters from the availableTrackingFilter list.
			Values (list(number)): Value to be matched for the condition.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.egress.flowcondition.flowcondition.FlowCondition)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.page.egress.flowcondition.flowcondition import FlowCondition
		return self._create(FlowCondition(self), locals())

	@property
	def CommitEgressPage(self):
		"""Attribute used to commit egress paging from TCL

		Returns:
			bool
		"""
		return self._get_attribute('commitEgressPage')
	@CommitEgressPage.setter
	def CommitEgressPage(self, value):
		self._set_attribute('commitEgressPage', value)

	@property
	def CurrentPage(self):
		"""Determines the current egress page for the indicated ingress page.

		Returns:
			number
		"""
		return self._get_attribute('currentPage')
	@CurrentPage.setter
	def CurrentPage(self, value):
		self._set_attribute('currentPage', value)

	@property
	def RowCount(self):
		"""Displays the particular row number in the view.

		Returns:
			number
		"""
		return self._get_attribute('rowCount')

	@property
	def TotalPages(self):
		"""The total number of egress pages.

		Returns:
			number
		"""
		return self._get_attribute('totalPages')
