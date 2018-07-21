#! /usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import sys
from rpcdb import rpcserver
from threading import Thread
import mysql.connector as mysql
import os
import subprocess

class ServerLogin(QDialog):
	def __init__(self):
		super().__init__()
		dialog = loadUi('../server_login.ui', self)
		dialog.show()
		self.btnConnect.clicked.connect(self.onConnect)
		self.btnShutdown.clicked.connect(self.onShutdown)
		self.setFixedSize(400, 380)
		self.setWindowIcon(QIcon('../comp.ico'))
		dialog.closeEvent = self.onShutdown

	def onConnect(self, event):		
		user = self.user.text()
		password = self.password.text()
		host = self.host.text()
		database = self.database.text()

		server_ip = self.server_ip.text()
		server_port = self.server_port.text()

		if user and host and database and password:
			try:
				try:
					server_port = int(server_port)
				except ValueError:
					raise ValueError("Server Port should be an integer")
				else:
					mysql.connect(user=user, password=password, database=database, 
						host=host)
			except Exception as e:
				QMessageBox.about(self, "Connection Error", str(e))
				return False
			else:
				QMessageBox.about(self, "Success", "Connected to mysql server")

			rpcserver.connect(user=user, password=password, 
				database=database, host=host)

			if server_ip and server_port:
				t = Thread(target=rpcserver.serve_forver,
					args=(server_ip, server_port))
			elif server_port and not server_ip:
				t = Thread(target=rpcserver.serve_forver,
					args=("", server_port))
			else:
				t = Thread(target=rpcserver.serve_forver)

			t.daemon = True
			t.start()

			self.btnConnect.setEnabled(False)
			self.user.setEnabled(False)
			self.password.setEnabled(False)
			self.host.setEnabled(False)
			self.database.setEnabled(False)
			self.server_ip.setEnabled(False)
			self.server_port.setEnabled(False)


	def onShutdown(self, event):
		self.close()
		subprocess.Popen("taskkill /IM rpcd.exe")


def main():
	App = QApplication(sys.argv)
	App.setStyle('Fusion')
	window = ServerLogin()
	window.show()
	sys.exit(App.exec_())

if __name__ == '__main__':
	main()
	
