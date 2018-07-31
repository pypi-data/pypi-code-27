from ixnetwork_restpy.base import Base
from ixnetwork_restpy.errors import IxNetworkError


class Sessions(Base):
	"""Access the /sessions hierarchy.
	
	Provides the following functionality:
		get /sessions instances
		get/set properties on /sessions instances
		execute methods on /sessions instances
		get /sessions child nodes.

	Example:
		TestPlatform('localhost').add_Sessions()
	"""
	_SDM_NAME = 'sessions'
	
	def __init__(self, parent):
		"""The current session"""
		super(Sessions, self).__init__(parent)
	
	@property
	def Ixnetwork(self):
		"""The root object of the configuration hierarchy
		
		Returns: 
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.ixnetwork.Ixnetwork)
		
		Raises:
			ServerError:
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.ixnetwork import Ixnetwork
		return self._read(Ixnetwork(self), None)
	
	@property
	def State(self):
		"""The state of the session

		Returns:
			str
		"""
		return self._properties['state'].upper()
	
	@property
	def ApplicationType(self):
		"""The application type of the session

		Returns:
			str
		"""
		return self._properties['applicationType']
	
	@property
	def Id(self):
		"""The id of the session

		Returns:
			str
		"""
		return self._properties['id']
	
	@property
	def UserId(self):
		"""The user id of the session

		Returns:
			str
		"""
		return self._properties['userId']
	
	@property
	def UserName(self):
		"""The user name of the session

		Returns:
			str
		"""
		return self._properties['userName']

	def Start(self):
		"""Starts the session

		Returns:
			None
		"""
		if self.State == 'INITIAL':
			self._execute('start', {'applicationType': self.ApplicationType})
		
	def Stop(self):
		"""Stops the session

		Returns:
			None
		"""
		try:
			self._execute('stop?deleteAfterStop=true', None)
		except IxNetworkError as e:
			if e._status_code not in [404, 405]:
				raise e

