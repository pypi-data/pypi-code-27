from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PppoxServerSessions(Base):
	"""PPPoX Server Sessions.
	"""

	_SDM_NAME = 'pppoxServerSessions'

	def __init__(self, parent):
		super(PppoxServerSessions, self).__init__(parent)

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
	def ChapName(self):
		"""User name when CHAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('chapName')

	@property
	def ChapSecret(self):
		"""Secret when CHAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('chapSecret')

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
	def DiscoveredClientsMacs(self):
		"""The discovered remote MAC address.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredClientsMacs')

	@property
	def DiscoveredRemoteSessionIds(self):
		"""The negotiated session ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredRemoteSessionIds')

	@property
	def DiscoveredRemoteTunnelIds(self):
		"""The negotiated tunnel ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredRemoteTunnelIds')

	@property
	def DiscoveredSessionIds(self):
		"""The negotiated session ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredSessionIds')

	@property
	def DiscoveredTunnelIPs(self):
		"""The discovered remote tunnel IP.

		Returns:
			list(str)
		"""
		return self._get_attribute('discoveredTunnelIPs')

	@property
	def DiscoveredTunnelIds(self):
		"""The negotiated tunnel ID.

		Returns:
			list(number)
		"""
		return self._get_attribute('discoveredTunnelIds')

	@property
	def DomainList(self):
		"""Configure domain group settings

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('domainList')

	@property
	def EnableDomainGroups(self):
		"""Enable domain groups

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableDomainGroups')

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
	def PapPassword(self):
		"""Password when PAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('papPassword')

	@property
	def PapUser(self):
		"""User name when PAP Authentication is being used

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('papUser')

	@property
	def ServerIpv4Addresses(self):
		"""IPv4 Server Address. Each PPPoX Server Session will display the v4 address from the PPPoX Server it belongs to.

		Returns:
			list(str)
		"""
		return self._get_attribute('serverIpv4Addresses')

	@property
	def ServerIpv6Addresses(self):
		"""IPv6 Server Address. Each PPPoX Server Session will display the v6 address from the PPPoX Server it belongs to.

		Returns:
			list(str)
		"""
		return self._get_attribute('serverIpv6Addresses')

	@property
	def SessionInfo(self):
		"""Logs additional information about the session state

		Returns:
			list(str[cLS_CFG_REJ_AUTH|cLS_CHAP_PEER_DET_FAIL|cLS_CHAP_PEER_RESP_BAD|cLS_CODE_REJ_IPCP|cLS_CODE_REJ_IPV6CP|cLS_CODE_REJ_LCP|cLS_ERR_PPP_NO_BUF|cLS_ERR_PPP_SEND_PKT|cLS_LINK_DISABLE|cLS_LOC_IPADDR_BROADCAST|cLS_LOC_IPADDR_CLASS_E|cLS_LOC_IPADDR_INVAL_ACKS_0|cLS_LOC_IPADDR_INVAL_ACKS_DIFF|cLS_LOC_IPADDR_LOOPBACK|cLS_LOC_IPADDR_PEER_MATCH_LOC|cLS_LOC_IPADDR_PEER_NO_GIVE|cLS_LOC_IPADDR_PEER_NO_HELP|cLS_LOC_IPADDR_PEER_NO_TAKE|cLS_LOC_IPADDR_PEER_REJ|cLS_LOOPBACK_DETECT|cLS_NO_NCP|cLS_NONE|cLS_PAP_BAD_PASSWD|cLS_PEER_DISCONNECTED|cLS_PEER_IPADDR_MATCH_LOC|cLS_PEER_IPADDR_PEER_NO_SET|cLS_PPOE_AC_SYSTEM_ERROR|cLS_PPOE_GENERIC_ERROR|cLS_PPP_DISABLE|cLS_PPPOE_PADI_TIMEOUT|cLS_PPPOE_PADO_TIMEOUT|cLS_PPPOE_PADR_TIMEOUT|cLS_PROTO_REJ_IPCP|cLS_PROTO_REJ_IPv6CP|cLS_TIMEOUT_CHAP_CHAL|cLS_TIMEOUT_CHAP_RESP|cLS_TIMEOUT_IPCP_CFG_REQ|cLS_TIMEOUT_IPV6CP_CFG_REQ|cLS_TIMEOUT_IPV6CP_RA|cLS_TIMEOUT_LCP_CFG_REQ|cLS_TIMEOUT_LCP_ECHO_REQ|cLS_TIMEOUT_PAP_AUTH_REQ])
		"""
		return self._get_attribute('sessionInfo')

	def CloseIpcp(self, Arg1):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX Server Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxServerSessions object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('closeIpcp', payload=locals(), response_object=None)

	def CloseIpcp(self, Arg1, SessionIndices):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX Server Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxServerSessions object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('closeIpcp', payload=locals(), response_object=None)

	def CloseIpcp(self, Arg1, SessionIndices):
		"""Executes the closeIpcp operation on the server.

		Close IPCP for selected PPPoX Server Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxServerSessions object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('closeIpcp', payload=locals(), response_object=None)

	def CloseIpv6cp(self, Arg1):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX Severs Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxServerSessions object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('closeIpv6cp', payload=locals(), response_object=None)

	def CloseIpv6cp(self, Arg1, SessionIndices):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX Severs Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxServerSessions object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('closeIpv6cp', payload=locals(), response_object=None)

	def CloseIpv6cp(self, Arg1, SessionIndices):
		"""Executes the closeIpv6cp operation on the server.

		Close IPv6CP for selected PPPoX Severs Sessions items.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pppoxServerSessions object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('closeIpv6cp', payload=locals(), response_object=None)

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
