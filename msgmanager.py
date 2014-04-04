#!/usr/bin/python

import json

class MsgManager():
	def resRequest(self, msg):
		data = json.loads(msg)

		if data['request'] == None:
			return 1, {}

		if data['request'] not in ['scan']:
			return 1, {}

		return 0, data

	def genResponse(self, data):
		return json.dumps(data)
