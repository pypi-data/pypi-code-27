from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AppErrors(Base):
	"""This node holds application errors.
	"""

	_SDM_NAME = 'appErrors'

	def __init__(self, parent):
		super(AppErrors, self).__init__(parent)

	def Error(self, Description=None, LastModified=None, Name=None, Provider=None):
		"""Gets child instances of Error from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Error will be returned.

		Args:
			Description (str): The description of the error
			LastModified (str): 
			Name (str): The name of the error
			Provider (str): The error provider of the error

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.error.error.Error))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.apperrors.error.error import Error
		return self._select(Error(self), locals())

	@property
	def ErrorCount(self):
		"""Total number of errors

		Returns:
			number
		"""
		return self._get_attribute('errorCount')

	@property
	def LastModified(self):
		"""Time of latest logged error or warning

		Returns:
			str
		"""
		return self._get_attribute('lastModified')

	@property
	def WarningCount(self):
		"""Total number of warnings

		Returns:
			number
		"""
		return self._get_attribute('warningCount')
