from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ResourceManager(Base):
	"""Top level node for resource manager API
	"""

	_SDM_NAME = 'resourceManager'

	def __init__(self, parent):
		super(ResourceManager, self).__init__(parent)

	def ExportConfig(self, Arg2, Arg3, Arg4):
		"""Executes the exportConfig operation on the server.

		Export the entire configuration or fragments of it in a text based format

		Args:
			Arg2 (list(str)): A list of xpaths each of which is a starting point in the configuration. The only supported xpath notation is by index or descendant-or-self:*. To export the entire configuration specify /descendant-or-self:*
			Arg3 (bool): True to include attributes that are equal to the default in the export, false to exclude them
			Arg4 (str(json)): The format of the exported configuration

		Returns:
			str: JSON configuration as a string

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('exportConfig', payload=locals(), response_object=None)

	def ExportConfigFile(self, Arg2, Arg3, Arg4, Arg5):
		"""Executes the exportConfigFile operation on the server.

		Export the entire configuration or fragments of it in a text based format

		Args:
			Arg2 (list(str)): A list of xpaths each of which is a starting point in the configuration. The only supported xpath notation is by index or descendant-or-self:*. To export the entire configuration specify /descendant-or-self:*
			Arg3 (bool): True to include attributes that are equal to the default in the export, false to exclude them
			Arg4 (str(json)): The format of the exported configuration
			Arg5 (obj(ixnetwork_restpy.files.Files)): The file object to write the configuration to

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		self._check_arg_type(Arg5, Files)
		return self._execute('exportConfigFile', payload=locals(), response_object=None)

	def ImportConfig(self, Arg2, Arg3):
		"""Executes the importConfig operation on the server.

		Create or update the test tool configuration

		Args:
			Arg2 (str): The configuration as a string
			Arg3 (bool): True to create a new configuration, false to update the current configuration

		Returns:
			list(str): A list of errors that occurred during import

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('importConfig', payload=locals(), response_object=None)

	def ImportConfigFile(self, Arg2, Arg3):
		"""Executes the importConfigFile operation on the server.

		Create or update the test tool configuration

		Args:
			Arg2 (obj(ixnetwork_restpy.files.Files)): The file object to read the configuration from
			Arg3 (bool): True to create a new configuration, false to update the current configuration

		Returns:
			list(str): A list of errors that occurred during import

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		self._check_arg_type(Arg2, Files)
		return self._execute('importConfigFile', payload=locals(), response_object=None)
