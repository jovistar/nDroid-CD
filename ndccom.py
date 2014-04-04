#!/usr/bin/python

import socket
import json
import os

class NdcCom():
	def __init__(self, host, port):
		self.address = (host, port)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def scan(self, path):
		data = {}
		data['request'] = 'scan'
		
		if not os.path.isfile(path):
			return 1, ()
		data['path'] = os.path.abspath(path)

		result = self.doCom(data)
		if result['response'] == 1:
			return 1, ()
		if result['response'] == 2:
			return 2, ()
		if result['response'] == 0:
			return 0, (result['hashval'], result['positive'], result['total'])

	def doCom(self, data):
		msg = json.dumps(data)
		self.s.sendto(msg, self.address)
		result,addr = self.s.recvfrom(4096)

		return json.loads(result)
