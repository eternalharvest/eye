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

#
# BACnetProxyService
#
class BACnetProxyService(object):
	#
	# Proxy サービス 起動
	#
	def exposed_start(self):
		#
		# デーモン起動
		#
		single = SingleProxyd.getInstance()
		result = single.start()

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
			return

		return bacnet.addObject(ProxyAnalogValueObject(
			objectName		= objectName,
			objectIdentifier	= (objectType, instance_id),
		))

