from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DiscoveredNeighbor(Base):
	"""This object holds the discoverd neighbor information for the virtual port.
	"""

	_SDM_NAME = 'discoveredNeighbor'

	def __init__(self, parent):
		super(DiscoveredNeighbor, self).__init__(parent)

	@property
	def IsRouter(self):
		"""(read only) Indicates if the neighbor is a router or not.

		Returns:
			str
		"""
		return self._get_attribute('isRouter')

	@property
	def LastUpdate(self):
		"""(read only) Indicates when the last update for the neighbor happened.

		Returns:
			str
		"""
		return self._get_attribute('lastUpdate')

	@property
	def NeighborIp(self):
		"""(read only) The IP address of the neighbor.

		Returns:
			str
		"""
		return self._get_attribute('neighborIp')

	@property
	def NeighborMac(self):
		"""(read only) The MAC address of the neighbor.

		Returns:
			str
		"""
		return self._get_attribute('neighborMac')

	def remove(self):
		"""Deletes a child instance of DiscoveredNeighbor on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
