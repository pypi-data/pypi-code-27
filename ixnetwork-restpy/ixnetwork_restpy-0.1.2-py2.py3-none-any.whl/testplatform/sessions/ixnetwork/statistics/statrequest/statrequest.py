from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class StatRequest(Base):
	"""Requests for specific statistical data.
	"""

	_SDM_NAME = 'statRequest'

	def __init__(self, parent):
		super(StatRequest, self).__init__(parent)

	def Pattern(self, FlowLabel=None):
		"""Gets child instances of Pattern from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Pattern will be returned.

		Args:
			FlowLabel (str): This corresponds to the name or the label given to each flow.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.statrequest.pattern.pattern.Pattern))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.statrequest.pattern.pattern import Pattern
		return self._select(Pattern(self), locals())

	def add_Pattern(self, FlowLabel=""):
		"""Adds a child instance of Pattern on the server.

		Args:
			FlowLabel (str): This corresponds to the name or the label given to each flow.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.statrequest.pattern.pattern.Pattern)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.statrequest.pattern.pattern import Pattern
		return self._create(Pattern(self), locals())

	@property
	def Filter(self):
		"""The Statistics filter

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=*)
		"""
		return self._get_attribute('filter')
	@Filter.setter
	def Filter(self, value):
		self._set_attribute('filter', value)

	@property
	def FilterItems(self):
		"""A list of filter items.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=*])
		"""
		return self._get_attribute('filterItems')
	@FilterItems.setter
	def FilterItems(self, value):
		self._set_attribute('filterItems', value)

	@property
	def IsReady(self):
		"""If true, the counter is ready to record statistics.

		Returns:
			bool
		"""
		return self._get_attribute('isReady')

	@property
	def MaxWaitTime(self):
		"""Value indicates the maximum wait time.

		Returns:
			number
		"""
		return self._get_attribute('maxWaitTime')
	@MaxWaitTime.setter
	def MaxWaitTime(self, value):
		self._set_attribute('maxWaitTime', value)

	@property
	def Source(self):
		"""The source for the statistical data.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=*)
		"""
		return self._get_attribute('source')
	@Source.setter
	def Source(self, value):
		self._set_attribute('source', value)

	@property
	def Stats(self):
		"""The statistics displayed.

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=*],arg2:str[average|averageRate|countDistinct|delta|divSum|first|intervalAverage|max|maxRate|min|minRate|none|positiveAverageRate|positiveMaxRate|positiveMinRate|positiveRate|rate|runStateAgg|runStateAggIgnoreRamp|standardDeviation|sum|vectorMax|vectorMin|weightedAverage]))
		"""
		return self._get_attribute('stats')
	@Stats.setter
	def Stats(self, value):
		self._set_attribute('stats', value)

	@property
	def Values(self):
		"""The values of the statistics data.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/vport?deepchild=*])
		"""
		return self._get_attribute('values')

	def remove(self):
		"""Deletes a child instance of StatRequest on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def GetStats(self):
		"""Executes the getStats operation on the server.

		Retreives the requested statistical data.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getStats', payload=locals(), response_object=None)
