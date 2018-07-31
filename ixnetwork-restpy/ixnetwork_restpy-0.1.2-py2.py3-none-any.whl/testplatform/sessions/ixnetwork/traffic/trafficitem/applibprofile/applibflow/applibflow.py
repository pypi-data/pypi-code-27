from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AppLibFlow(Base):
	"""This object specifies the particular application library flow related properties.
	"""

	_SDM_NAME = 'appLibFlow'

	def __init__(self, parent):
		super(AppLibFlow, self).__init__(parent)

	def Connection(self):
		"""Gets child instances of Connection from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Connection will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.connection.Connection))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.connection import Connection
		return self._select(Connection(self), locals())

	def Parameter(self, DisplayValue=None):
		"""Gets child instances of Parameter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Parameter will be returned.

		Args:
			DisplayValue (str): Current parameter UI Display Value

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.parameter.parameter.Parameter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.parameter.parameter import Parameter
		return self._select(Parameter(self), locals())

	@property
	def ConfigId(self):
		"""The internal config id asociated with this flow.

		Returns:
			number
		"""
		return self._get_attribute('configId')

	@property
	def ConnectionCount(self):
		"""Number of connections in this flow.

		Returns:
			number
		"""
		return self._get_attribute('connectionCount')

	@property
	def Description(self):
		"""Brief description of what the flow does.

		Returns:
			str
		"""
		return self._get_attribute('description')

	@property
	def FlowId(self):
		"""The identifier of the flow.

		Returns:
			str
		"""
		return self._get_attribute('flowId')

	@property
	def FlowSize(self):
		"""The size of the flow in bytes.

		Returns:
			number
		"""
		return self._get_attribute('flowSize')

	@property
	def Name(self):
		"""the name of the Flow.

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def Parameters(self):
		"""Array containing configurable parameters per flow.

		Returns:
			list(str)
		"""
		return self._get_attribute('parameters')

	@property
	def Percentage(self):
		"""The amount of traffic generated for this flows.

		Returns:
			number
		"""
		return self._get_attribute('percentage')
	@Percentage.setter
	def Percentage(self, value):
		self._set_attribute('percentage', value)
