from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IsisPseudoInterface(Base):
	"""Information for Simulated Router Interfaces
	"""

	_SDM_NAME = 'isisPseudoInterface'

	def __init__(self, parent):
		super(IsisPseudoInterface, self).__init__(parent)

	def IsisDcePseudoIfaceAttPoint1Config(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisDcePseudoIfaceAttPoint1Config from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisDcePseudoIfaceAttPoint1Config will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcepseudoifaceattpoint1config.IsisDcePseudoIfaceAttPoint1Config))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcepseudoifaceattpoint1config import IsisDcePseudoIfaceAttPoint1Config
		return self._select(IsisDcePseudoIfaceAttPoint1Config(self), locals())

	def IsisDcePseudoIfaceAttPoint2Config(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisDcePseudoIfaceAttPoint2Config from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisDcePseudoIfaceAttPoint2Config will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcepseudoifaceattpoint2config.IsisDcePseudoIfaceAttPoint2Config))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisdcepseudoifaceattpoint2config import IsisDcePseudoIfaceAttPoint2Config
		return self._select(IsisDcePseudoIfaceAttPoint2Config(self), locals())

	def IsisL3PseudoIfaceAttPoint1Config(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisL3PseudoIfaceAttPoint1Config from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisL3PseudoIfaceAttPoint1Config will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3pseudoifaceattpoint1config.IsisL3PseudoIfaceAttPoint1Config))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3pseudoifaceattpoint1config import IsisL3PseudoIfaceAttPoint1Config
		return self._select(IsisL3PseudoIfaceAttPoint1Config(self), locals())

	def IsisL3PseudoIfaceAttPoint2Config(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisL3PseudoIfaceAttPoint2Config from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisL3PseudoIfaceAttPoint2Config will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3pseudoifaceattpoint2config.IsisL3PseudoIfaceAttPoint2Config))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisl3pseudoifaceattpoint2config import IsisL3PseudoIfaceAttPoint2Config
		return self._select(IsisL3PseudoIfaceAttPoint2Config(self), locals())

	def IsisSpbPseudoIfaceAttPoint1Config(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisSpbPseudoIfaceAttPoint1Config from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisSpbPseudoIfaceAttPoint1Config will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbpseudoifaceattpoint1config.IsisSpbPseudoIfaceAttPoint1Config))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbpseudoifaceattpoint1config import IsisSpbPseudoIfaceAttPoint1Config
		return self._select(IsisSpbPseudoIfaceAttPoint1Config(self), locals())

	def IsisSpbPseudoIfaceAttPoint2Config(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisSpbPseudoIfaceAttPoint2Config from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisSpbPseudoIfaceAttPoint2Config will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbpseudoifaceattpoint2config.IsisSpbPseudoIfaceAttPoint2Config))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisspbpseudoifaceattpoint2config import IsisSpbPseudoIfaceAttPoint2Config
		return self._select(IsisSpbPseudoIfaceAttPoint2Config(self), locals())

	def IsisTrillPseudoIfaceAttPoint1Config(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisTrillPseudoIfaceAttPoint1Config from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisTrillPseudoIfaceAttPoint1Config will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillpseudoifaceattpoint1config.IsisTrillPseudoIfaceAttPoint1Config))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillpseudoifaceattpoint1config import IsisTrillPseudoIfaceAttPoint1Config
		return self._select(IsisTrillPseudoIfaceAttPoint1Config(self), locals())

	def IsisTrillPseudoIfaceAttPoint2Config(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisTrillPseudoIfaceAttPoint2Config from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisTrillPseudoIfaceAttPoint2Config will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillpseudoifaceattpoint2config.IsisTrillPseudoIfaceAttPoint2Config))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isistrillpseudoifaceattpoint2config import IsisTrillPseudoIfaceAttPoint2Config
		return self._select(IsisTrillPseudoIfaceAttPoint2Config(self), locals())

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
	def LinkType(self):
		"""Link Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('linkType')

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
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisPseudoInterface object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Targets):
		"""Executes the stop operation on the server.

		Stop CPF control plane (equals to demote to PreValidated-DoDDone state).

		Args:
			Targets (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./isisPseudoInterface object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
