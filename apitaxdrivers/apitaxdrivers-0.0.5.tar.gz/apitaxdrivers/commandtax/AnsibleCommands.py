# Application imports
from apitax.drivers.DriverCommands import DriverCommands
from apitax.ah.State import State

# from apitax.drivers.plugins.commandtax.apitaxtests import *

# Openstack Command Driver for handling custom commands when the openstack driver is used
class AnsibleCommands(DriverCommands):

    def getDriverName(self):
        return 'ansible'
        
    def getResponseBody(self):
        return ''

    def handle(self, command):
        State.log(command)
        return self
