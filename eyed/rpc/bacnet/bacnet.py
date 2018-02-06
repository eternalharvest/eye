#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# BACnet Driver
#
from eyed.driver.bacnet import BACnetClient
from eyed.driver.bacnet import definition

#
# BACnet Daemon Instance
#
from eyed.single import SingleBACnetd

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
		single = SingleBACnetd.getInstance()
		app = single.bacnetd.application
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
		single = SingleBACnetd.getInstance()
		app = single.bacnetd.application
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
		single = SingleBACnetd.getInstance()
		app = single.bacnetd.application
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
# Entry Point
#
if __name__ == '__main__':
	obj = definition.findObjectByName('device')
	prs = definition.getPropertiesByObject(obj)

	print obj
	print prs
	pass

