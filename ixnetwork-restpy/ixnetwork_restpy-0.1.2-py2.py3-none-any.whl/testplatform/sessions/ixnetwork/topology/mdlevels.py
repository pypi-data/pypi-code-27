from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MdLevels(Base):
	"""
	"""

	_SDM_NAME = 'mdLevels'

	def __init__(self, parent):
		super(MdLevels, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def BridgeId(self):
		"""Bridge ID

		Returns:
			list(str)
		"""
		return self._get_attribute('bridgeId')

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
	def MdMegLevel(self):
		"""MD/MEG Level

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mdMegLevel')

	@property
	def MdName(self):
		"""MD Name For MAC + Int, Please Use MAC-Int eg. 11:22:33:44:55:66-1 For Others, Use Any String

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mdName')

	@property
	def MdNameFormat(self):
		"""MD Name Format

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mdNameFormat')

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
	def NumberOfMdLevels(self):
		"""Number of MD Levels

		Returns:
			number
		"""
		return self._get_attribute('numberOfMdLevels')
	@NumberOfMdLevels.setter
	def NumberOfMdLevels(self, value):
		self._set_attribute('numberOfMdLevels', value)

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
