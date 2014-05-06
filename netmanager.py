#!/usr/bin/python

from twisted.internet.protocol import DatagramProtocol
from logger import Logger
from dbmanager import DbManager
from msgmanager import MsgManager
import ndutil
import os
import shutil
from Queue import Queue
import threading

class NetManager(DatagramProtocol):
	def setNdlCom(self, logger):
		self.logger = logger
		self.msgManager = MsgManager()

	def setDbManager(self, dbManager):
		self.dbManager = dbManager

	def setFsQueue(self, fsQueue, fsLock):
		self.fsQueue = fsQueue
		self.fsLock = fsLock

	def datagramReceived(self, data, (host, port)):
		self.logger.logger('Request from %s:%d' % (host, port))
		self.dispatch(data, host, port)

	def dispatch(self, data, host, port):
		retCode, result = self.msgManager.resRequest(data)
		if retCode != 0:
			self.logger.logger('Error Request')
		else:
			responseData = {}
			if result['request'] == 'scan':
				self.logger.logger('Request: SCAN')
				if not os.path.isfile(result['path']):
					responseData['response'] = 1
				else:
					hashval = ndutil.getMd5(result['path'])
					reqTime = ndutil.getCreated()
					fileSize = ndutil.getSize(result['path'])

					if (fileSize/1024/1024) >= 32:
						responseData['response'] = 1
					else:
						scanCode, scanResult = self.dbManager.scan(reqTime, result['path'], hashval)
						if scanCode == 0:
							responseData['response'] = 0
							nums = scanResult.split('/', 1)
							responseData['hashval'] = hashval
							responseData['positive'] = nums[0]
							responseData['total'] = nums[1]
						if scanCode == 1:
							responseData['response'] = 2
						if scanCode == 2:
							responseData['response'] = 2
							self.fsLock.acquire()
							self.fsQueue.put('%s,%s' % (hashval, result['path']), 1)
							self.fsLock.release()

			msg = self.msgManager.genResponse(responseData)
			self.transport.write(msg, (host, port))
