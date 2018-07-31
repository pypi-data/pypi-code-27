from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OpenFlowChannel(Base):
	"""OpenFlow Controller global and per-port settings
	"""

	_SDM_NAME = 'openFlowChannel'

	def __init__(self, parent):
		super(OpenFlowChannel, self).__init__(parent)

	@property
	def FlowAggrMatchTemplate(self):
		"""Returns the one and only one FlowAggrMatchTemplate object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.flowaggrmatchtemplate.FlowAggrMatchTemplate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.flowaggrmatchtemplate import FlowAggrMatchTemplate
		return self._read(FlowAggrMatchTemplate(self), None)

	@property
	def FlowStatMatchTemplate(self):
		"""Returns the one and only one FlowStatMatchTemplate object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.flowstatmatchtemplate.FlowStatMatchTemplate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.flowstatmatchtemplate import FlowStatMatchTemplate
		return self._read(FlowStatMatchTemplate(self), None)

	@property
	def PacketOutActionTemplate(self):
		"""Returns the one and only one PacketOutActionTemplate object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.packetoutactiontemplate.PacketOutActionTemplate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.packetoutactiontemplate import PacketOutActionTemplate
		return self._read(PacketOutActionTemplate(self), None)

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
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

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
