from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ixnet(Base):
	"""This node tracks remote clients connected using the ixNet Service. Each client connection is being transported over an https websocket.
	"""

	_SDM_NAME = 'ixnet'

	def __init__(self, parent):
		super(Ixnet, self).__init__(parent)

	@property
	def ConnectedClients(self):
		"""Returns the remote address and remote port for each of the currently connected ixNet clients.

		Returns:
			list(str)
		"""
		return self._get_attribute('connectedClients')

	@property
	def IsActive(self):
		"""Returns true if any remote clients are connected, false if no remote clients are connected.

		Returns:
			bool
		"""
		return self._get_attribute('isActive')
