from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Globals(Base):
	"""This object holds the configurable global values of IxNetwork for interfaces and the protocol stack.
	"""

	_SDM_NAME = 'globals'

	def __init__(self, parent):
		super(Globals, self).__init__(parent)

	def AppErrors(self, LastModified=None):
		"""Gets child instances of AppErrors from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AppErrors will be returned.

		Args:
			LastModified (str): Time of latest logged error or warning

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.apperrors.AppErrors))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.apperrors import AppErrors
		return self._select(AppErrors(self), locals())

	@property
	def Interfaces(self):
		"""Returns the one and only one Interfaces object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.interfaces.interfaces.Interfaces)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.interfaces.interfaces import Interfaces
		return self._read(Interfaces(self), None)

	@property
	def Ixnet(self):
		"""Returns the one and only one Ixnet object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.ixnet.ixnet.Ixnet)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.ixnet.ixnet import Ixnet
		return self._read(Ixnet(self), None)

	@property
	def Licensing(self):
		"""Returns the one and only one Licensing object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.licensing.licensing.Licensing)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.licensing.licensing import Licensing
		return self._read(Licensing(self), None)

	@property
	def Preferences(self):
		"""Returns the one and only one Preferences object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.preferences.preferences.Preferences)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.preferences.preferences import Preferences
		return self._read(Preferences(self), None)

	@property
	def Scriptgen(self):
		"""Returns the one and only one Scriptgen object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.scriptgen.Scriptgen)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.scriptgen import Scriptgen
		return self._read(Scriptgen(self), None)

	@property
	def Topology(self):
		"""Returns the one and only one Topology object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.topology.Topology)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.topology import Topology
		return self._read(Topology(self), None)

	@property
	def BuildNumber(self):
		"""The IxNetwork software build number.

		Returns:
			str
		"""
		return self._get_attribute('buildNumber')

	@property
	def ConfigFileName(self):
		"""The name of the configuration file.

		Returns:
			str
		"""
		return self._get_attribute('configFileName')

	@property
	def ConfigSummary(self):
		"""A high level summary description of the currently loaded configuration

		Returns:
			list(dict(arg1:str,arg2:str,arg3:list[dict(arg1:str,arg2:str)]))
		"""
		return self._get_attribute('configSummary')

	@property
	def IsConfigDifferent(self):
		"""(Read only) If true, then the current IxNetwork configuration is different than the configuration that was previously loaded.

		Returns:
			bool
		"""
		return self._get_attribute('isConfigDifferent')

	@property
	def IxosBuildNumber(self):
		"""The IxOS software build number.

		Returns:
			str
		"""
		return self._get_attribute('ixosBuildNumber')

	@property
	def PersistencePath(self):
		"""This attribute returns a directory of the IxNetwork API server machine, where users can drop their files from the client scripts using IxNetwork APIs. To Put files in this directory, users do not require to run IxNetwork API server in administrative mode

		Returns:
			str
		"""
		return self._get_attribute('persistencePath')

	@property
	def ProtocolbuildNumber(self):
		"""The build number of the protocol.

		Returns:
			str
		"""
		return self._get_attribute('protocolbuildNumber')

	@property
	def Username(self):
		"""The name of the user.

		Returns:
			str
		"""
		return self._get_attribute('username')
