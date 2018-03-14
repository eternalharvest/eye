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
	# getObjects
	#
	def getObjects(self):
		#
		# オブジェクトの取得
		#
		bacnet = self.root.BACnetService()
		return bacnet.getObjects()

	#
	# addObject
	#
	def addObject(self, name, object_id, instance_id):
		#
		# オブジェクトの登録
		#
		bacnet = self.root.BACnetService()
		return bacnet.addObject(name, object_id, instance_id)

	#
	# setProperty
	#
	def addProperty(self, name, property_id):
		#
		# プロパティの登録
		#
		bacnet = self.root.BACnetService()
		return bacnet.addProperty(name, property_id)

	#
	# setProperty
	#
	def setProperty(self, name, property_id, value):
		#
		# ポイントの登録
		#
		bacnet = self.root.BACnetService()
		return bacnet.setProperty(name, property_id, value)

#
# SchedulerRPCClient
#
class SchedulerRPCClient(RPCClient):
	#
	# addInterval
	#
	def addInterval(self, name, interval):
		service = self.root.SchedulerService()
		return service.addInterval(name, interval)

#
# Entry Point
#
if __name__ == '__main__':
	#
	# ポイントの登録
	#
	#client = BACnetRPCClient('127.0.0.1', 1413)
	client = SchedulerRPCClient('127.0.0.1', 1413)
	client.addInterval('TEST1', 60)
	client.addInterval('TEST2', 30)
	pass

