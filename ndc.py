#!/usr/bin/python

import shutil
import os
import time
import threading
from Queue import Queue

from twisted.internet import reactor
from filesender import FileSender
from scansender import ScanSender
from logger import Logger
from dbmanager import DbManager
from netmanager import NetManager
from cnfmanager import CnfManager
import ndutil

def ndc_loop():
	ndutil.setTimezone()

	logger = Logger('nDroid-CD', '127.0.0.1', 12322)
	logger.logger('Initiating')

	logger.logger('Loading Config')
	cnfManager = CnfManager()
	cnfManager.load('./ndc.cnf')
	cnfData = cnfManager.getCnfData()

	fsQueue = Queue()
	fsLock = threading.Lock()
	sfQueue = Queue()
	sfLock = threading.Lock()

	logger.logger('Connecting to DB')
	dbManager = DbManager(cnfData['dbHost'], cnfData['dbUser'], cnfData['dbPass'], cnfData['dbName'])
	dbManager.create_table()

	netManager = NetManager()
	netManager.setNdlCom(logger)
	netManager.setDbManager(dbManager)
	netManager.setFsQueue(fsQueue, fsLock)

	logger.logger('Starting Threads')
	fileSender = FileSender([logger, fsQueue, fsLock, sfQueue, sfLock, cnfData['host'], cnfData['fileUrl'], cnfData['apiKey'], cnfData['interval']], 'FileSender')
	scanSender = ScanSender([logger, fsQueue, fsLock, sfQueue, sfLock, cnfData['host'], cnfData['scanUrl'], cnfData['apiKey'], cnfData['interval'], dbManager], 'ScanSender')

	fileSender.start()
	scanSender.start()

	reactor.listenUDP(cnfData['comPort'], netManager)
	logger.logger('Listening Com Port')
	reactor.run()

	#scanSender.join()
	#fileSender.join()


if __name__ == '__main__':
	ndc_loop()
