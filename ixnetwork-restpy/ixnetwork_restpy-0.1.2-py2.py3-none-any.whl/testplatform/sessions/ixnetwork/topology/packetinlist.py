from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PacketInList(Base):
	"""Openflow Switch PacketIn Configuration
	"""

	_SDM_NAME = 'packetInList'

	def __init__(self, parent):
		super(PacketInList, self).__init__(parent)

	@property
	def AuxiliaryId(self):
		"""The identifier for auxiliary connections.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('auxiliaryId')

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
	def FlowTable(self):
		"""If selected, the Switch looks up for each PacketIn configured in the Flow Table.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flowTable')

	@property
	def InPort(self):
		"""The Switch Port on which, this Packet has come.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('inPort')

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
	def PacketInName(self):
		"""The description of the packet-in.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('packetInName')

	@property
	def PhysicalInPort(self):
		"""The physical In port value for this PacketIn range. It is the underlying physical port when packet is received on a logical port.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('physicalInPort')

	@property
	def SendPacketIn(self):
		"""If selected, the Switch starts sending PacketIn messages when the session comes up.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendPacketIn')

	@property
	def SwitchName(self):
		"""Parent Switch Name

		Returns:
			str
		"""
		return self._get_attribute('switchName')

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

	def SendPause(self, Arg2):
		"""Executes the sendPause operation on the server.

		Pause Sending PacketIn

		Args:
			Arg2 (list(number)): List of PacketIn.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPause', payload=locals(), response_object=None)

	def SendStart(self, Arg2):
		"""Executes the sendStart operation on the server.

		Start Sending PacketIn

		Args:
			Arg2 (list(number)): List of PacketIn.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendStart', payload=locals(), response_object=None)

	def SendStop(self, Arg2):
		"""Executes the sendStop operation on the server.

		Stop Sending PacketIn

		Args:
			Arg2 (list(number)): List of PacketIn.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendStop', payload=locals(), response_object=None)
