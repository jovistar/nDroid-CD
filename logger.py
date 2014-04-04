#!/usr/bin/python

from datetime import *
import time
import os
import threading
import socket

class Logger():
	def __init__(self, name, host, port):
		self.name = name
		self.address = (host, port)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		#multithread
		self.lock = threading.Lock()


	def logger(self, msg):
		self.lock.acquire()

		finalMsg = '%s : %s' % (self.name, msg)
		self.s.sendto(finalMsg, self.address)

		self.lock.release()
