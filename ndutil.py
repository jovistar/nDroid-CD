#!/usr/bin/python

import hashlib
import os
from datetime import *
import time

def getUid(path):
	return getMd5(path)

def getMd5(path):
	m = hashlib.md5()
	fileHandle = open(path, 'rb')
	m.update(fileHandle.read())
	value = m.hexdigest()
	fileHandle.close()

	return value

def getSize(path):
	return os.path.getsize(path)

def setTimezone():
	os.environ['TZ'] = 'Asia/Shanghai'
	time.tzset()

def getCreated():
	curTime = datetime.now()
	return curTime.strftime('%Y-%m-%d %H:%M:%S')

def getAbstractPath(path):
	return os.path.abspath(path)

def enableDir(path):
	if not os.path.exists(path):
		os.makedirs(path)
