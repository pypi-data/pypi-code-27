from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Connector(Base):
	"""Connects scenario elements
	"""

	_SDM_NAME = 'connector'

	def __init__(self, parent):
		super(Connector, self).__init__(parent)

	@property
	def ConnectedTo(self):
		"""Scenario element this connector is connecting to

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/lag?deepchild=*)
		"""
		return self._get_attribute('connectedTo')
	@ConnectedTo.setter
	def ConnectedTo(self, value):
		self._set_attribute('connectedTo', value)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def PropagateMultiplier(self):
		"""The Connector will propagate the multiplicity of destination back to the source and its parent NetworkElementSet

		Returns:
			bool
		"""
		return self._get_attribute('propagateMultiplier')

	def remove(self):
		"""Deletes a child instance of Connector on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
