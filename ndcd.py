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
	watchDir = cf.get('conf', 'watchDir')
	workingDir = cf.get('conf', 'workingDir')

	if not os.path.exists(watchDir):
		os.mkdir(watchDir)
	if not os.path.exists(workingDir):
		os.mkdir(workingDir)

	fsQueue = Queue()
	fsLock = threading.Lock()
	sfQueue = Queue()
	sfLock = threading.Lock()

	logger.logger('Starting Threads')
	fileSender = FileSender([logger, fsQueue, fsLock, sfQueue, sfLock, host, fileUrl, apiKey, interval, workingDir], 'FileSender')
	scanSender = ScanSender([logger, fsQueue, fsLock, sfQueue, sfLock, host, scanUrl, apiKey, interval, workingDir], 'ScanSender')

	fileSender.start()
	scanSender.start()

	while True:
		logger.logger('Walking DIR:%s' % watchDir)
		watchDirHandle = os.walk(watchDir)
		for root, dirs, files in watchDirHandle:
			for oneFile in files:
				if oneFile[-4:] == '.apk':
					logger.logger('Found File: %s' % oneFile)

					m = hashlib.md5()
					fileHandle = open('%s/%s' % (watchDir, oneFile), 'rb')
					m.update(fileHandle.read())
					hashValue = m.hexdigest()
					fileHandle.close()

					newFile = '%s/%s' % (workingDir, oneFile)
					oldFile = '%s/%s' % (watchDir, oneFile)
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
