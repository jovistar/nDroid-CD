#!/usr/bin/python

from datetime import *
import time
import os
import threading
import socket

class Logger():
	def __init__(self, port):
		self.address = ('127.0.0.1', port)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		#multithread
		self.lock = threading.Lock()


	def logger(self, msg):
		self.lock.acquire()
		curTime = datetime.now()

		finalMsg = '[MSG] ' + curTime.strftime('%Y-%m-%d %H:%M:%S') + ' nDroid-Storage: %s' % msg

		self.s.sendto(finalMsg, self.address)

		self.lock.release()
