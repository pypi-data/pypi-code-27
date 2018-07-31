from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class RsvpRROSubObjectsList(Base):
	"""Rsvp RRO Sub-Objects
	"""

	_SDM_NAME = 'rsvpRROSubObjectsList'

	def __init__(self, parent):
		super(RsvpRROSubObjectsList, self).__init__(parent)

	@property
	def BandwidthProtection(self):
		"""Bandwidth Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthProtection')

	@property
	def CType(self):
		"""C-Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cType')

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
	def GlobalLabel(self):
		"""Global Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('globalLabel')

	@property
	def Ip(self):
		"""IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ip')

	@property
	def Label(self):
		"""Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('label')

	@property
	def LocalIp(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('localIp')

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
	def NodeProtection(self):
		"""Node Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nodeProtection')

	@property
	def ProtectionAvailable(self):
		"""Protection Available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionAvailable')

	@property
	def ProtectionInUse(self):
		"""Protection In Use

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionInUse')

	@property
	def Type(self):
		"""Reservation Style

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('type')

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


class RsvpRroSubObjectsList(Base):
	"""Rsvp RRO Sub-Objects
	"""

	_SDM_NAME = 'rsvpRroSubObjectsList'

	def __init__(self, parent):
		super(RsvpRroSubObjectsList, self).__init__(parent)

	@property
	def BandwidthProtection(self):
		"""Bandwidth Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthProtection')

	@property
	def CType(self):
		"""C-Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('cType')

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
	def GlobalLabel(self):
		"""Global Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('globalLabel')

	@property
	def Ip(self):
		"""IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ip')

	@property
	def Label(self):
		"""Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('label')

	@property
	def LocalIp(self):
		"""Local IP

		Returns:
			list(str)
		"""
		return self._get_attribute('localIp')

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
	def NodeProtection(self):
		"""Node Protection

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('nodeProtection')

	@property
	def P2mpIdAsIp(self):
		"""P2MP ID As IP

		Returns:
			list(str)
		"""
		return self._get_attribute('p2mpIdAsIp')

	@property
	def P2mpIdAsNum(self):
		"""P2MP ID displayed in Integer format

		Returns:
			list(str)
		"""
		return self._get_attribute('p2mpIdAsNum')

	@property
	def ProtectionAvailable(self):
		"""Protection Available

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionAvailable')

	@property
	def ProtectionInUse(self):
		"""Protection In Use

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionInUse')

	@property
	def Type(self):
		"""Type: Label Or IP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('type')

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
