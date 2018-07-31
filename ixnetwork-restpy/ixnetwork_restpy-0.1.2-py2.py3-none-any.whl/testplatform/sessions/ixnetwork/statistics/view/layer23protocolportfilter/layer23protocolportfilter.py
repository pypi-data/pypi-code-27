from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Layer23ProtocolPortFilter(Base):
	"""Filters associated with layer23ProtocolPort view.
	"""

	_SDM_NAME = 'layer23ProtocolPortFilter'

	def __init__(self, parent):
		super(Layer23ProtocolPortFilter, self).__init__(parent)

	@property
	def PortFilterIds(self):
		"""Selected port filters from the availablePortFilter list.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])
		"""
		return self._get_attribute('portFilterIds')
	@PortFilterIds.setter
	def PortFilterIds(self, value):
		self._set_attribute('portFilterIds', value)

	def remove(self):
		"""Deletes a child instance of Layer23ProtocolPortFilter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
