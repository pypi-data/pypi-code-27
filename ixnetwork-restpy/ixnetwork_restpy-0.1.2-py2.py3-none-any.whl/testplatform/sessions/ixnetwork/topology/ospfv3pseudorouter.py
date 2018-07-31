from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ospfv3PseudoRouter(Base):
	"""Simulated Router Information
	"""

	_SDM_NAME = 'ospfv3PseudoRouter'

	def __init__(self, parent):
		super(Ospfv3PseudoRouter, self).__init__(parent)

	def ExternalRoutes(self, DescriptiveName=None, Name=None):
		"""Gets child instances of ExternalRoutes from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of ExternalRoutes will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.externalroutes.ExternalRoutes))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.externalroutes import ExternalRoutes
		return self._select(ExternalRoutes(self), locals())

	def InterAreaPrefix(self, DescriptiveName=None, Name=None):
		"""Gets child instances of InterAreaPrefix from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of InterAreaPrefix will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interareaprefix.InterAreaPrefix))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interareaprefix import InterAreaPrefix
		return self._select(InterAreaPrefix(self), locals())

	def InterAreaRouter(self, DescriptiveName=None, Name=None):
		"""Gets child instances of InterAreaRouter from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of InterAreaRouter will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interarearouter.InterAreaRouter))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.interarearouter import InterAreaRouter
		return self._select(InterAreaRouter(self), locals())

	def IntraAreaPrefix(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IntraAreaPrefix from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IntraAreaPrefix will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.intraareaprefix.IntraAreaPrefix))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.intraareaprefix import IntraAreaPrefix
		return self._select(IntraAreaPrefix(self), locals())

	def LinkLsaRoutes(self, DescriptiveName=None, Name=None):
		"""Gets child instances of LinkLsaRoutes from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of LinkLsaRoutes will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.linklsaroutes.LinkLsaRoutes))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.linklsaroutes import LinkLsaRoutes
		return self._select(LinkLsaRoutes(self), locals())

	def NssaRoutes(self, DescriptiveName=None, Name=None):
		"""Gets child instances of NssaRoutes from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of NssaRoutes will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nssaroutes.NssaRoutes))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.nssaroutes import NssaRoutes
		return self._select(NssaRoutes(self), locals())

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def BBit(self):
		"""Router-LSA B-Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bBit')

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
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

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

	def Start(self, Targets):
		"""Executes the start operation on the server.

		Start CPF control plane (equals to promote to negotiated state).

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfv3PseudoRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def StartSimulatedRouter(self, Arg1):
		"""Executes the startSimulatedRouter operation on the server.

		Start Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfv3PseudoRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startSimulatedRouter', payload=locals(), response_object=None)

	def StartSimulatedRouter(self, Arg1, SessionIndices):
		"""Executes the startSimulatedRouter operation on the server.

		Start Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfv3PseudoRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startSimulatedRouter', payload=locals(), response_object=None)

	def StartSimulatedRouter(self, Arg1, SessionIndices):
		"""Executes the startSimulatedRouter operation on the server.

		Start Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfv3PseudoRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('startSimulatedRouter', payload=locals(), response_object=None)

	def StartSimulatedRouter(self, Arg2):
		"""Executes the startSimulatedRouter operation on the server.

		Shutdown OSPFv3 state machine on this simulated router.

		Args:
			Arg2 (list(number)): List of indices into the network info. An empty list indicates all instances in the node specific data.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('startSimulatedRouter', payload=locals(), response_object=None)

	def Stop(self, Targets):
		"""Executes the stop operation on the server.

		Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfv3PseudoRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def StopSimulatedRouter(self, Arg1):
		"""Executes the stopSimulatedRouter operation on the server.

		Stop Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfv3PseudoRouter object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopSimulatedRouter', payload=locals(), response_object=None)

	def StopSimulatedRouter(self, Arg1, SessionIndices):
		"""Executes the stopSimulatedRouter operation on the server.

		Stop Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfv3PseudoRouter object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopSimulatedRouter', payload=locals(), response_object=None)

	def StopSimulatedRouter(self, Arg1, SessionIndices):
		"""Executes the stopSimulatedRouter operation on the server.

		Stop Pseudo Router

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./ospfv3PseudoRouter object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopSimulatedRouter', payload=locals(), response_object=None)

	def StopSimulatedRouter(self, Arg2):
		"""Executes the stopSimulatedRouter operation on the server.

		Withdraws all the routes mentioned in this route range.

		Args:
			Arg2 (list(number)): List of indices into the network info. An empty list indicates all instances in the network info.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stopSimulatedRouter', payload=locals(), response_object=None)
