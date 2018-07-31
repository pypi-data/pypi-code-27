from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Topology(Base):
	"""Topology port level configuration
	"""

	_SDM_NAME = 'topology'

	def __init__(self, parent):
		super(Topology, self).__init__(parent)

	@property
	def Ancp(self):
		"""Returns the one and only one Ancp object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ancp.ancp.Ancp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ancp.ancp import Ancp
		return self._read(Ancp(self), None)

	@property
	def BfdRouter(self):
		"""Returns the one and only one BfdRouter object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bfdrouter.bfdrouter.BfdRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bfdrouter.bfdrouter import BfdRouter
		return self._read(BfdRouter(self), None)

	@property
	def BgpIpv4Peer(self):
		"""Returns the one and only one BgpIpv4Peer object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv4peer.bgpipv4peer.BgpIpv4Peer)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv4peer.bgpipv4peer import BgpIpv4Peer
		return self._read(BgpIpv4Peer(self), None)

	@property
	def BgpIpv6Peer(self):
		"""Returns the one and only one BgpIpv6Peer object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv6peer.bgpipv6peer.BgpIpv6Peer)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.bgpipv6peer.bgpipv6peer import BgpIpv6Peer
		return self._read(BgpIpv6Peer(self), None)

	@property
	def CfmBridge(self):
		"""Returns the one and only one CfmBridge object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.cfmbridge.cfmbridge.CfmBridge)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.cfmbridge.cfmbridge import CfmBridge
		return self._read(CfmBridge(self), None)

	@property
	def Dhcpv4client(self):
		"""Returns the one and only one Dhcpv4client object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4client.dhcpv4client.Dhcpv4client)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4client.dhcpv4client import Dhcpv4client
		return self._read(Dhcpv4client(self), None)

	@property
	def Dhcpv4relayAgent(self):
		"""Returns the one and only one Dhcpv4relayAgent object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4relayagent.dhcpv4relayagent.Dhcpv4relayAgent)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4relayagent.dhcpv4relayagent import Dhcpv4relayAgent
		return self._read(Dhcpv4relayAgent(self), None)

	@property
	def Dhcpv4server(self):
		"""Returns the one and only one Dhcpv4server object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4server.dhcpv4server.Dhcpv4server)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv4server.dhcpv4server import Dhcpv4server
		return self._read(Dhcpv4server(self), None)

	@property
	def Dhcpv6client(self):
		"""Returns the one and only one Dhcpv6client object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6client.dhcpv6client.Dhcpv6client)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6client.dhcpv6client import Dhcpv6client
		return self._read(Dhcpv6client(self), None)

	@property
	def Dhcpv6relayAgent(self):
		"""Returns the one and only one Dhcpv6relayAgent object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6relayagent.dhcpv6relayagent.Dhcpv6relayAgent)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6relayagent.dhcpv6relayagent import Dhcpv6relayAgent
		return self._read(Dhcpv6relayAgent(self), None)

	@property
	def Dhcpv6server(self):
		"""Returns the one and only one Dhcpv6server object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6server.dhcpv6server.Dhcpv6server)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dhcpv6server.dhcpv6server import Dhcpv6server
		return self._read(Dhcpv6server(self), None)

	@property
	def DotOneX(self):
		"""Returns the one and only one DotOneX object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dotonex.dotonex.DotOneX)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.dotonex.dotonex import DotOneX
		return self._read(DotOneX(self), None)

	@property
	def Ethernet(self):
		"""Returns the one and only one Ethernet object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ethernet.ethernet.Ethernet)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ethernet.ethernet import Ethernet
		return self._read(Ethernet(self), None)

	@property
	def Geneve(self):
		"""Returns the one and only one Geneve object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.geneve.geneve.Geneve)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.geneve.geneve import Geneve
		return self._read(Geneve(self), None)

	@property
	def Greoipv4(self):
		"""Returns the one and only one Greoipv4 object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.greoipv4.greoipv4.Greoipv4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.greoipv4.greoipv4 import Greoipv4
		return self._read(Greoipv4(self), None)

	@property
	def Greoipv6(self):
		"""Returns the one and only one Greoipv6 object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.greoipv6.greoipv6.Greoipv6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.greoipv6.greoipv6 import Greoipv6
		return self._read(Greoipv6(self), None)

	@property
	def IgmpHost(self):
		"""Returns the one and only one IgmpHost object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.igmphost.igmphost.IgmpHost)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.igmphost.igmphost import IgmpHost
		return self._read(IgmpHost(self), None)

	@property
	def IgmpQuerier(self):
		"""Returns the one and only one IgmpQuerier object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.igmpquerier.igmpquerier.IgmpQuerier)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.igmpquerier.igmpquerier import IgmpQuerier
		return self._read(IgmpQuerier(self), None)

	@property
	def Ipv4(self):
		"""Returns the one and only one Ipv4 object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv4.ipv4.Ipv4)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv4.ipv4 import Ipv4
		return self._read(Ipv4(self), None)

	@property
	def Ipv6(self):
		"""Returns the one and only one Ipv6 object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv6.ipv6.Ipv6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv6.ipv6 import Ipv6
		return self._read(Ipv6(self), None)

	@property
	def Ipv6Autoconfiguration(self):
		"""Returns the one and only one Ipv6Autoconfiguration object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv6autoconfiguration.ipv6autoconfiguration.Ipv6Autoconfiguration)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ipv6autoconfiguration.ipv6autoconfiguration import Ipv6Autoconfiguration
		return self._read(Ipv6Autoconfiguration(self), None)

	def IsisFabricPathRouter(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisFabricPathRouter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisFabricPathRouter will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisfabricpathrouter.isisfabricpathrouter.IsisFabricPathRouter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisfabricpathrouter.isisfabricpathrouter import IsisFabricPathRouter
		return self._select(IsisFabricPathRouter(self), locals())

	def IsisL3Router(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisL3Router from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisL3Router will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisl3router.isisl3router.IsisL3Router))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisl3router.isisl3router import IsisL3Router
		return self._select(IsisL3Router(self), locals())

	@property
	def IsisSpbRouter(self):
		"""Returns the one and only one IsisSpbRouter object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisspbrouter.isisspbrouter.IsisSpbRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isisspbrouter.isisspbrouter import IsisSpbRouter
		return self._read(IsisSpbRouter(self), None)

	def IsisTrillRouter(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisTrillRouter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisTrillRouter will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isistrillrouter.isistrillrouter.IsisTrillRouter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.isistrillrouter.isistrillrouter import IsisTrillRouter
		return self._select(IsisTrillRouter(self), locals())

	@property
	def Lac(self):
		"""Returns the one and only one Lac object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lac.lac.Lac)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lac.lac import Lac
		return self._read(Lac(self), None)

	@property
	def Lacp(self):
		"""Returns the one and only one Lacp object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lacp.lacp.Lacp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lacp.lacp import Lacp
		return self._read(Lacp(self), None)

	@property
	def LdpBasicRouter(self):
		"""Returns the one and only one LdpBasicRouter object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldpbasicrouter.ldpbasicrouter.LdpBasicRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldpbasicrouter.ldpbasicrouter import LdpBasicRouter
		return self._read(LdpBasicRouter(self), None)

	@property
	def LdpBasicRouterV6(self):
		"""Returns the one and only one LdpBasicRouterV6 object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldpbasicrouterv6.ldpbasicrouterv6.LdpBasicRouterV6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldpbasicrouterv6.ldpbasicrouterv6 import LdpBasicRouterV6
		return self._read(LdpBasicRouterV6(self), None)

	@property
	def LdpTargetedRouter(self):
		"""Returns the one and only one LdpTargetedRouter object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldptargetedrouter.ldptargetedrouter.LdpTargetedRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldptargetedrouter.ldptargetedrouter import LdpTargetedRouter
		return self._read(LdpTargetedRouter(self), None)

	@property
	def LdpTargetedRouterV6(self):
		"""Returns the one and only one LdpTargetedRouterV6 object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldptargetedrouterv6.ldptargetedrouterv6.LdpTargetedRouterV6)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ldptargetedrouterv6.ldptargetedrouterv6 import LdpTargetedRouterV6
		return self._read(LdpTargetedRouterV6(self), None)

	@property
	def LightweightDhcpv6relayAgent(self):
		"""Returns the one and only one LightweightDhcpv6relayAgent object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lightweightdhcpv6relayagent.lightweightdhcpv6relayagent.LightweightDhcpv6relayAgent)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lightweightdhcpv6relayagent.lightweightdhcpv6relayagent import LightweightDhcpv6relayAgent
		return self._read(LightweightDhcpv6relayAgent(self), None)

	@property
	def Lns(self):
		"""Returns the one and only one Lns object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lns.lns.Lns)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.lns.lns import Lns
		return self._read(Lns(self), None)

	@property
	def MldHost(self):
		"""Returns the one and only one MldHost object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.mldhost.mldhost.MldHost)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.mldhost.mldhost import MldHost
		return self._read(MldHost(self), None)

	@property
	def MldQuerier(self):
		"""Returns the one and only one MldQuerier object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.mldquerier.mldquerier.MldQuerier)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.mldquerier.mldquerier import MldQuerier
		return self._read(MldQuerier(self), None)

	@property
	def MsrpListener(self):
		"""Returns the one and only one MsrpListener object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.msrplistener.msrplistener.MsrpListener)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.msrplistener.msrplistener import MsrpListener
		return self._read(MsrpListener(self), None)

	@property
	def MsrpTalker(self):
		"""Returns the one and only one MsrpTalker object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.msrptalker.msrptalker.MsrpTalker)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.msrptalker.msrptalker import MsrpTalker
		return self._read(MsrpTalker(self), None)

	@property
	def NetconfClient(self):
		"""Returns the one and only one NetconfClient object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.netconfclient.netconfclient.NetconfClient)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.netconfclient.netconfclient import NetconfClient
		return self._read(NetconfClient(self), None)

	@property
	def NetconfServer(self):
		"""Returns the one and only one NetconfServer object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.netconfserver.netconfserver.NetconfServer)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.netconfserver.netconfserver import NetconfServer
		return self._read(NetconfServer(self), None)

	@property
	def Nglacp(self):
		"""Returns the one and only one Nglacp object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.nglacp.nglacp.Nglacp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.nglacp.nglacp import Nglacp
		return self._read(Nglacp(self), None)

	@property
	def Ngstaticlag(self):
		"""Returns the one and only one Ngstaticlag object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ngstaticlag.ngstaticlag.Ngstaticlag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ngstaticlag.ngstaticlag import Ngstaticlag
		return self._read(Ngstaticlag(self), None)

	@property
	def Ntpclock(self):
		"""Returns the one and only one Ntpclock object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ntpclock.ntpclock.Ntpclock)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ntpclock.ntpclock import Ntpclock
		return self._read(Ntpclock(self), None)

	@property
	def OpenFlowChannel(self):
		"""Returns the one and only one OpenFlowChannel object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.openflowchannel.OpenFlowChannel)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.openflowchannel import OpenFlowChannel
		return self._read(OpenFlowChannel(self), None)

	@property
	def OpenFlowController(self):
		"""Returns the one and only one OpenFlowController object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.openflowcontroller.OpenFlowController)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowcontroller.openflowcontroller import OpenFlowController
		return self._read(OpenFlowController(self), None)

	def Ospfv2Router(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Ospfv2Router from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ospfv2Router will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv2router.ospfv2router.Ospfv2Router))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv2router.ospfv2router import Ospfv2Router
		return self._select(Ospfv2Router(self), locals())

	@property
	def Ospfv3Router(self):
		"""Returns the one and only one Ospfv3Router object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv3router.ospfv3router.Ospfv3Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv3router.ospfv3router import Ospfv3Router
		return self._read(Ospfv3Router(self), None)

	@property
	def Ovsdbcontroller(self):
		"""Returns the one and only one Ovsdbcontroller object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ovsdbcontroller.ovsdbcontroller.Ovsdbcontroller)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ovsdbcontroller.ovsdbcontroller import Ovsdbcontroller
		return self._read(Ovsdbcontroller(self), None)

	@property
	def Ovsdbserver(self):
		"""Returns the one and only one Ovsdbserver object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ovsdbserver.ovsdbserver.Ovsdbserver)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ovsdbserver.ovsdbserver import Ovsdbserver
		return self._read(Ovsdbserver(self), None)

	@property
	def Pcc(self):
		"""Returns the one and only one Pcc object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pcc.pcc.Pcc)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pcc.pcc import Pcc
		return self._read(Pcc(self), None)

	@property
	def PimRouter(self):
		"""Returns the one and only one PimRouter object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pimrouter.pimrouter.PimRouter)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pimrouter.pimrouter import PimRouter
		return self._read(PimRouter(self), None)

	@property
	def Pppoxclient(self):
		"""Returns the one and only one Pppoxclient object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pppoxclient.pppoxclient.Pppoxclient)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pppoxclient.pppoxclient import Pppoxclient
		return self._read(Pppoxclient(self), None)

	@property
	def Pppoxserver(self):
		"""Returns the one and only one Pppoxserver object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pppoxserver.pppoxserver.Pppoxserver)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.pppoxserver.pppoxserver import Pppoxserver
		return self._read(Pppoxserver(self), None)

	@property
	def Ptp(self):
		"""Returns the one and only one Ptp object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ptp.ptp.Ptp)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ptp.ptp import Ptp
		return self._read(Ptp(self), None)

	@property
	def RsvpteIf(self):
		"""Returns the one and only one RsvpteIf object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.rsvpteif.rsvpteif.RsvpteIf)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.rsvpteif.rsvpteif import RsvpteIf
		return self._read(RsvpteIf(self), None)

	@property
	def RsvpteLsps(self):
		"""Returns the one and only one RsvpteLsps object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.rsvptelsps.rsvptelsps.RsvpteLsps)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.rsvptelsps.rsvptelsps import RsvpteLsps
		return self._read(RsvpteLsps(self), None)

	@property
	def StaticLag(self):
		"""Returns the one and only one StaticLag object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.staticlag.staticlag.StaticLag)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.staticlag.staticlag import StaticLag
		return self._read(StaticLag(self), None)

	@property
	def Vxlan(self):
		"""Returns the one and only one Vxlan object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.vxlan.vxlan.Vxlan)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.vxlan.vxlan import Vxlan
		return self._read(Vxlan(self), None)

	@property
	def ApplyOnTheFlyState(self):
		"""Checks whether the apply changes operation is allowed

		Returns:
			str(allowed|notAllowed|nothingToApply)
		"""
		return self._get_attribute('applyOnTheFlyState')

	@property
	def NgpfProtocolRateMode(self):
		"""Decides whether protocol's sessions will started in normal or smooth mode

		Returns:
			str(basic|smooth)
		"""
		return self._get_attribute('ngpfProtocolRateMode')
	@NgpfProtocolRateMode.setter
	def NgpfProtocolRateMode(self, value):
		self._set_attribute('ngpfProtocolRateMode', value)

	@property
	def ProtocolActionsInProgress(self):
		"""Lists all current protocol actions in progress

		Returns:
			list(str)
		"""
		return self._get_attribute('protocolActionsInProgress')

	@property
	def ProtocolStackingMode(self):
		"""Decides whether protocol's sessions will started sequentially or parallelly across the layers

		Returns:
			str(parallel|sequential)
		"""
		return self._get_attribute('protocolStackingMode')
	@ProtocolStackingMode.setter
	def ProtocolStackingMode(self, value):
		self._set_attribute('protocolStackingMode', value)

	@property
	def Status(self):
		"""The current state of the scenario

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	@property
	def Vports(self):
		"""List of virtual ports included in the port level configuration

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/vport])
		"""
		return self._get_attribute('vports')

	def AbortApplyOnTheFly(self):
		"""Executes the abortApplyOnTheFly operation on the server.

		Aborts any on the fly changes that are outstanding

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('abortApplyOnTheFly', payload=locals(), response_object=None)

	def ApplyOnTheFly(self):
		"""Executes the applyOnTheFly operation on the server.

		Apply any outstanding on the fly changes

		Returns:
			str: Details about the operation's state.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('applyOnTheFly', payload=locals(), response_object=None)

	def ConfigureAll(self):
		"""Executes the configureAll operation on the server.

		Configures all protocols in current scenario

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('configureAll', payload=locals(), response_object=None)

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
