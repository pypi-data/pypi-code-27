from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AppLibProfile(Base):
	"""This object specifies the properties of the particular application traffic profile.
	"""

	_SDM_NAME = 'appLibProfile'

	def __init__(self, parent):
		super(AppLibProfile, self).__init__(parent)

	def AppLibFlow(self, Description=None, FlowId=None, Name=None):
		"""Gets child instances of AppLibFlow from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of AppLibFlow will be returned.

		Args:
			Description (str): Brief description of what the flow does.
			FlowId (str): The identifier of the flow.
			Name (str): the name of the Flow.

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.applibflow.AppLibFlow))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.applibprofile.applibflow.applibflow import AppLibFlow
		return self._select(AppLibFlow(self), locals())

	@property
	def AvailableFlows(self):
		"""(Read only) All available application library flows.

		Returns:
			list(str[])
		"""
		return self._get_attribute('availableFlows')

	@property
	def ConfiguredFlows(self):
		"""Configured application library flows within profile.

		Returns:
			list(str[])
		"""
		return self._get_attribute('configuredFlows')
	@ConfiguredFlows.setter
	def ConfiguredFlows(self, value):
		self._set_attribute('configuredFlows', value)

	@property
	def EnablePerIPStats(self):
		"""Enable Per IP Stats. When true then Per IP statistic drilldown is available.

		Returns:
			bool
		"""
		return self._get_attribute('enablePerIPStats')
	@EnablePerIPStats.setter
	def EnablePerIPStats(self, value):
		self._set_attribute('enablePerIPStats', value)

	@property
	def ObjectiveDistribution(self):
		"""Objective distribution value.

		Returns:
			str(applyFullObjectiveToEachPort|splitObjectiveEvenlyAmongPorts)
		"""
		return self._get_attribute('objectiveDistribution')
	@ObjectiveDistribution.setter
	def ObjectiveDistribution(self, value):
		self._set_attribute('objectiveDistribution', value)

	@property
	def ObjectiveType(self):
		"""The objective type of the test.A Test Objective is the way the user sets the actual rate of the Application Library Traffic transmission.

		Returns:
			str(simulatedUsers|throughputGbps|throughputKbps|throughputMbps)
		"""
		return self._get_attribute('objectiveType')
	@ObjectiveType.setter
	def ObjectiveType(self, value):
		self._set_attribute('objectiveType', value)

	@property
	def ObjectiveValue(self):
		"""The absolute value of either simulated users or throughput in its measure unit.

		Returns:
			number
		"""
		return self._get_attribute('objectiveValue')
	@ObjectiveValue.setter
	def ObjectiveValue(self, value):
		self._set_attribute('objectiveValue', value)

	@property
	def TrafficState(self):
		"""(Read only) A read-only field which indicates the current state of the traffic item.

		Returns:
			str(Configured|Interim|Running|Unconfigured)
		"""
		return self._get_attribute('trafficState')

	def remove(self):
		"""Deletes a child instance of AppLibProfile on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def AddAppLibraryFlow(self, Arg2):
		"""Executes the addAppLibraryFlow operation on the server.

		This exec adds a flow to an application traffic profile.

		Args:
			Arg2 (list(str[])): This object specifies the flow(s) to be added.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('addAppLibraryFlow', payload=locals(), response_object=None)

	def DistributeFlowsEvenly(self):
		"""Executes the distributeFlowsEvenly operation on the server.

		This exec distributes the percentage for each flow evenly.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('distributeFlowsEvenly', payload=locals(), response_object=None)

	def RemoveAppLibraryFlow(self, Arg2):
		"""Executes the removeAppLibraryFlow operation on the server.

		This exec removes a flow from an application traffic profile.

		Args:
			Arg2 (list(str[])): This object specifies the flow(s) to be removed.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('removeAppLibraryFlow', payload=locals(), response_object=None)

	def Start(self):
		"""Executes the start operation on the server.

		This exec starts running the configured application traffic.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		This exec stops the configured application traffic from running.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stop', payload=locals(), response_object=None)
