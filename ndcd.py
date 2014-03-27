#!/usr/bin/python

import shutil
import os
import time
import hashlib
import threading
from Queue import Queue
import ConfigParser

from filesender import FileSender
from scansender import ScanSender
from logger import Logger

def ndcd_loop():
	os.environ['TZ'] = 'Asia/Shanghai'
	time.tzset()

	if not os.path.exists('watch'):
		os.mkdir('watch')
	if not os.path.exists('working'):
		os.mkdir('working')

	logger = Logger('LOGPRINT')
	logger.logger('Initiating')

	logger.logger('Loading Config')
	cf = ConfigParser.ConfigParser()
	cf.read('ndcd.cnf')

	host = cf.get('conf', 'host')
	fileUrl = cf.get('conf', 'fileUrl')
	scanUrl = cf.get('conf', 'scanUrl')
	apiKey = cf.get('conf', 'apiKey')
	interval = float(cf.get('conf', 'interval'))

	fsQueue = Queue()
	fsLock = threading.Lock()
	sfQueue = Queue()
	sfLock = threading.Lock()

	logger.logger('Starting Threads')
	fileSender = FileSender([logger, fsQueue, fsLock, sfQueue, sfLock, host, fileUrl, apiKey, interval], 'FileSender')
	scanSender = ScanSender([logger, fsQueue, fsLock, sfQueue, sfLock, host, scanUrl, apiKey, interval], 'ScanSender')

	fileSender.start()
	scanSender.start()

	while True:
		logger.logger('Walking DIR:watch')
		watchDir = os.walk('watch')
		for root, dirs, files in watchDir:
			for oneFile in files:
				if oneFile[-4:] == '.apk':
					logger.logger('Found File: %s' % oneFile)

					m = hashlib.md5()
					fileHandle = open('watch/%s' % oneFile, 'rb')
					m.update(fileHandle.read())
					hashValue = m.hexdigest()
					fileHandle.close()

					newFile = 'working/%s' % oneFile
					oldFile = 'watch/%s' % oneFile
					#newFile = oldFile

					shutil.move(oldFile, newFile)
					fsLock.acquire()
					fsQueue.put('%s,%s' % (hashValue, oneFile), 1)
					fsLock.release()

		time.sleep(interval)


	scanSender.join()
	fileSender.join()


if __name__ == '__main__':
	ndcd_loop()
