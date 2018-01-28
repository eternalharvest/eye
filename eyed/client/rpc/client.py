#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rpyc
from eyed.driver.bacnet import definition

#
# RPCClient
#
class RPCClient:
	def __init__(self, host, port = 1413):
		self.connection = rpyc.connect(host, port)
		self.root = self.connection.root

#
# BACnetdRPCClient
#
class BACnetdRPCClient(RPCClient):
	#
	# Start
	#
	def start(self, interface):
		bacnetd = self.root.BACnetdService()
		return bacnetd.start(interface)

	#
	# Stop
	#
	def stop(self):
		bacnetd = self.root.BACnetdService()
		return bacnetd.stop()

#
# BACnetRPCClient
#
class BACnetRPCClient(RPCClient):
	#
	# doReadPropertyRequest
	#
	def doReadPropertyRequest(self, device_id, object_id, instance_id, property_id):
		bacnet = client.root.BACnetService()
		return bacnet.doReadPropertyRequest(device_id, object_id, instance_id, property_id)

	#
	# scan
	#
	def scan(self):
		bacnet = client.root.BACnetService()
		return bacnet.doWhoIsRequest()

	#
	# getDevices
	#
	def getDevices(self):
		bacnet = self.root.BACnetService()
		return bacnet.getDevices()

	#
	# getObjectList
	#
	def getObjectList(self, device_id):
		obj = definition.findObjectByName('device')
		prs = definition.findPropertyByName('objectList')

		return self.doReadPropertyRequest(
			device_id,
			obj['id'],
			device_id,
			prs['id']
		)

	#
	# getEpics
	#
	def getEpics(self, device_id):
		obj = definition.findObjectByName('device')
		prs = definition.getPropertiesByObject(obj)

		values = dict()
		for p in prs:
			result = self.doReadPropertyRequest(
				device_id,
				obj['id'],
				device_id,
				p['id']
			)
			values[p['name']] = result['value']
		return values

#
# Entry Point
#
if __name__ == '__main__':
	#client = RPCClient('10.2.10.29', 1413)
	#client = BACnetdRPCClient('10.2.10.29', 1413)
	client = BACnetRPCClient('10.2.10.29', 1413)

	#print client.start('enp0s3')
	#print client.stop()
	#print client.start('enp0s3')

	#
	# BACnet Daemon への 操作
	#
	#bacnetd = client.root.BACnetdService()
	#print bacnetd.start('en0')
	#print bacnetd.stop()
	#print bacnetd.start('en0')

	#print client.scan()
	#print client.getDevices()
	#print client.getEpics(1234)
	print client.getObjectList(1234)

