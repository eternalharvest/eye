#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Database Session
#
from eyed.model import ProxyPoint
from eyed.db import createSession

from eyed.single import SingleProxyd
from eyed.single import SingleBACnetd

from eyed.driver.bacnet import BACnetClient
from eyed.driver.bacnet.proxy import ProxyAnalogValueObject
from eyed.driver.bacnet.proxy import ProxyAnalogInputObject

#
# BACnetProxyService
#
class BACnetProxyService(object):
	#
	# Proxy サービス 起動
	#
	def exposed_start(self, host, interval):
		#
		# デーモン起動
		#
		single = SingleProxyd.getInstance()
		result = single.start(host, interval)

		#
		# デーモンの起動に成功したかを確認
		#
		if result == True:
			#
			# 登録済み ポイント を追加
			#
			session = createSession()
			points = session.query(ProxyPoint).all()
			for point in points:
				self.registerPoint(
					point.des_device_id,
					point.des_object_id,
					point.des_instance_id,
					point.des_property_id
				)

			#
			# DB 接続の切断
			#
			session.close()

		#
		# 結果の返却
		#
		return result

	#
	# Proxy ポイント の 登録
	#
	def exposed_add(self, device_id, object_id, instance_id, property_id):
		#
		# 既に登録が行われている監視ポイントであるかを確認する
		#
		session = createSession()
		point = session.query(ProxyPoint).filter_by(
			des_device_id = device_id,
			des_object_id = object_id,
			des_instance_id = instance_id,
			des_property_id = property_id
		).first()

		#
		# 監視ポイントが既に登録されているか確認
		#
		if not point == None:
			return False

		#
		# プロキシポイントの定義
		#
		point = ProxyPoint(
			device_id,
			object_id,
			instance_id,
			property_id,
			65535,
			object_id,
			instance_id,
			property_id
		)
		session.add(point)
		session.commit()
		session.close()

	#
	# プロキシをサポートするオブジェクトを返す
	#
	def getSupportedObject(self, objectType):
		#
		# プロキシ用オブジェクト辞書の作成
		#
		proxyObjects = {
			'analogValue'	: ProxyAnalogValueObject,
			'analogInput'	: ProxyAnalogInputObject,
		}

		#
		# プロキシ可能なオブジェクトかどうかを確認
		#
		if objectType in proxyObjects:
			return proxyObjects[objectType]
		return None

	#
	# ポイントの登録
	#
	def registerPoint(self, device_id, object_id, instance_id, property_id):
		#
		# BACnet コマンド操作用インスタンス取得
		#
		app = SingleBACnetd.getApplication()

		#
		# BACnet クライアント の 取得
		#
		bacnet = BACnetClient(app)

		#
		# objectName の 取得
		#
		objectName = bacnet.ReadPropertyRequest(
			device_id,
			object_id,
			instance_id,
			77
		)

		#
		# objectType の 取得
		#
		objectType = bacnet.ReadPropertyRequest(
			device_id,
			object_id,
			instance_id,
			79
		)

		#
		# objectName or objectType が取得できない場合は終了
		#
		if objectName == None or objectType == False:
			return False

		#
		# プロキシオブジェクトの取得
		#
		ProxyObject = self.getSupportedObject(objectType)
		if not ProxyObject == None:
			#
			# オブジェクトの登録
			#
			return bacnet.addObject(ProxyObject(
				objectName		= objectName,
				objectIdentifier	= (objectType, instance_id),
			))
		return False

