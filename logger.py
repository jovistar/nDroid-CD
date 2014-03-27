#!/usr/bin/python

from datetime import *
import time
import os
import threading

class Logger():
	def __init__(self, logMode):
		LOG_FILE = 'log.log'
		self.logFile = open(LOG_FILE, 'w')

		if logMode in ['LOGONLY', 'LOGPRINT']:
			if logMode == 'LOGONLY':
				self.logPrint = False
			elif logMode == 'LOGPRINT':
				self.logPrint = True
		else:
			self.logPrint = False

		#multithread
		self.lock = threading.Lock()


	def logger(self, msg):
		self.lock.acquire()
		curTime = datetime.now()

		finalMsg = '[MSG] ' + curTime.strftime('%Y-%m-%d %H:%M:%S') + ' nDroid-CD: %s' % msg

		#std
		if self.logPrint:
			print finalMsg

		#log file
		self.logFile.write(finalMsg + '\n')
		self.lock.release()
