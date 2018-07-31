from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PcepMetricSubObjectsList(Base):
	"""
	"""

	_SDM_NAME = 'pcepMetricSubObjectsList'

	def __init__(self, parent):
		super(PcepMetricSubObjectsList, self).__init__(parent)

	@property
	def Active(self):
		"""Specifies whether the corresponding metric object is active or not.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def BFlag(self):
		"""B (bound) flag MUST be set in the METRIC object, which specifies that the SID depth for the computed path MUST NOT exceed the metric-value.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bFlag')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def MetricType(self):
		"""This is a drop down which has 4 choices: IGP/ TE/ Hop count/ MSD.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metricType')

	@property
	def MetricValue(self):
		"""User can specify the metric value corresponding to the metric type selected.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metricValue')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

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
