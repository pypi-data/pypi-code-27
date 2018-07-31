from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Base64CodeOptions(Base):
	"""Contains the base64 encoding code generation options
	"""

	_SDM_NAME = 'base64CodeOptions'

	def __init__(self, parent):
		super(Base64CodeOptions, self).__init__(parent)

	@property
	def IncludeSampleCode(self):
		"""Flag to include sample code

		Returns:
			bool
		"""
		return self._get_attribute('includeSampleCode')
	@IncludeSampleCode.setter
	def IncludeSampleCode(self, value):
		self._set_attribute('includeSampleCode', value)

	@property
	def SampleObjectReferences(self):
		"""A list of object references used to generate sample code

		Returns:
			list(str[None])
		"""
		return self._get_attribute('sampleObjectReferences')
	@SampleObjectReferences.setter
	def SampleObjectReferences(self, value):
		self._set_attribute('sampleObjectReferences', value)
