from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Error(Base):
	"""This node is a specific application error instance
	"""

	_SDM_NAME = 'error'

	def __init__(self, parent):
		super(Error, self).__init__(parent)

	def Instance(self):
		"""Gets child instances of Instance from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Instance will be returned.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.error.instance.instance.Instance))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.error.instance.instance import Instance
		return self._select(Instance(self), locals())

	@property
	def Description(self):
		"""The description of the error

		Returns:
			str
		"""
		return self._get_attribute('description')

	@property
	def ErrorCode(self):
		"""The error code of the error

		Returns:
			number
		"""
		return self._get_attribute('errorCode')

	@property
	def ErrorLevel(self):
		"""The error level of the error

		Returns:
			str(kAnalysis|kCount|kError|kMessage|kWarning)
		"""
		return self._get_attribute('errorLevel')

	@property
	def InstanceCount(self):
		"""The number of instances of the error

		Returns:
			number
		"""
		return self._get_attribute('instanceCount')

	@property
	def LastModified(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('lastModified')

	@property
	def Name(self):
		"""The name of the error

		Returns:
			str
		"""
		return self._get_attribute('name')

	@property
	def Provider(self):
		"""The error provider of the error

		Returns:
			str
		"""
		return self._get_attribute('provider')

	@property
	def SourceColumns(self):
		"""If the error content originated from an xml meta file, these are the source column names if any for this error.

		Returns:
			list(str)
		"""
		return self._get_attribute('sourceColumns')

	@property
	def SourceColumnsDisplayName(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('sourceColumnsDisplayName')
