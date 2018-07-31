from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PceUpdateRsvpEroSubObjectList(Base):
	"""
	"""

	_SDM_NAME = 'pceUpdateRsvpEroSubObjectList'

	def __init__(self, parent):
		super(PceUpdateRsvpEroSubObjectList, self).__init__(parent)

	@property
	def ActiveThisEro(self):
		"""Controls whether the ERO sub-object will be sent in the PCInitiate message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('activeThisEro')

	@property
	def AsNumber(self):
		"""AS Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asNumber')

	@property
	def Ipv4Prefix(self):
		"""IPv4 Prefix is specified as an IPv4 address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4Prefix')

	@property
	def Ipv6Prefix(self):
		"""IPv6 Prefix is specified as an IPv6 address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6Prefix')

	@property
	def LooseHop(self):
		"""Indicates if user wants to represent a loose-hop sub object in the LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('looseHop')

	@property
	def PrefixLength(self):
		"""Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	@property
	def SubObjectType(self):
		"""Using the Sub Object Type control user can configure which sub object needs to be included from the following options: Not Applicable IPv4 Prefix IPv6 Prefix AS Number.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('subObjectType')

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('fetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)
