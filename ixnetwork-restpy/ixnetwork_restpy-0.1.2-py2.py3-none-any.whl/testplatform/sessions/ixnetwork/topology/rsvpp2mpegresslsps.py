from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RsvpP2mpEgressLsps(Base):
	"""RSVP-TE P2MP Tail (Egress) Tunnels
	"""

	_SDM_NAME = 'rsvpP2mpEgressLsps'

	def __init__(self, parent):
		super(RsvpP2mpEgressLsps, self).__init__(parent)

	def RsvpRroSubObjectsList(self, DescriptiveName=None, Name=None):
		"""Gets child instances of RsvpRroSubObjectsList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of RsvpRroSubObjectsList will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvprrosubobjectslist.RsvpRroSubObjectsList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.rsvprrosubobjectslist import RsvpRroSubObjectsList
		return self._select(RsvpRroSubObjectsList(self), locals())

	def Tag(self, Name=None):
		"""Gets child instances of Tag from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Tag will be returned.

		Args:
			Name (str): specifies the name of the tag the entity will be part of

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return self._select(Tag(self), locals())

	def add_Tag(self, Enabled="False", Name=None):
		"""Adds a child instance of Tag on the server.

		Args:
			Enabled (bool): Enables/disables tags
			Name (str): specifies the name of the tag the entity will be part of

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return self._create(Tag(self), locals())

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def DestinationIpv4GroupAddress(self):
		"""Destination IPv4 Group Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destinationIpv4GroupAddress')

	@property
	def EnableFixedLabelForReservations(self):
		"""Enable Fixed Label For Reservations

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableFixedLabelForReservations')

	@property
	def EndPointIpv6(self):
		"""Destination IPv6 Group Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('endPointIpv6')

	@property
	def IncludeConnectedIpOnTop(self):
		"""Include connected IP on top

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeConnectedIpOnTop')

	@property
	def IncludeLeafIpAtBottom(self):
		"""Include Leaf IP at bottom

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeLeafIpAtBottom')

	@property
	def LabelValue(self):
		"""Label Value

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('labelValue')

	@property
	def LocalIp(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('localIp')

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
	def NumberOfRroSubObjects(self):
		"""Number Of RRO Sub-Objects

		Returns:
			number
		"""
		return self._get_attribute('numberOfRroSubObjects')
	@NumberOfRroSubObjects.setter
	def NumberOfRroSubObjects(self, value):
		self._set_attribute('numberOfRroSubObjects', value)

	@property
	def P2mpIdAsNumber(self):
		"""P2MP ID displayed in Integer format

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('p2mpIdAsNumber')

	@property
	def P2mpIdIp(self):
		"""P2MP ID displayed in IP Address format

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('p2mpIdIp')

	@property
	def ReflectRro(self):
		"""Reflect RRO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reflectRro')

	@property
	def RefreshInterval(self):
		"""Refresh Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('refreshInterval')

	@property
	def ReservationStyle(self):
		"""Reservation Style

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reservationStyle')

	@property
	def SendAsRro(self):
		"""Send As RRO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendAsRro')

	@property
	def SendAsSrro(self):
		"""Send As SRRO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendAsSrro')

	@property
	def SendReservationConfirmation(self):
		"""Send Reservation Confirmation

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sendReservationConfirmation')

	@property
	def State(self):
		"""State

		Returns:
			list(str[down|none|notStarted|up])
		"""
		return self._get_attribute('state')

	@property
	def SubLspsDown(self):
		"""Sub LSPs Down

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('subLspsDown')

	@property
	def TimeoutMultiplier(self):
		"""Timeout Multiplier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('timeoutMultiplier')

	@property
	def TypeP2mpId(self):
		"""P2MP ID Type

		Returns:
			str(iP|p2MPId)
		"""
		return self._get_attribute('typeP2mpId')
	@TypeP2mpId.setter
	def TypeP2mpId(self, value):
		self._set_attribute('typeP2mpId', value)

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

	def GraftSubLsp(self, Arg1):
		"""Executes the graftSubLsp operation on the server.

		Activate/Enable Tunnel selected SubLsp Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('graftSubLsp', payload=locals(), response_object=None)

	def GraftSubLsp(self, Arg1, SessionIndices):
		"""Executes the graftSubLsp operation on the server.

		Activate/Enable Tunnel selected SubLsp Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('graftSubLsp', payload=locals(), response_object=None)

	def GraftSubLsp(self, Arg1, SessionIndices):
		"""Executes the graftSubLsp operation on the server.

		Activate/Enable Tunnel selected SubLsp Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('graftSubLsp', payload=locals(), response_object=None)

	def GraftSubLsp(self, Arg2):
		"""Executes the graftSubLsp operation on the server.

		Activate/Enable Tunnel selected SubLsp Ranges

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('graftSubLsp', payload=locals(), response_object=None)

	def PruneSubLsp(self, Arg1):
		"""Executes the pruneSubLsp operation on the server.

		Deactivate/Disable selected Tunnel SubLsp Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('pruneSubLsp', payload=locals(), response_object=None)

	def PruneSubLsp(self, Arg1, SessionIndices):
		"""Executes the pruneSubLsp operation on the server.

		Deactivate/Disable selected Tunnel SubLsp Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('pruneSubLsp', payload=locals(), response_object=None)

	def PruneSubLsp(self, Arg1, SessionIndices):
		"""Executes the pruneSubLsp operation on the server.

		Deactivate/Disable selected Tunnel SubLsp Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('pruneSubLsp', payload=locals(), response_object=None)

	def PruneSubLsp(self, Arg2):
		"""Executes the pruneSubLsp operation on the server.

		Deactivate/Disable selected Tunnel SubLsp Ranges

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('pruneSubLsp', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Activate/Enable selected Tunnel Tail Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Activate/Enable selected Tunnel Tail Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Activate/Enable selected Tunnel Tail Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg2):
		"""Executes the start operation on the server.

		Start

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Deactivate/Disable selected Tunnel Tail Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Deactivate/Disable selected Tunnel Tail Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Deactivate/Disable selected Tunnel Tail Ranges

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./rsvpP2mpEgressLsps object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg2):
		"""Executes the stop operation on the server.

		Stop

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stop', payload=locals(), response_object=None)
