#!/usr/bin/python

import threading
from Queue import Queue
from logger import Logger
import postfile
import json
import time

class FileSender(threading.Thread):
	def __init__(self, paras, name):
		super(FileSender, self).__init__()
		self.logger = paras[0]
		self.fsQueue = paras[1]
		self.fsLock = paras[2]
		self.sfQueue = paras[3]
		self.sfLock = paras[4]
		self.host = paras[5]
		self.url = paras[6]
		self.apiKey = paras[7]
		self.interval = paras[8]
		self.name = name

	def run(self):
		self.logger.logger('FileSender Started')

		while True:
			tmp = self.sfQueue.get(1)
			items = tmp.split(',', 1)
			hashValue = items[0]
			fileName = items[1]
			
			fields = [('apikey', self.apiKey)]

			fileData = open(fileName, 'rb').read()
			files = [('file', 'sample.apk', fileData)]

			self.logger.logger('Sending File %s to Scan' % fileName)
			response = postfile.post_multipart(self.host, self.url, fields, files)
			result = json.loads(response)
			if result['response_code'] == 0 or result['response_code'] == -1:
				self.logger.logger('Operation ERROR')
				self.sfLock.acquire()
				self.sfQueue.put(tmp, 1)
				self.sfLock.release()

			if result['response_code'] == 1:
				self.logger.logger('Operation OK')
				self.fsLock.acquire()
				self.fsQueue.put(tmp, 1)
				self.fsLock.release()

			time.sleep(self.interval)
