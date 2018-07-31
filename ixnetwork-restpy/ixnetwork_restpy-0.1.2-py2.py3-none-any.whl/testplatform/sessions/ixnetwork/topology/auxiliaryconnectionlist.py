from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AuxiliaryConnectionList(Base):
	"""Openflow Switch Auxiliary Connections level Configuration
	"""

	_SDM_NAME = 'auxiliaryConnectionList'

	def __init__(self, parent):
		super(AuxiliaryConnectionList, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AuxId(self):
		"""Specify the Auxiliary Id, {0 - 255}

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('auxId')

	@property
	def ChannelName(self):
		"""Parent Channel Name

		Returns:
			str
		"""
		return self._get_attribute('channelName')

	@property
	def ConnectionType(self):
		"""The type of connection used for the Interface. Options include: 1) TCP 2) TLS 3) UDP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('connectionType')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def UDPSrcPortNum(self):
		"""UDP Source Port Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('uDPSrcPortNum')

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
