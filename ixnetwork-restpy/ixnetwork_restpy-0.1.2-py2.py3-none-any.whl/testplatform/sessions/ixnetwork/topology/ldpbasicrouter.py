from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LdpBasicRouter(Base):
	"""Ldp V4 Device level Configuration
	"""

	_SDM_NAME = 'ldpBasicRouter'

	def __init__(self, parent):
		super(LdpBasicRouter, self).__init__(parent)

	def Connector(self):
		"""Gets child instances of Connector from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Connector will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector.Connector))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector import Connector
		return self._select(Connector(self), locals())

	def add_Connector(self, ConnectedTo=None):
		"""Adds a child instance of Connector on the server.

		Args:
			ConnectedTo (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): Scenario element this connector is connecting to

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector.Connector)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.connector import Connector
		return self._create(Connector(self), locals())

	@property
	def LdpLeafRangeV4(self):
		"""Returns the one and only one LdpLeafRangeV4 object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpleafrangev4.LdpLeafRangeV4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpleafrangev4 import LdpLeafRangeV4
		return self._read(LdpLeafRangeV4(self), None)

	@property
	def LdpRootRangeV4(self):
		"""Returns the one and only one LdpRootRangeV4 object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldprootrangev4.LdpRootRangeV4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldprootrangev4 import LdpRootRangeV4
		return self._read(LdpRootRangeV4(self), None)

	def Ldpotherpws(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Ldpotherpws from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ldpotherpws will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpotherpws.Ldpotherpws))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpotherpws import Ldpotherpws
		return self._select(Ldpotherpws(self), locals())

	def add_Ldpotherpws(self, AutoPeerId="False", ConnectedVia=None, Multiplier="1", Name=None, StackedLayers=None):
		"""Adds a child instance of Ldpotherpws on the server.

		Args:
			AutoPeerId (bool): If selected, LDP Peer IP would be taken from LDP router's peer configuration.
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpotherpws.Ldpotherpws)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpotherpws import Ldpotherpws
		return self._create(Ldpotherpws(self), locals())

	def Ldppwvpls(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Ldppwvpls from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ldppwvpls will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldppwvpls.Ldppwvpls))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldppwvpls import Ldppwvpls
		return self._select(Ldppwvpls(self), locals())

	def add_Ldppwvpls(self, AutoPeerId="False", ConnectedVia=None, Multiplier="1", Name=None, StackedLayers=None):
		"""Adds a child instance of Ldppwvpls on the server.

		Args:
			AutoPeerId (bool): If selected, LDP Peer IP would be taken from LDP router's peer configuration.
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldppwvpls.Ldppwvpls)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldppwvpls import Ldppwvpls
		return self._create(Ldppwvpls(self), locals())

	def Ldpvplsbgpad(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Ldpvplsbgpad from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ldpvplsbgpad will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpvplsbgpad.Ldpvplsbgpad))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpvplsbgpad import Ldpvplsbgpad
		return self._select(Ldpvplsbgpad(self), locals())

	def add_Ldpvplsbgpad(self, AutoPeerId="False", ConnectedVia=None, Multiplier="1", Name=None, StackedLayers=None):
		"""Adds a child instance of Ldpvplsbgpad on the server.

		Args:
			AutoPeerId (bool): If selected, LDP Peer IP would be taken from LDP router's peer configuration.
			ConnectedVia (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of layers this layer used to connect to the wire
			Multiplier (number): Number of layer instances per parent instance (multiplier)
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			StackedLayers (list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])): List of secondary (many to one) child layer protocols

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpvplsbgpad.Ldpvplsbgpad)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpvplsbgpad import Ldpvplsbgpad
		return self._create(Ldpvplsbgpad(self), locals())

	def LearnedInfo(self, State=None, Type=None):
		"""Gets child instances of LearnedInfo from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of LearnedInfo will be returned.

		Args:
			State (str): The state of the learned information query
			Type (str): The type of learned information

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo.LearnedInfo))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.learnedinfo import LearnedInfo
		return self._select(LearnedInfo(self), locals())

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def ConnectedVia(self):
		"""List of layers this layer used to connect to the wire

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('connectedVia')
	@ConnectedVia.setter
	def ConnectedVia(self, value):
		self._set_attribute('connectedVia', value)

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
	def EnableBfdMplsLearnedLsp(self):
		"""If selected, BFD MPLS is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableBfdMplsLearnedLsp')

	@property
	def EnableFec128Advertisement(self):
		"""If selected, FEC128 P2P-PW app type is enabled in SAC TLV.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableFec128Advertisement')

	@property
	def EnableFec129Advertisement(self):
		"""If selected, FEC129 P2P-PW app type is enabled in SAC TLV.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableFec129Advertisement')

	@property
	def EnableGracefulRestart(self):
		"""If selected, LDP Graceful Restart is enabled on this Ixia-emulated LDP Router.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableGracefulRestart')

	@property
	def EnableIpv4Advertisement(self):
		"""If selected, IPv4-Prefix LSP app type is enabled in SAC TLV.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableIpv4Advertisement')

	@property
	def EnableIpv6Advertisement(self):
		"""If selected, IPv6-Prefix LSP app type is enabled in SAC TLV.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableIpv6Advertisement')

	@property
	def EnableLspPingLearnedLsp(self):
		"""If selected, LSP Ping is enabled for learned LSPs.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLspPingLearnedLsp')

	@property
	def EnableP2MPCapability(self):
		"""If selected, LDP Router is P2MP capable.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableP2MPCapability')

	@property
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def IgnoreStateAdvertisementControlCapability(self):
		"""If selected, LDP Router ignores SAC TLV it receives.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ignoreStateAdvertisementControlCapability')

	@property
	def IncludeSac(self):
		"""Select to include 'State Advertisement Control Capability' TLV in Initialization message and Capability message

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSac')

	@property
	def KeepAliveHoldTime(self):
		"""The period of time, in seconds, between KEEP-ALIVE messages sent to the DUT.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('keepAliveHoldTime')

	@property
	def KeepAliveInterval(self):
		"""The frequency, in seconds, at which IxNetwork sends KEEP-ALIVE requests.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('keepAliveInterval')

	@property
	def LdpVersion(self):
		"""Version of LDP. When RFC 5036 is chosen, LDP version is version 1. When draft-pdutta-mpls-ldp-adj-capability-00 is chosen, LDP version is version 2

		Returns:
			str(version1|version2)
		"""
		return self._get_attribute('ldpVersion')
	@LdpVersion.setter
	def LdpVersion(self, value):
		self._set_attribute('ldpVersion', value)

	@property
	def LeafRangesCountV4(self):
		"""The number of Leaf Ranges configured for this LDP router

		Returns:
			number
		"""
		return self._get_attribute('leafRangesCountV4')
	@LeafRangesCountV4.setter
	def LeafRangesCountV4(self, value):
		self._set_attribute('leafRangesCountV4', value)

	@property
	def LocalRouterID(self):
		"""Router ID

		Returns:
			list(str)
		"""
		return self._get_attribute('localRouterID')

	@property
	def Multiplier(self):
		"""Number of layer instances per parent instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

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
	def ReconnectTime(self):
		"""Reconnect Time ms

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('reconnectTime')

	@property
	def RecoveryTime(self):
		"""The restarting LSR advertises the amount of time that it will retain its MPLS forwarding state.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('recoveryTime')

	@property
	def RootRangesCountV4(self):
		"""The number of Root Ranges configured for this LDP router

		Returns:
			number
		"""
		return self._get_attribute('rootRangesCountV4')
	@RootRangesCountV4.setter
	def RootRangesCountV4(self, value):
		self._set_attribute('rootRangesCountV4', value)

	@property
	def SessionInfo(self):
		"""Logs additional information about the LDP session state

		Returns:
			list(str[lDP_STATE_INITIALIZED|lDP_STATE_MULTIPLE_PEERS|lDP_STATE_NON_EXISTENT|lDP_STATE_OPENREC|lDP_STATE_OPENSENT|lDP_STATE_OPERATIONAL|none])
		"""
		return self._get_attribute('sessionInfo')

	@property
	def SessionPreference(self):
		"""The transport connection preference of the LDP router that is conveyed in Dual-stack capability TLV included in LDP Hello message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sessionPreference')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def StackedLayers(self):
		"""List of secondary (many to one) child layer protocols

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('stackedLayers')
	@StackedLayers.setter
	def StackedLayers(self, value):
		self._set_attribute('stackedLayers', value)

	@property
	def StateCounts(self):
		"""A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up

		Returns:
			dict(total:number,notStarted:number,down:number,up:number)
		"""
		return self._get_attribute('stateCounts')

	@property
	def Status(self):
		"""Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	def remove(self):
		"""Deletes a child instance of LdpBasicRouter on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def ClearAllLearnedInfo(self, Arg1):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the clearAllLearnedInfo operation on the server.

		Clear All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('clearAllLearnedInfo', payload=locals(), response_object=None)

	def ClearAllLearnedInfoInClient(self, Arg2):
		"""Executes the clearAllLearnedInfoInClient operation on the server.

		Clears ALL routes from GUI grid for the selected LDP Router.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('clearAllLearnedInfoInClient', payload=locals(), response_object=None)

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

	def GetAllLearnedInfo(self, Arg1):
		"""Executes the getAllLearnedInfo operation on the server.

		Get All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getAllLearnedInfo', payload=locals(), response_object=None)

	def GetAllLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getAllLearnedInfo operation on the server.

		Get All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getAllLearnedInfo', payload=locals(), response_object=None)

	def GetAllLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getAllLearnedInfo operation on the server.

		Get All Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getAllLearnedInfo', payload=locals(), response_object=None)

	def GetAllLearnedInfo(self, Arg2):
		"""Executes the getAllLearnedInfo operation on the server.

		Gets ALL routes learnt and stored by this LDP Router.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getAllLearnedInfo', payload=locals(), response_object=None)

	def GetFEC128LearnedInfo(self, Arg1):
		"""Executes the getFEC128LearnedInfo operation on the server.

		Get FEC 128 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getFEC128LearnedInfo', payload=locals(), response_object=None)

	def GetFEC128LearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getFEC128LearnedInfo operation on the server.

		Get FEC 128 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getFEC128LearnedInfo', payload=locals(), response_object=None)

	def GetFEC128LearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getFEC128LearnedInfo operation on the server.

		Get FEC 128 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getFEC128LearnedInfo', payload=locals(), response_object=None)

	def GetFEC128LearnedInfo(self, Arg2):
		"""Executes the getFEC128LearnedInfo operation on the server.

		Gets FEC128 Learned Information learnt by this LDP router.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getFEC128LearnedInfo', payload=locals(), response_object=None)

	def GetFEC129LearnedInfo(self, Arg1):
		"""Executes the getFEC129LearnedInfo operation on the server.

		Get FEC 129 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getFEC129LearnedInfo', payload=locals(), response_object=None)

	def GetFEC129LearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getFEC129LearnedInfo operation on the server.

		Get FEC 129 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getFEC129LearnedInfo', payload=locals(), response_object=None)

	def GetFEC129LearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getFEC129LearnedInfo operation on the server.

		Get FEC 129 Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getFEC129LearnedInfo', payload=locals(), response_object=None)

	def GetFEC129LearnedInfo(self, Arg2):
		"""Executes the getFEC129LearnedInfo operation on the server.

		Gets FEC129 Learned Information learnt by this LDP router.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getFEC129LearnedInfo', payload=locals(), response_object=None)

	def GetIPv4FECLearnedInfo(self, Arg1):
		"""Executes the getIPv4FECLearnedInfo operation on the server.

		Get IPv4 FEC Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getIPv4FECLearnedInfo', payload=locals(), response_object=None)

	def GetIPv4FECLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getIPv4FECLearnedInfo operation on the server.

		Get IPv4 FEC Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getIPv4FECLearnedInfo', payload=locals(), response_object=None)

	def GetIPv4FECLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getIPv4FECLearnedInfo operation on the server.

		Get IPv4 FEC Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getIPv4FECLearnedInfo', payload=locals(), response_object=None)

	def GetIPv4FECLearnedInfo(self, Arg2):
		"""Executes the getIPv4FECLearnedInfo operation on the server.

		Gets Learned Information learnt by this LDP router.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getIPv4FECLearnedInfo', payload=locals(), response_object=None)

	def GetIPv6FECLearnedInfo(self, Arg1):
		"""Executes the getIPv6FECLearnedInfo operation on the server.

		Get IPv6 FEC Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getIPv6FECLearnedInfo', payload=locals(), response_object=None)

	def GetIPv6FECLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getIPv6FECLearnedInfo operation on the server.

		Get IPv6 FEC Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getIPv6FECLearnedInfo', payload=locals(), response_object=None)

	def GetIPv6FECLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getIPv6FECLearnedInfo operation on the server.

		Get IPv6 FEC Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getIPv6FECLearnedInfo', payload=locals(), response_object=None)

	def GetIPv6FECLearnedInfo(self, Arg2):
		"""Executes the getIPv6FECLearnedInfo operation on the server.

		Gets Learned Information learnt by this LDP router.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getIPv6FECLearnedInfo', payload=locals(), response_object=None)

	def GetP2MPFECLearnedInfo(self, Arg1):
		"""Executes the getP2MPFECLearnedInfo operation on the server.

		Get P2MP FEC Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getP2MPFECLearnedInfo', payload=locals(), response_object=None)

	def GetP2MPFECLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getP2MPFECLearnedInfo operation on the server.

		Get P2MP FEC Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getP2MPFECLearnedInfo', payload=locals(), response_object=None)

	def GetP2MPFECLearnedInfo(self, Arg1, SessionIndices):
		"""Executes the getP2MPFECLearnedInfo operation on the server.

		Get P2MP FEC Learned Info

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('getP2MPFECLearnedInfo', payload=locals(), response_object=None)

	def GetP2MPFECLearnedInfo(self, Arg2):
		"""Executes the getP2MPFECLearnedInfo operation on the server.

		Gets P2MP FEC Learned Information learnt by this LDP router.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getP2MPFECLearnedInfo', payload=locals(), response_object=None)

	def GracefullyRestart(self, Arg1, Delay):
		"""Executes the gracefullyRestart operation on the server.

		Gracefully Restart

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			Delay (number): This parameter requires a delay of type kInteger

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('gracefullyRestart', payload=locals(), response_object=None)

	def GracefullyRestart(self, Arg1, Delay, SessionIndices):
		"""Executes the gracefullyRestart operation on the server.

		Gracefully Restart

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			Delay (number): This parameter requires a delay of type kInteger
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('gracefullyRestart', payload=locals(), response_object=None)

	def GracefullyRestart(self, Arg1, SessionIndices, Delay):
		"""Executes the gracefullyRestart operation on the server.

		Gracefully Restart

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a delay of type kInteger
			Delay (number): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('gracefullyRestart', payload=locals(), response_object=None)

	def GracefullyRestart(self, Arg2, Arg3):
		"""Executes the gracefullyRestart operation on the server.

		Gracefully restart selected Routers

		Args:
			Arg2 (list(number)): Action indices for gracefully restart
			Arg3 (number): Restart After Time (in secs)

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('gracefullyRestart', payload=locals(), response_object=None)

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def ResumeKeepAlive(self, Arg1):
		"""Executes the resumeKeepAlive operation on the server.

		Resume sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('resumeKeepAlive', payload=locals(), response_object=None)

	def ResumeKeepAlive(self, Arg1, SessionIndices):
		"""Executes the resumeKeepAlive operation on the server.

		Resume sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('resumeKeepAlive', payload=locals(), response_object=None)

	def ResumeKeepAlive(self, Arg1, SessionIndices):
		"""Executes the resumeKeepAlive operation on the server.

		Resume sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('resumeKeepAlive', payload=locals(), response_object=None)

	def Resumekeepalive(self, Arg2):
		"""Executes the resumekeepalive operation on the server.

		Start Sending Keep Alive Messages.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('resumekeepalive', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start LDP Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start LDP Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start LDP Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Stop LDP Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop LDP Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop LDP Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def StopKeepAlive(self, Arg1):
		"""Executes the stopKeepAlive operation on the server.

		Stop sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopKeepAlive', payload=locals(), response_object=None)

	def StopKeepAlive(self, Arg1, SessionIndices):
		"""Executes the stopKeepAlive operation on the server.

		Stop sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopKeepAlive', payload=locals(), response_object=None)

	def StopKeepAlive(self, Arg1, SessionIndices):
		"""Executes the stopKeepAlive operation on the server.

		Stop sending KeepAlive

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ldpBasicRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopKeepAlive', payload=locals(), response_object=None)

	def Stopkeepalive(self, Arg2):
		"""Executes the stopkeepalive operation on the server.

		Stop Sending Keep Alive Messages.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stopkeepalive', payload=locals(), response_object=None)
