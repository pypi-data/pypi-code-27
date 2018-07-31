from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetworkTopology(Base):
	"""Container for Network Topology related objects
	"""

	_SDM_NAME = 'networkTopology'

	def __init__(self, parent):
		super(NetworkTopology, self).__init__(parent)

	def ExternalLink(self):
		"""Gets child instances of ExternalLink from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of ExternalLink will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.externallink.ExternalLink))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.externallink import ExternalLink
		return self._select(ExternalLink(self), locals())

	def add_ExternalLink(self, FromNodeIndex="0", ToNetworkTopology=None, ToNodeIndex="0"):
		"""Adds a child instance of ExternalLink on the server.

		Args:
			FromNodeIndex (number): Index of the originating node as defined in fromNetworkTopology
			ToNetworkTopology (str(None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): Network Topology this link is pointing to
			ToNodeIndex (number): Index of the target node as defined in toNetworkTopology

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.externallink.ExternalLink)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.externallink import ExternalLink
		return self._create(ExternalLink(self), locals())

	def IsisDceSimulatedTopologyConfig(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisDceSimulatedTopologyConfig from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisDceSimulatedTopologyConfig will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcesimulatedtopologyconfig.IsisDceSimulatedTopologyConfig))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcesimulatedtopologyconfig import IsisDceSimulatedTopologyConfig
		return self._select(IsisDceSimulatedTopologyConfig(self), locals())

	def IsisL3SimulatedTopologyConfig(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisL3SimulatedTopologyConfig from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisL3SimulatedTopologyConfig will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3simulatedtopologyconfig.IsisL3SimulatedTopologyConfig))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3simulatedtopologyconfig import IsisL3SimulatedTopologyConfig
		return self._select(IsisL3SimulatedTopologyConfig(self), locals())

	def IsisSpbSimulatedTopologyConfig(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisSpbSimulatedTopologyConfig from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisSpbSimulatedTopologyConfig will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbsimulatedtopologyconfig.IsisSpbSimulatedTopologyConfig))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbsimulatedtopologyconfig import IsisSpbSimulatedTopologyConfig
		return self._select(IsisSpbSimulatedTopologyConfig(self), locals())

	def IsisTrillSimulatedTopologyConfig(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisTrillSimulatedTopologyConfig from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisTrillSimulatedTopologyConfig will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillsimulatedtopologyconfig.IsisTrillSimulatedTopologyConfig))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillsimulatedtopologyconfig import IsisTrillSimulatedTopologyConfig
		return self._select(IsisTrillSimulatedTopologyConfig(self), locals())

	def LdpSimulatedTopologyConfig(self, DescriptiveName=None, Name=None):
		"""Gets child instances of LdpSimulatedTopologyConfig from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of LdpSimulatedTopologyConfig will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpsimulatedtopologyconfig.LdpSimulatedTopologyConfig))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ldpsimulatedtopologyconfig import LdpSimulatedTopologyConfig
		return self._select(LdpSimulatedTopologyConfig(self), locals())

	def NetTopologyCustom(self):
		"""Gets child instances of NetTopologyCustom from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetTopologyCustom will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologycustom.NetTopologyCustom))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologycustom import NetTopologyCustom
		return self._select(NetTopologyCustom(self), locals())

	def add_NetTopologyCustom(self, IncludeEntryPoint="False", LinkMultiplier="1"):
		"""Adds a child instance of NetTopologyCustom on the server.

		Args:
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologycustom.NetTopologyCustom)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologycustom import NetTopologyCustom
		return self._create(NetTopologyCustom(self), locals())

	def NetTopologyFatTree(self):
		"""Gets child instances of NetTopologyFatTree from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetTopologyFatTree will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyfattree.NetTopologyFatTree))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyfattree import NetTopologyFatTree
		return self._select(NetTopologyFatTree(self), locals())

	def add_NetTopologyFatTree(self, IncludeEntryPoint="False", LevelCount="2", LinkMultiplier="1"):
		"""Adds a child instance of NetTopologyFatTree on the server.

		Args:
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LevelCount (number): Number of Levels
			LinkMultiplier (number): number of links between two nodes

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyfattree.NetTopologyFatTree)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyfattree import NetTopologyFatTree
		return self._create(NetTopologyFatTree(self), locals())

	def NetTopologyGrid(self):
		"""Gets child instances of NetTopologyGrid from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetTopologyGrid will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologygrid.NetTopologyGrid))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologygrid import NetTopologyGrid
		return self._select(NetTopologyGrid(self), locals())

	def add_NetTopologyGrid(self, Columns="3", IncludeEntryPoint="False", LinkMultiplier="1", Rows="3"):
		"""Adds a child instance of NetTopologyGrid on the server.

		Args:
			Columns (number): number of columns
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes
			Rows (number): number of rows

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologygrid.NetTopologyGrid)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologygrid import NetTopologyGrid
		return self._create(NetTopologyGrid(self), locals())

	def NetTopologyHubNSpoke(self):
		"""Gets child instances of NetTopologyHubNSpoke from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetTopologyHubNSpoke will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyhubnspoke.NetTopologyHubNSpoke))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyhubnspoke import NetTopologyHubNSpoke
		return self._select(NetTopologyHubNSpoke(self), locals())

	def add_NetTopologyHubNSpoke(self, EnableLevel2Spokes="False", IncludeEntryPoint="False", LinkMultiplier="1", NumberOfFirstLevelSpokes="3", NumberOfSecondLevelSpokes="2"):
		"""Adds a child instance of NetTopologyHubNSpoke on the server.

		Args:
			EnableLevel2Spokes (bool): Enable Level 2 Spokes
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes
			NumberOfFirstLevelSpokes (number): Number of First Level Spokes
			NumberOfSecondLevelSpokes (number): Number of Second Level Spokes

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyhubnspoke.NetTopologyHubNSpoke)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyhubnspoke import NetTopologyHubNSpoke
		return self._create(NetTopologyHubNSpoke(self), locals())

	def NetTopologyLinear(self):
		"""Gets child instances of NetTopologyLinear from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetTopologyLinear will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologylinear.NetTopologyLinear))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologylinear import NetTopologyLinear
		return self._select(NetTopologyLinear(self), locals())

	def add_NetTopologyLinear(self, IncludeEntryPoint="False", LinkMultiplier="1", Nodes="1"):
		"""Adds a child instance of NetTopologyLinear on the server.

		Args:
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes
			Nodes (number): number of nodes

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologylinear.NetTopologyLinear)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologylinear import NetTopologyLinear
		return self._create(NetTopologyLinear(self), locals())

	def NetTopologyMesh(self):
		"""Gets child instances of NetTopologyMesh from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetTopologyMesh will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologymesh.NetTopologyMesh))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologymesh import NetTopologyMesh
		return self._select(NetTopologyMesh(self), locals())

	def add_NetTopologyMesh(self, IncludeEntryPoint="False", LinkMultiplier="1", Nodes="3"):
		"""Adds a child instance of NetTopologyMesh on the server.

		Args:
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes
			Nodes (number): number of nodes

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologymesh.NetTopologyMesh)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologymesh import NetTopologyMesh
		return self._create(NetTopologyMesh(self), locals())

	def NetTopologyRing(self):
		"""Gets child instances of NetTopologyRing from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetTopologyRing will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyring.NetTopologyRing))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyring import NetTopologyRing
		return self._select(NetTopologyRing(self), locals())

	def add_NetTopologyRing(self, IncludeEntryPoint="False", LinkMultiplier="1", Nodes="3"):
		"""Adds a child instance of NetTopologyRing on the server.

		Args:
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes
			Nodes (number): number of nodes

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyring.NetTopologyRing)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologyring import NetTopologyRing
		return self._create(NetTopologyRing(self), locals())

	def NetTopologyTree(self):
		"""Gets child instances of NetTopologyTree from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NetTopologyTree will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologytree.NetTopologyTree))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologytree import NetTopologyTree
		return self._select(NetTopologyTree(self), locals())

	def add_NetTopologyTree(self, IncludeEntryPoint="False", LinkMultiplier="1", MaxChildPerNode="3", Nodes="7", TreeDepth="2", UseTreeDepth="False"):
		"""Adds a child instance of NetTopologyTree on the server.

		Args:
			IncludeEntryPoint (bool): if true, entry node belongs to ring topology, otherwise it is outside of ring
			LinkMultiplier (number): number of links between two nodes
			MaxChildPerNode (number): Maximum children per node
			Nodes (number): number of nodes
			TreeDepth (number): Depth of the Tree, defined as length of path from root node to deepest node in the tree
			UseTreeDepth (bool): Use Tree Depth

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologytree.NetTopologyTree)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nettopologytree import NetTopologyTree
		return self._create(NetTopologyTree(self), locals())

	def OspfSimulatedTopologyConfig(self, DescriptiveName=None, Name=None):
		"""Gets child instances of OspfSimulatedTopologyConfig from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of OspfSimulatedTopologyConfig will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsimulatedtopologyconfig.OspfSimulatedTopologyConfig))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsimulatedtopologyconfig import OspfSimulatedTopologyConfig
		return self._select(OspfSimulatedTopologyConfig(self), locals())

	def Ospfv3SimulatedTopologyConfig(self, DescriptiveName=None, Name=None):
		"""Gets child instances of Ospfv3SimulatedTopologyConfig from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Ospfv3SimulatedTopologyConfig will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3simulatedtopologyconfig.Ospfv3SimulatedTopologyConfig))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfv3simulatedtopologyconfig import Ospfv3SimulatedTopologyConfig
		return self._select(Ospfv3SimulatedTopologyConfig(self), locals())

	def SimInterface(self, DescriptiveName=None, Name=None):
		"""Gets child instances of SimInterface from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of SimInterface will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.siminterface.SimInterface))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.siminterface import SimInterface
		return self._select(SimInterface(self), locals())

	def SimRouter(self, DescriptiveName=None, Name=None):
		"""Gets child instances of SimRouter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of SimRouter will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.simrouter.SimRouter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.simrouter import SimRouter
		return self._select(SimRouter(self), locals())

	def SimRouterBridge(self, DescriptiveName=None, Name=None):
		"""Gets child instances of SimRouterBridge from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of SimRouterBridge will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.simrouterbridge.SimRouterBridge))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.simrouterbridge import SimRouterBridge
		return self._select(SimRouterBridge(self), locals())

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def LinksPerNetwork(self):
		"""linksPerNetwork is controled by assigned topology

		Returns:
			number
		"""
		return self._get_attribute('linksPerNetwork')

	@property
	def NodesPerNetwork(self):
		"""Number of nodes in the Network Topology, including the root node defined in the parent Device Group

		Returns:
			number
		"""
		return self._get_attribute('nodesPerNetwork')

	def remove(self):
		"""Deletes a child instance of NetworkTopology on the server.

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
