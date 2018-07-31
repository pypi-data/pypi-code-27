from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OspfPseudoRouter(Base):
	"""Simulated Router Information
	"""

	_SDM_NAME = 'ospfPseudoRouter'

	def __init__(self, parent):
		super(OspfPseudoRouter, self).__init__(parent)

	def OspfPseudoRouterStubNetworks(self, DescriptiveName=None, Name=None):
		"""Gets child instances of OspfPseudoRouterStubNetworks from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of OspfPseudoRouterStubNetworks will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudorouterstubnetworks.OspfPseudoRouterStubNetworks))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudorouterstubnetworks import OspfPseudoRouterStubNetworks
		return self._select(OspfPseudoRouterStubNetworks(self), locals())

	def OspfPseudoRouterStubRoutes(self, DescriptiveName=None, Name=None):
		"""Gets child instances of OspfPseudoRouterStubRoutes from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of OspfPseudoRouterStubRoutes will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudorouterstubroutes.OspfPseudoRouterStubRoutes))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudorouterstubroutes import OspfPseudoRouterStubRoutes
		return self._select(OspfPseudoRouterStubRoutes(self), locals())

	def OspfPseudoRouterSummaryRoutes(self, DescriptiveName=None, Name=None):
		"""Gets child instances of OspfPseudoRouterSummaryRoutes from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of OspfPseudoRouterSummaryRoutes will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudoroutersummaryroutes.OspfPseudoRouterSummaryRoutes))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudoroutersummaryroutes import OspfPseudoRouterSummaryRoutes
		return self._select(OspfPseudoRouterSummaryRoutes(self), locals())

	def OspfPseudoRouterType1ExtRoutes(self, DescriptiveName=None, Name=None):
		"""Gets child instances of OspfPseudoRouterType1ExtRoutes from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of OspfPseudoRouterType1ExtRoutes will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudoroutertype1extroutes.OspfPseudoRouterType1ExtRoutes))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudoroutertype1extroutes import OspfPseudoRouterType1ExtRoutes
		return self._select(OspfPseudoRouterType1ExtRoutes(self), locals())

	def OspfPseudoRouterType2ExtRoutes(self, DescriptiveName=None, Name=None):
		"""Gets child instances of OspfPseudoRouterType2ExtRoutes from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of OspfPseudoRouterType2ExtRoutes will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudoroutertype2extroutes.OspfPseudoRouterType2ExtRoutes))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfpseudoroutertype2extroutes import OspfPseudoRouterType2ExtRoutes
		return self._select(OspfPseudoRouterType2ExtRoutes(self), locals())

	def OspfSRAlgorithmList(self, DescriptiveName=None, Name=None):
		"""Gets child instances of OspfSRAlgorithmList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of OspfSRAlgorithmList will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsralgorithmlist.OspfSRAlgorithmList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsralgorithmlist import OspfSRAlgorithmList
		return self._select(OspfSRAlgorithmList(self), locals())

	def OspfSRGBRangeSubObjectsList(self, DescriptiveName=None, Name=None):
		"""Gets child instances of OspfSRGBRangeSubObjectsList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of OspfSRGBRangeSubObjectsList will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsrgbrangesubobjectslist.OspfSRGBRangeSubObjectsList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.ospfsrgbrangesubobjectslist import OspfSRGBRangeSubObjectsList
		return self._select(OspfSRGBRangeSubObjectsList(self), locals())

	@property
	def Active(self):
		"""Activate/DeActivate OSPF Simulated Router

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AdvertiseRouterIdAsStubNetwork(self):
		"""Advertise RouterId As Stub Network

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('advertiseRouterIdAsStubNetwork')

	@property
	def Algorithm(self):
		"""Algorithm for the Node SID/Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('algorithm')

	@property
	def BBit(self):
		"""Router-LSA B-Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bBit')

	@property
	def ConfigureSIDIndexLabel(self):
		"""Configure SID/Index/Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('configureSIDIndexLabel')

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
	def EBit(self):
		"""Router-LSA E-Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('eBit')

	@property
	def EFlag(self):
		"""Explicit-Null Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('eFlag')

	@property
	def EnableSegmentRouting(self):
		"""Enable Segment Routing

		Returns:
			bool
		"""
		return self._get_attribute('enableSegmentRouting')
	@EnableSegmentRouting.setter
	def EnableSegmentRouting(self, value):
		self._set_attribute('enableSegmentRouting', value)

	@property
	def LFlag(self):
		"""Local or Global Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lFlag')

	@property
	def MFlag(self):
		"""Mapping Server Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mFlag')

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
	def NpFlag(self):
		"""No-PHP Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('npFlag')

	@property
	def SRAlgorithmCount(self):
		"""SR Algorithm Count

		Returns:
			number
		"""
		return self._get_attribute('sRAlgorithmCount')
	@SRAlgorithmCount.setter
	def SRAlgorithmCount(self, value):
		self._set_attribute('sRAlgorithmCount', value)

	@property
	def SidIndexLabel(self):
		"""SID/Index/Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sidIndexLabel')

	@property
	def SrgbRangeCount(self):
		"""SRGB Range Count

		Returns:
			number
		"""
		return self._get_attribute('srgbRangeCount')
	@SrgbRangeCount.setter
	def SrgbRangeCount(self, value):
		self._set_attribute('srgbRangeCount', value)

	@property
	def VFlag(self):
		"""Value or Index Flag

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vFlag')

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

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfPseudoRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfPseudoRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfPseudoRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Stop Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfPseudoRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfPseudoRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfPseudoRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
