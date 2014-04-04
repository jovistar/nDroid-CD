#!/usr/bin/python

import MySQLdb

class DbManager():
	def __init__(self, dbHost, dbUser, dbPass, dbName):
		self.dbCon = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName, charset='utf8')
		self.dbCursor = self.dbCon.cursor()

	def create_table(self):
		self.drop_table()
		self.dbCursor.execute('CREATE TABLE cdrec(crid int auto_increment primary key not null,reqtime varchar(128) not null,path varchar(4096) not null,hashval varchar(64) not null)')
		self.dbCursor.execute('CREATE TABLE cd(cid int auto_increment primary key not null,hashval varchar(64) not null,result varchar(32) not null)')
		self.dbCon.commit()

	def drop_table(self):
		self.dbCursor.execute('DROP TABLE IF EXISTS cdrec')
		self.dbCursor.execute('DROP TABLE IF EXISTS cd')
		self.dbCon.commit()

	def update(self, hashval, result):
		value = (hashval, result)
		self.dbCursor.execute('update cd set result=%s where hashval=%s', (result, hashval))
		self.dbCon.commit()

	def scan(self, reqtime, path, hashval):
		value = (0, reqtime, path, hashval)
		self.dbCursor.execute('insert into cdrec values(%s,%s,%s,%s)', value)
		self.dbCon.commit()

		count = self.dbCursor.execute('select result from cd where hashval=%s', hashval)
		if count:
			result = self.dbCursor.fetchone()
			if result[0] == '0/0':
				return 1, ''
			else:
				return 0, result[0]
		else:
			self.dbCursor.execute('insert into cd values(%s,%s,%s)', (0, hashval, '0/0'))
			self.dbCon.commit()
			return 2, ''
