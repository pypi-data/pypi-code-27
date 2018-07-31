from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Field(Base):
	"""This object specifies the field properties.
	"""

	_SDM_NAME = 'field'

	def __init__(self, parent):
		super(Field, self).__init__(parent)

	@property
	def DisplayName(self):
		"""Refers to the name of the field.

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def FieldValue(self):
		"""Refers to the value displayed in the field.

		Returns:
			str
		"""
		return self._get_attribute('fieldValue')
