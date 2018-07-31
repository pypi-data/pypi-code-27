from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Connection(Base):
	"""This specifies the particular connection related properties.
	"""

	_SDM_NAME = 'connection'

	def __init__(self, parent):
		super(Connection, self).__init__(parent)

	def Parameter(self, DisplayValue=None):
		"""Gets child instances of Parameter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Parameter will be returned.

		Args:
			DisplayValue (str): Current parameter UI Display Value

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.parameter.Parameter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.connection.parameter.parameter import Parameter
		return self._select(Parameter(self), locals())

	@property
	def ConnectionId(self):
		"""(Read only) Application library flow connection id.

		Returns:
			number
		"""
		return self._get_attribute('connectionId')

	@property
	def ConnectionParams(self):
		"""(Read only) Names of parameter available on application flow connection.

		Returns:
			list(str)
		"""
		return self._get_attribute('connectionParams')

	@property
	def IsTCP(self):
		"""(Read only) Application library flow connection type - true is the type is TCP, false if it's UDP.

		Returns:
			bool
		"""
		return self._get_attribute('isTCP')
