from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Layer23ProtocolAuthAccessFilter(Base):
	"""Filters associated with layer23ProtocolAuthaccess view.
	"""

	_SDM_NAME = 'layer23ProtocolAuthAccessFilter'

	def __init__(self, parent):
		super(Layer23ProtocolAuthAccessFilter, self).__init__(parent)

	@property
	def PortFilterIds(self):
		"""Ports that have been filtered.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])
		"""
		return self._get_attribute('portFilterIds')
	@PortFilterIds.setter
	def PortFilterIds(self, value):
		self._set_attribute('portFilterIds', value)

	@property
	def ProtocolFilterIds(self):
		"""Protocols that have been filtered.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolFilter])
		"""
		return self._get_attribute('protocolFilterIds')
	@ProtocolFilterIds.setter
	def ProtocolFilterIds(self, value):
		self._set_attribute('protocolFilterIds', value)

	def remove(self):
		"""Deletes a child instance of Layer23ProtocolAuthAccessFilter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
