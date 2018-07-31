from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OfHostData(Base):
	"""Contains number of host ports per switch and number of hosts per host port
	"""

	_SDM_NAME = 'ofHostData'

	def __init__(self, parent):
		super(OfHostData, self).__init__(parent)

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
	def NumberOfHostPorts(self):
		"""number of Host Ports per OF Switch.

		Returns:
			number
		"""
		return self._get_attribute('numberOfHostPorts')
	@NumberOfHostPorts.setter
	def NumberOfHostPorts(self, value):
		self._set_attribute('numberOfHostPorts', value)

	@property
	def NumberOfHostsPerPort(self):
		"""Number of Host Groups for each Host Port. Configure Number of Hosts Per Host Group using the Count field in Encapsulations Tab

		Returns:
			number
		"""
		return self._get_attribute('numberOfHostsPerPort')
	@NumberOfHostsPerPort.setter
	def NumberOfHostsPerPort(self, value):
		self._set_attribute('numberOfHostsPerPort', value)

	@property
	def ParentSwitchPortName(self):
		"""Description of the parent Switch Port.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('parentSwitchPortName')

	def remove(self):
		"""Deletes a child instance of OfHostData on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

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

	def SendPacketWithTraverseLI(self, Arg2, Arg3, Arg4, Arg5, Arg6, Arg7, Arg8, Arg9):
		"""Executes the sendPacketWithTraverseLI operation on the server.

		Send an Host Packet (ARP/PING/CUSTOM) from the given device instance to the given destination instance.

		Args:
			Arg2 (list(number)): List of indices into the device group for the corresponding device instances whose IP addresses are used as the source of the request messages.
			Arg3 (number): Destination Host index.
			Arg4 (str(aRP|custom|pING)): Packet Type.
			Arg5 (number): Encapsulation index.
			Arg6 (number): Response Timeout.
			Arg7 (bool): Periodic.
			Arg8 (number): Periodic Interval.
			Arg9 (number): Number of Iteration.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('sendPacketWithTraverseLI', payload=locals(), response_object=None)
