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
# Database 接続用
#
from eyed.model import BACnetEmulationObject, BACnetEmulationProperty
from eyed.db import createSession

#
# BACnet Daemon Instance
#
from eyed.single import SingleBACnetd

#
# 初期化処理
#
from initialize import addBACnetObject, addBACnetProperty

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
	# オブジェクト の 登録
	#
	def exposed_addObject(self, name, object_id, instance_id):
		#
		# オブジェクト名が既に利用されていないかを確認
		#
		session = createSession()
		obj = session.query(BACnetEmulationObject).filter_by(
			name = name
		).first()
		if not obj == None: return False

		#
		# オブジェクトの登録
		#
		if addBACnetObject(name, object_id, instance_id) == False:
			return False

		#
		# オブジェクトの登録(DB)
		#
		session.add(BACnetEmulationObject(name, object_id, instance_id))
		session.commit()
		return True

	#
	# プロパティの設定
	#
	def exposed_addProperty(self, name, property_id):
		#
		# オブジェクト名が登録されているかを確認
		#
		session = createSession()
		obj = session.query(BACnetEmulationObject).filter_by(name = name).first()
		if obj == None: return False

		#
		# プロパティ名が既に存在していないかを確認
		#
		prop = obj.properties.filter_by(property_id = property_id).first()
		if not prop == None: return False

		#
		# プロパティの登録
		#
		if addBACnetProperty(obj.name, obj.object_id, obj.instance_id, prop.property_id) == False:
			return False

		#
		# プロパティの登録(DB)
		#
		obj.properties.append(BACnetEmulationProperty(property_id))
		session.commit()
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

