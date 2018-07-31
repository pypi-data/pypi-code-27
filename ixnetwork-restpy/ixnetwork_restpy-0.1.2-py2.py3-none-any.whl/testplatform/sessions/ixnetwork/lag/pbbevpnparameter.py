from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PbbEVpnParameter(Base):
	"""PBB-EVPN
	"""

	_SDM_NAME = 'pbbEVpnParameter'

	def __init__(self, parent):
		super(PbbEVpnParameter, self).__init__(parent)

	@property
	def BMac(self):
		"""Broadcast MAC addresses of the devices

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bMac')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def UsePbbEVpnParameters(self):
		"""Flag to determine whether optional PBB EVPN parameters are provided.

		Returns:
			bool
		"""
		return self._get_attribute('usePbbEVpnParameters')
	@UsePbbEVpnParameters.setter
	def UsePbbEVpnParameters(self, value):
		self._set_attribute('usePbbEVpnParameters', value)

	def remove(self):
		"""Deletes a child instance of PbbEVpnParameter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
