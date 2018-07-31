from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CurrentPacket(Base):
	"""This object specifies current packet properties.
	"""

	_SDM_NAME = 'currentPacket'

	def __init__(self, parent):
		super(CurrentPacket, self).__init__(parent)

	def Stack(self, DisplayName=None):
		"""Gets child instances of Stack from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Stack will be returned.

		Args:
			DisplayName (str): Refers to the name of the stack.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.currentpacket.stack.stack.Stack))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.capture.currentpacket.stack.stack import Stack
		return self._select(Stack(self), locals())

	@property
	def PacketHex(self):
		"""Gets the packet hex of the current packet

		Returns:
			str
		"""
		return self._get_attribute('packetHex')

	def GetPacketFromControlCapture(self, Arg2):
		"""Executes the getPacketFromControlCapture operation on the server.

		The command retrieves a packet from the control capture started on a port.

		Args:
			Arg2 (number): The packet index.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getPacketFromControlCapture', payload=locals(), response_object=None)

	def GetPacketFromDataCapture(self, Arg2):
		"""Executes the getPacketFromDataCapture operation on the server.

		The command retrieves a packet from the data capture started on a port.

		Args:
			Arg2 (number): The packet index.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getPacketFromDataCapture', payload=locals(), response_object=None)
