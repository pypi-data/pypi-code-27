from ixnetwork_restpy.connection import Connection
from ixnetwork_restpy.base import Base


class TestPlatform(Base):
	"""Top level access to an IxNetwork test tool platform (Linux API Server, Windows GUI, ConnectionManager)
	"""
	_SDM_NAME = None

	def __init__(self, ip_address, rest_port=443, insecure=False):
		super(TestPlatform, self).__init__(None)
		self._connection = Connection(ip_address, rest_port, insecure)
		self._set_default_href()

	def _set_default_href(self):
		self._properties['href'] = '/api/v1'

	def Authenticate(self, uid, pwd):
		"""Set the X-Api-Key by authenticating against the connected TestPlatform
		
		Args:
			uid (str): The userid to be authenticated
			pwd (str): The password to be authenticated

		Raises:
			UnauthorizedError: Access is unauthorized
			ServerError: The server has encountered an uncategorized error condition

		Example:
			test_platform = TestPlatform('127.0.0.1')
			test_platform.Authenticate('admin', 'admin')
		 """
		self._properties['href'] = '/api/v1/auth/session'
		response = self._execute(None, {'username': uid, 'password': pwd})
		self.ApiKey = response['apiKey']
		self._set_default_href()

	@property
	def Trace(self):
		"""Trace http transactions to console
		
		Returns:
			bool
		"""
		return self._connection.trace
	@Trace.setter
	def Trace(self, trace):
		self._connection.trace = trace

	@property
	def ApiKey(self):
		"""Set the X-Api-Key for authorizing transactions instead of using the authenticate method
		
		Returns:
			bool
		"""
		return self._connection.x_api_key
	@ApiKey.setter
	def ApiKey(self, value):
		self._connection.x_api_key = value

	def add_Sessions(self):
		"""Add a new IxNetwork test tool session on the connected TestPlatform
		
		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.sessions.Sessions): A new Sessions object
		
		Raises:
			UnauthorizedError: Access is unauthorized
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.sessions import Sessions
		applicationType = 'ixnrest'
		session = self._create(Sessions(self), locals())
		session.Start()
		return session

	def Sessions(self):
		"""Get a list of test tool sessions on the connected TestPlatform

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.sessions.Sessions)): A list of Sessions objects

		Raises:
			UnauthorizedError: Access is unauthorized
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.sessions import Sessions
		return self._read(Sessions(self), None)
