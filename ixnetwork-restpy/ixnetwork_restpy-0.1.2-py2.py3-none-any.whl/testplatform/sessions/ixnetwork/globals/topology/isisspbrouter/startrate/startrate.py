from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class StartRate(Base):
	"""Parameters used for controlling the rate of actions
	"""

	_SDM_NAME = 'startRate'

	def __init__(self, parent):
		super(StartRate, self).__init__(parent)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def Enabled(self):
		"""Enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enabled')

	@property
	def Interval(self):
		"""The time interval in milliseconds during which the rate is calculated(rate = count/interval)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interval')

	@property
	def Rate(self):
		"""Number of times an action is triggered per time interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rate')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	@property
	def ScaleMode(self):
		"""Indicates whether the control is specified per port or per device group.

		Returns:
			str(deviceGroup|port)
		"""
		return self._get_attribute('scaleMode')
	@ScaleMode.setter
	def ScaleMode(self, value):
		self._set_attribute('scaleMode', value)

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
