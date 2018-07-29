import telnetlib
import socket
import requests
import time
from xml.etree import ElementTree
from abc import ABC, abstractmethod

class FNIPOutput:

	def __init__(self, host, port, channel):
	    self._host = host
	    self._port = int(port)
	    self._timeout = 1 # seconds
	    self._channel = int(channel)
	    self._state = None
	    self._updated_time = 0

	@abstractmethod
	def is_on(self):
		status = self.get_status(find)
		return status

	@abstractmethod
	def turn_on(self, state):
		cmd = "FN,ON," + str(self._channel)
		self.send_cmd(cmd)
		self.update_state(1)

	def turn_off(self):
		cmd = "FN,OFF," + str(self._channel)
		self.send_cmd(cmd)
		self.update_state(0)

	def update_state(self, state):
		self._state = state
		self._updated_time = time.time()

	def get_status(self, find):
		if self._updated_time > time.time()-2:
			# Use cached state for 2 seconds
			status = self._state
		else:
			# 2s delay is needed to get state change values ready in status.xml
			response = requests.get("http://" + self._host + "/status.xml")
			tree = ElementTree.fromstring(response.content)
			status = tree.findtext(find, "0")
			self.update_state(status)
		return status

	def send_cmd(self, cmd):
		try:
			tn = telnetlib.Telnet(self._host, self._port, self._timeout)
			tn.write(cmd.encode('ascii') + b"\r\n")
			tn.read_some()
			tn.close()
		except socket.timeout:
			pass

class FNIP8x10aOutput(FNIPOutput):
	def is_on(self):
		find = "led" + str(int(self._channel)-1)
		status = self.get_status(find)
		return status

	def turn_on(self, state):
		cmd = "FN,ON," + str(self._channel)
		self.send_cmd(cmd)
		self.update_state(1)

class FNIP6x2adOutput(FNIPOutput):
	def is_on(self):
		find = "level" + str(self._channel)
		status = self.get_status(find)
		return status

	def turn_on(self, state):
		cmd = "FN,LEV," + str(self._channel) + "," + str(state)
		self.send_cmd(cmd)
		self.update_state(state)
