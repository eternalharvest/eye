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
		bacnet = self.root.BACnetService()
		return bacnet.doReadPropertyRequest(device_id, object_id, instance_id, property_id)

	#
	# scan
	#
	def scan(self):
		#
		# WhoIsRequest の 実行
		#
		bacnet = self.root.BACnetService()
		return bacnet.doWhoIsRequest()

	#
	# getDevices
	#
	def getDevices(self):
		#
		# デバイス一覧の取得
		#
		bacnet = self.root.BACnetService()
		return bacnet.getDevices()

	#
	# getObjectList
	#
	def getObjectList(self, device_id):
		#
		# オブジェクトID, プロパティID の 取得
		#
		obj = definition.findObjectByName('device')
		prs = definition.findPropertyByName('objectList')

		#
		# リクエスト の 実行
		#
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
		#
		# デバイスオブジェクトの全プロパティ取得
		#
		obj = definition.findObjectByName('device')
		prs = definition.getPropertiesByObject(obj)

		#
		# 各プロパティに対してリクエストの実行
		#
		values = dict()
		for p in prs:
			#
			# リクエスト実行
			#
			result = self.doReadPropertyRequest(
				device_id,
				obj['id'],
				device_id,
				p['id']
			)

			#
			# 実行結果を辞書に登録
			#
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

