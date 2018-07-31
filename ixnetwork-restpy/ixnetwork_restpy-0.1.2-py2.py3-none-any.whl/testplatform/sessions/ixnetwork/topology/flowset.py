from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowSet(Base):
	"""Flow Set Configuration
	"""

	_SDM_NAME = 'flowSet'

	def __init__(self, parent):
		super(FlowSet, self).__init__(parent)

	@property
	def FlowProfile(self):
		"""Returns the one and only one FlowProfile object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.flowprofile.FlowProfile)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.flowprofile import FlowProfile
		return self._read(FlowProfile(self), None)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Cookie(self):
		"""Cookie of the flow entry that was looked up. This is the opaque controller-issued identifier.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cookie')

	@property
	def CookieMask(self):
		"""The mask used to restrict the cookie bits.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cookieMask')

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
	def FlowAdvertise(self):
		"""If selected, the flows are advertised by the OF Channel.

		Returns:
			bool
		"""
		return self._get_attribute('flowAdvertise')
	@FlowAdvertise.setter
	def FlowAdvertise(self, value):
		self._set_attribute('flowAdvertise', value)

	@property
	def FlowFlags(self):
		"""Allows to configure the Flow Flags. Options are: 1) Send Flow Removed 2) Check Overlap 3) Reset Counts 4) No Packet Count 5) No Byte Count

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flowFlags')

	@property
	def FlowMatchType(self):
		"""The type of match to be configured. Options include the following: 1) Strict 2) Loose

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flowMatchType')

	@property
	def FlowSetId(self):
		"""Specify the controller Flow Set identifier.

		Returns:
			str
		"""
		return self._get_attribute('flowSetId')
	@FlowSetId.setter
	def FlowSetId(self, value):
		self._set_attribute('flowSetId', value)

	@property
	def HardTimeout(self):
		"""The inactive time in seconds after which the Flow range will hard timeout and close.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('hardTimeout')

	@property
	def IdleTimeout(self):
		"""The inactive time in seconds after which the Flow range will timeout and become idle.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('idleTimeout')

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
	def NumberOfFlows(self):
		"""The number of flows to be configured for the controller table.

		Returns:
			number
		"""
		return self._get_attribute('numberOfFlows')
	@NumberOfFlows.setter
	def NumberOfFlows(self, value):
		self._set_attribute('numberOfFlows', value)

	@property
	def Priority(self):
		"""The priority level for the Flow Range.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('priority')

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
