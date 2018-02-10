#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rpyc
from eyed.driver.bacnet import definition

#
# RPCClient
#
class RPCClient:
	#
	# コンストラクタ
	#
	def __init__(self, host, port = 1413):
		self.connection = rpyc.connect(host, port)
		self.root = self.connection.root

	#
	# NIC の 取得
	#
	def getNetworkInterfaces(self):
		systemd = self.root.SystemService()
		return systemd.getNetworkInterfaces()

#
# BACnetdRPCClient
#
class BACnetdRPCClient(RPCClient):
	#
	# Start
	#
	def start(self, interface, device_id):
		bacnetd = self.root.BACnetdService()
		return bacnetd.start(interface, device_id)

	#
	# getStatus
	#
	def getStatus(self):
		bacnetd = self.root.BACnetdService()
		return bacnetd.getStatus()

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
# BACnetProxydRPCClient
#
class BACnetProxydRPCClient(RPCClient):
	#
	# addObject
	#
	def addObject(self):
		proxy = self.root.BACnetProxydService()
		return proxy.addObject()

#
# BACnetProxyRPCClient
#
class BACnetProxyRPCClient(RPCClient):
	#
	# Start
	#
	def add(self, device_id, object_id, instance_id, property_id):
		proxy = self.root.BACnetProxyService()
		return proxy.add(device_id, object_id, instance_id, property_id)

#
# Entry Point
#
if __name__ == '__main__':
	#client = BACnetRPCClient('10.2.10.29', 1413)
	#print client.scan()
	#client = BACnetdRPCClient('10.2.10.29', 1413)
	#client = BACnetRPCClient('127.0.0.1', 1413)

	client = BACnetProxyRPCClient('127.0.0.1', 1413)
	client.add(1234, 2, 1, 85)

	#client = BACnetdRPCClient('127.0.0.1', 1413)
	#print client.start('en0', 65535)
	#print client.stop()
	#print client.start('enp0s3')

	#
	# BACnet Daemon への 操作
	#
	#bacnetd = client.root.BACnetdService()
	#print bacnetd.start('en0')
	#print bacnetd.stop()
	#print bacnetd.start('en0')

	#bacnetd = client.root.BACnetdService()
	#client = BACnetRPCClient('127.0.0.1', 1413)
	#print client.scan()
	#print client.getDevices()
	#print client.getEpics(1234)

	#
	# Proxy Service
	#
	#client = BACnetProxydRPCClient('127.0.0.1', 1413)
	#print client.addObject()

