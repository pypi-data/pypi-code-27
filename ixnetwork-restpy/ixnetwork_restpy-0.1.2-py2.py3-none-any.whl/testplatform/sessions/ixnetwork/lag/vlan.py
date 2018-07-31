from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Vlan(Base):
	"""VLAN
	"""

	_SDM_NAME = 'vlan'

	def __init__(self, parent):
		super(Vlan, self).__init__(parent)

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
	def Priority(self):
		"""3-bit user priority field in the VLAN tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('priority')

	@property
	def Tpid(self):
		"""16-bit Tag Protocol Identifier (TPID) or EtherType in the VLAN tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tpid')

	@property
	def VlanId(self):
		"""12-bit VLAN ID in the VLAN tag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('vlanId')
