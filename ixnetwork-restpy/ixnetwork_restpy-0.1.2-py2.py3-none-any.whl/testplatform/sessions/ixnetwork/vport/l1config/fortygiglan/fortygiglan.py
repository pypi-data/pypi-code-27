from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FortyGigLan(Base):
	"""40GE LAN.
	"""

	_SDM_NAME = 'fortyGigLan'

	def __init__(self, parent):
		super(FortyGigLan, self).__init__(parent)

	@property
	def Fcoe(self):
		"""Returns the one and only one Fcoe object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.fortygiglan.fcoe.fcoe.Fcoe)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.fortygiglan.fcoe.fcoe import Fcoe
		return self._read(Fcoe(self), None)

	@property
	def TxLane(self):
		"""Returns the one and only one TxLane object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.fortygiglan.txlane.txlane.TxLane)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.fortygiglan.txlane.txlane import TxLane
		return self._read(TxLane(self), None)

	@property
	def AutoInstrumentation(self):
		"""The auto instrumentation mode.

		Returns:
			str(endOfFrame|floating)
		"""
		return self._get_attribute('autoInstrumentation')
	@AutoInstrumentation.setter
	def AutoInstrumentation(self, value):
		self._set_attribute('autoInstrumentation', value)

	@property
	def EnableLASIMonitoring(self):
		"""If selected, enables LASI monitoring.

		Returns:
			bool
		"""
		return self._get_attribute('enableLASIMonitoring')
	@EnableLASIMonitoring.setter
	def EnableLASIMonitoring(self, value):
		self._set_attribute('enableLASIMonitoring', value)

	@property
	def EnablePPM(self):
		"""If true, enables the portsppm.

		Returns:
			bool
		"""
		return self._get_attribute('enablePPM')
	@EnablePPM.setter
	def EnablePPM(self, value):
		self._set_attribute('enablePPM', value)

	@property
	def EnabledFlowControl(self):
		"""Enables the port's MAC Flow control mechanisms to listen for a directed address pause message.

		Returns:
			bool
		"""
		return self._get_attribute('enabledFlowControl')
	@EnabledFlowControl.setter
	def EnabledFlowControl(self, value):
		self._set_attribute('enabledFlowControl', value)

	@property
	def FlowControlDirectedAddress(self):
		"""This is the 48-bit MAC address that the port will listen on for a directed pause message.

		Returns:
			str
		"""
		return self._get_attribute('flowControlDirectedAddress')
	@FlowControlDirectedAddress.setter
	def FlowControlDirectedAddress(self, value):
		self._set_attribute('flowControlDirectedAddress', value)

	@property
	def Loopback(self):
		"""If enabled, the port is set to internally loopback from transmit to receive.

		Returns:
			bool
		"""
		return self._get_attribute('loopback')
	@Loopback.setter
	def Loopback(self, value):
		self._set_attribute('loopback', value)

	@property
	def Ppm(self):
		"""Indicates the value that needs to be adjusted for the line transmit frequency.

		Returns:
			number
		"""
		return self._get_attribute('ppm')
	@Ppm.setter
	def Ppm(self, value):
		self._set_attribute('ppm', value)

	@property
	def TransmitClocking(self):
		"""Allows to select the transmit clocing options.

		Returns:
			str(external|internal|recovered)
		"""
		return self._get_attribute('transmitClocking')
	@TransmitClocking.setter
	def TransmitClocking(self, value):
		self._set_attribute('transmitClocking', value)

	@property
	def TxIgnoreRxLinkFaults(self):
		"""Tx ignore Rx link fault.

		Returns:
			bool
		"""
		return self._get_attribute('txIgnoreRxLinkFaults')
	@TxIgnoreRxLinkFaults.setter
	def TxIgnoreRxLinkFaults(self, value):
		self._set_attribute('txIgnoreRxLinkFaults', value)
