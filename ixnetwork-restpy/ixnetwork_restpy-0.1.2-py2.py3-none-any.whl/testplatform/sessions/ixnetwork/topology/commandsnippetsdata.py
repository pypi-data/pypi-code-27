from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CommandSnippetsData(Base):
	"""Command Snippets Data allows user to fire Yang commands to DUT
	"""

	_SDM_NAME = 'commandSnippetsData'

	def __init__(self, parent):
		super(CommandSnippetsData, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def CommandSnippetDirectory(self):
		"""Directory containing XML based Netconf compliant command snippets.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('commandSnippetDirectory')

	@property
	def CommandSnippetFile(self):
		"""File containing XML based Netconf compliant command snippet. For multiple command snippets with assymetric file names( which cannot be expressed easily as a pattern) please explore File option in Master Row Pattern Editor by putting the file namesin a .csv and pulling those values into the column cells.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('commandSnippetFile')

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
	def PeriodicTransmissionInterval(self):
		"""Minimum interval between scheduling of two transmits of the Command Snippet.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('periodicTransmissionInterval')

	@property
	def TransmissionBehaviour(self):
		"""Transmission behaviour for command snippet.Don't Send : This means that command will not be automatically executed. This choice should beused if user wants to control the order or/and timing of sending the command snippet to the DUTusing Test Composer or Automation Script.Once: The command will be sent only once to the DUT every time session comes up with the DUT.Periodic - Continuous: The command will be sent every Transmission Interval for the full lifetime of the session.Capture should be enabled with care if this option is selected.Periodic - Fixed Count: The command will be sent Transmission Count number of times, every Periodic Transmission Interval.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('transmissionBehaviour')

	@property
	def TransmissionCount(self):
		"""Number of times to transmit the Command Snippet.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('transmissionCount')

	def ExecuteCommand(self, Arg1):
		"""Executes the executeCommand operation on the server.

		Send the selected command snippet if the Netconf session is established with the Netconf Server

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./commandSnippetsData object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('executeCommand', payload=locals(), response_object=None)

	def ExecuteCommand(self, Arg1, SessionIndices):
		"""Executes the executeCommand operation on the server.

		Send the selected command snippet if the Netconf session is established with the Netconf Server

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./commandSnippetsData object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('executeCommand', payload=locals(), response_object=None)

	def ExecuteCommand(self, Arg1, SessionIndices):
		"""Executes the executeCommand operation on the server.

		Send the selected command snippet if the Netconf session is established with the Netconf Server

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./commandSnippetsData object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('executeCommand', payload=locals(), response_object=None)

	def ExecuteCommand(self, Arg2):
		"""Executes the executeCommand operation on the server.

		Send the configured command for the selected rows to the DUT if the selected client's Netconf session is up with the DUT.

		Args:
			Arg2 (list(number)): List of indices into the device group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('executeCommand', payload=locals(), response_object=None)

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
