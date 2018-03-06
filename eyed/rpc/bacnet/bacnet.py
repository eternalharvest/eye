#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.object import AnalogValueObject
from bacpypes.object import AnalogInputObject

#
# BACnet Driver
#
from eyed.driver.bacnet import BACnetClient
from eyed.driver.bacnet import definition

#
# BACnet Daemon Instance
#
from eyed.single import SingleBACnetd

from property import EyedPresentValue

from eyed.driver.bacnet import BACnetClient

#
# BACnetService
#
class BACnetService(object):
	#
	# WhoIsRequest の 実行
	#
	def exposed_doWhoIsRequest(self, timeout = 10):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None:
			raise Exception('BAcnetd is not running...')
		bacnet = BACnetClient(app)

		#
		# WhoIsRequest の 送信
		#
		bacnet.WhoIsRequest()

		#
		# WhoIsRequest を 投げてから最初の IAmRequestを受け取るまで待つ
		#
		try:
			device_id = app.responseQueue.get(timeout = timeout)
			return { 'device_id' : device_id }
		except Exception:
			#
			# タイムアウトを通知
			#
			return None

	#
	# デバイスマップの取得
	#
	def exposed_getDevices(self):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None:
			raise Exception('BAcnetd is not running...')
		bacnet = BACnetClient(app)

		#
		# デバイスリストの作成
		#
		devices = []
		for key, value in app.device_map.items():
			devices.append({ 'device_id' : key, 'ip' : str(value) })

		#
		# デバイスリストを返却
		#
		return devices

	#
	# ReadPropertyRequest の 実行
	#
	def exposed_doReadPropertyRequest(self, device_id, object_id, instance_id, property_id):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()
		if app == None:
			raise Exception('BAcnetd is not woring...')
		bacnet = BACnetClient(app)

		#
		# リクエストの実行
		#
		value = bacnet.ReadPropertyRequest(device_id, object_id, instance_id, property_id)

		#
		# リクエスト結果をJSONで返す
		#
		return { 'value' : value }

	#
	# パラメータの複数読み込みに対応
	#

	#
	# サポートするオブジェクトを返す
	#
	def getSupportedObject(self, objectType):
		#
		# オブジェクト辞書の作成
		#
		supportedObjects = {
			'analogValue'	: AnalogValueObject,
			'analogInput'	: AnalogInputObject,
		}

		#
		# 対応するオブジェクトかどうかを確認
		#
		if objectType in supportedObjects:
			return supportedObjects[objectType]
		return None

	#
	# ポイント の 登録
	#
	def exposed_setPoint(self, object_name, object_id, instance_id, property_id):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()

		#
		# BACnet クライアント の 取得
		#
		bacnet = BACnetClient(app)

		#
		# オブジェクトの取得
		#
		obj = definition.findObjectByID(object_id)
		if obj == None:
			return False

		#
		# サポートするオブジェクトの取得
		#
		objectType = obj['name']
		Object = self.getSupportedObject(objectType)

		#
		# オブジェクトとプロパティの定義
		#
		o = Object(
			objectName		= object_name,
			objectIdentifier	= (objectType, instance_id),
		)
		o.add_property(EyedPresentValue(object_id, instance_id))

		#
		# オブジェクトが既に登録されていないかを確認
		#
		pass

		#
		# オブジェクトの登録
		#
		bacnet.addObject(o)
		return True

#
# Entry Point
#
if __name__ == '__main__':
	obj = definition.findObjectByName('device')
	prs = definition.getPropertiesByObject(obj)

	print obj
	print prs
	pass

