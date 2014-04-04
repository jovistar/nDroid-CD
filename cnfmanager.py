#!/usr/bin/python

import ConfigParser
import os

class CnfManager():
	def load(self, cnfFile):
		if not os.path.isfile(cnfFile):
			cnfFile = './ndc.cnf'

		cf = ConfigParser.ConfigParser()
		cf.read(cnfFile)

		self.cnfData = {}
		self.cnfData['host'] = cf.get('api', 'host')
		self.cnfData['fileUrl'] = cf.get('api', 'fileUrl')
		self.cnfData['scanUrl'] = cf.get('api', 'scanUrl')
		self.cnfData['apiKey'] = cf.get('api', 'apiKey')
		self.cnfData['interval'] = float(cf.get('api', 'interval'))
		self.cnfData['dbHost'] = cf.get('db', 'dbHost')
		self.cnfData['dbUser'] = cf.get('db', 'dbUser')
		self.cnfData['dbPass'] = cf.get('db', 'dbPass')
		self.cnfData['dbName'] = cf.get('db', 'dbName')
		self.cnfData['comPort'] = int(cf.get('com', 'comPort'))

	def getCnfData(self):
		return self.cnfData
