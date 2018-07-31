from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class VpnParameter(Base):
	"""VPN
	"""

	_SDM_NAME = 'vpnParameter'

	def __init__(self, parent):
		super(VpnParameter, self).__init__(parent)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def SiteId(self):
		"""VPN Site Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('siteId')

	@property
	def UseVpnParameters(self):
		"""Flag to determine whether optional VPN parameters are provided.

		Returns:
			bool
		"""
		return self._get_attribute('useVpnParameters')
	@UseVpnParameters.setter
	def UseVpnParameters(self, value):
		self._set_attribute('useVpnParameters', value)

	def remove(self):
		"""Deletes a child instance of VpnParameter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
