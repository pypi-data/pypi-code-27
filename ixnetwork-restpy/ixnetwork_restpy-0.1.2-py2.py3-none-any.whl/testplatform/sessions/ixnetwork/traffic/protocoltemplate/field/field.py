from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Field(Base):
	"""This object specifies the field properties of the protocol template.
	"""

	_SDM_NAME = 'field'

	def __init__(self, parent):
		super(Field, self).__init__(parent)

	@property
	def __id__(self):
		"""An alphanumeric string that defines the internal field ID.

		Returns:
			str
		"""
		return self._get_attribute('__id__')

	@property
	def DisplayName(self):
		"""It is used to get the name of the particular field as available in the protocol template.

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def FieldTypeId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('fieldTypeId')

	@property
	def Length(self):
		"""It is used to get the length of the field in bits.

		Returns:
			number
		"""
		return self._get_attribute('length')

	@property
	def Trackable(self):
		"""The trackable fields.

		Returns:
			bool
		"""
		return self._get_attribute('trackable')
