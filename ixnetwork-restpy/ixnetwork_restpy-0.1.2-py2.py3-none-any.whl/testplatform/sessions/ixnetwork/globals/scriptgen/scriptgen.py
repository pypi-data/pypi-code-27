from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Scriptgen(Base):
	"""Container for scriptgen options
	"""

	_SDM_NAME = 'scriptgen'

	def __init__(self, parent):
		super(Scriptgen, self).__init__(parent)

	@property
	def Base64CodeOptions(self):
		"""Returns the one and only one Base64CodeOptions object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.base64codeoptions.base64codeoptions.Base64CodeOptions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.base64codeoptions.base64codeoptions import Base64CodeOptions
		return self._read(Base64CodeOptions(self), None)

	@property
	def IxNetCodeOptions(self):
		"""Returns the one and only one IxNetCodeOptions object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.ixnetcodeoptions.ixnetcodeoptions.IxNetCodeOptions)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.scriptgen.ixnetcodeoptions.ixnetcodeoptions import IxNetCodeOptions
		return self._read(IxNetCodeOptions(self), None)

	@property
	def ConnectHostname(self):
		"""The hostname to be used in the connect command

		Returns:
			str
		"""
		return self._get_attribute('connectHostname')
	@ConnectHostname.setter
	def ConnectHostname(self, value):
		self._set_attribute('connectHostname', value)

	@property
	def ConnectPort(self):
		"""The port number to be used in the connect command

		Returns:
			number
		"""
		return self._get_attribute('connectPort')
	@ConnectPort.setter
	def ConnectPort(self, value):
		self._set_attribute('connectPort', value)

	@property
	def ConnectVersion(self):
		"""The version number to be used in the connect command

		Returns:
			str
		"""
		return self._get_attribute('connectVersion')
	@ConnectVersion.setter
	def ConnectVersion(self, value):
		self._set_attribute('connectVersion', value)

	@property
	def IncludeConnect(self):
		"""Flag to include the connect command

		Returns:
			bool
		"""
		return self._get_attribute('includeConnect')
	@IncludeConnect.setter
	def IncludeConnect(self, value):
		self._set_attribute('includeConnect', value)

	@property
	def IncludeTestComposer(self):
		"""Flag to include test composer code

		Returns:
			bool
		"""
		return self._get_attribute('includeTestComposer')
	@IncludeTestComposer.setter
	def IncludeTestComposer(self, value):
		self._set_attribute('includeTestComposer', value)

	@property
	def Language(self):
		"""Select the target scriptgen language

		Returns:
			str(perl|python|ruby|tcl)
		"""
		return self._get_attribute('language')
	@Language.setter
	def Language(self, value):
		self._set_attribute('language', value)

	@property
	def LinePerAttribute(self):
		"""If true the scriptgen output will show each attribute on a separate line

		Returns:
			bool
		"""
		return self._get_attribute('linePerAttribute')
	@LinePerAttribute.setter
	def LinePerAttribute(self, value):
		self._set_attribute('linePerAttribute', value)

	@property
	def OverwriteScriptFilename(self):
		"""If true the file indicated by the script filename will be overwritten

		Returns:
			bool
		"""
		return self._get_attribute('overwriteScriptFilename')
	@OverwriteScriptFilename.setter
	def OverwriteScriptFilename(self, value):
		self._set_attribute('overwriteScriptFilename', value)

	@property
	def ScriptFilename(self):
		"""The name of the target scriptgen file

		Returns:
			str
		"""
		return self._get_attribute('scriptFilename')
	@ScriptFilename.setter
	def ScriptFilename(self, value):
		self._set_attribute('scriptFilename', value)

	@property
	def SerializationType(self):
		"""The scriptgen serialization type

		Returns:
			str(base64|ixNet)
		"""
		return self._get_attribute('serializationType')
	@SerializationType.setter
	def SerializationType(self, value):
		self._set_attribute('serializationType', value)

	def Generate(self):
		"""Executes the generate operation on the server.

		Generate a script of the currently loaded configuration using the options in the /globals/scriptgen hierarchy.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('generate', payload=locals(), response_object=None)

	def Generate(self, Arg2):
		"""Executes the generate operation on the server.

		Generate a script of the currently loaded configuration using the options in the /globals/scriptgen hierarchy.

		Args:
			Arg2 (obj(ixnetwork_restpy.files.Files)): A valid writeTo file handle the script will be written to.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		self._check_arg_type(Arg2, Files)
		return self._execute('generate', payload=locals(), response_object=None)
