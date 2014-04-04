#!/usr/bin/python

import json
import threading
from Queue import Queue
import urllib
import urllib2
from logger import Logger
import time
from dbmanager import DbManager

class ScanSender(threading.Thread):
	def __init__(self, paras, name):
		super(ScanSender, self).__init__()
		self.logger = paras[0]
		self.fsQueue = paras[1]
		self.fsLock = paras[2]
		self.sfQueue = paras[3]
		self.sfLock = paras[4]
		self.host = paras[5]
		self.url = paras[6]
		self.apiKey = paras[7]
		self.interval = paras[8]
		self.dbManager = paras[9]
		self.name = name

	def run(self):
		self.logger.logger('ScanSender Started')

		while True:
			tmp = self.fsQueue.get(1)
			items = tmp.split(',', 1)

			hashValue = items[0]
			paras = {'resource': hashValue, 'apikey': self.apiKey}

			self.logger.logger('Trying to Get Scan Result')
			data = urllib.urlencode(paras)
			request = urllib2.Request(self.url, data)
			response = urllib2.urlopen(request)

			result = json.loads(response.read())

			if result['response_code'] == -1:
				self.logger.logger('Operation ERROR')
				self.fsLock.acquire()
				self.fsQueue.put(tmp, 1)
				self.fsLock.release()
			if result['response_code'] == 0:
				self.logger.logger('Not in the DATASTORE')
				self.sfLock.acquire()
				self.sfQueue.put(tmp, 1)
				self.sfLock.release()
			if result['response_code'] == 1:
				self.logger.logger('Operation OK')
				self.logger.logger('%d / %d : %s is POSITIVE' % (result['positives'], result['total'], hashValue))
				self.dbManager.update(hashValue, '%d/%d' % (result['positives'], result['total']))

			time.sleep(self.interval)

