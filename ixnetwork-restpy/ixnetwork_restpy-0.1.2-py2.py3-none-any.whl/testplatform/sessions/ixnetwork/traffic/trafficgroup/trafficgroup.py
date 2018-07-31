from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TrafficGroup(Base):
	"""This object fetches the traffic group related statistics.
	"""

	_SDM_NAME = 'trafficGroup'

	def __init__(self, parent):
		super(TrafficGroup, self).__init__(parent)

	@property
	def Name(self):
		"""Name of the traffic item.

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	def remove(self):
		"""Deletes a child instance of TrafficGroup on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
