from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class IsisBierSubDomainList(Base):
	"""ISIS BIER Sub Domain
	"""

	_SDM_NAME = 'isisBierSubDomainList'

	def __init__(self, parent):
		super(IsisBierSubDomainList, self).__init__(parent)

	def IsisBierBSObjectList(self, DescriptiveName=None, Name=None):
		"""Gets child instances of IsisBierBSObjectList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of IsisBierBSObjectList will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisbierbsobjectlist.IsisBierBSObjectList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.isisbierbsobjectlist import IsisBierBSObjectList
		return self._select(IsisBierBSObjectList(self), locals())

	@property
	def BAR(self):
		"""BIER Algorithm

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BAR')

	@property
	def BFRId(self):
		"""BFR Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('BFRId')

	@property
	def IPA(self):
		"""IGP Algorithm

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('IPA')

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

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
	def NumberOfBSLen(self):
		"""Number of Supported BSL

		Returns:
			number
		"""
		return self._get_attribute('numberOfBSLen')
	@NumberOfBSLen.setter
	def NumberOfBSLen(self, value):
		self._set_attribute('numberOfBSLen', value)

	@property
	def SubDomainId(self):
		"""Sub Domain Id

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('subDomainId')

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
