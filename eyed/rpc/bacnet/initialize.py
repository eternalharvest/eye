#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# BACnet Driver
#
from eyed.driver.bacnet import BACnetClient

#
# Database 接続用
#
from eyed.model import BACnetEmulationObject, BACnetEmulationProperty
from eyed.db import createSession

#
# BACnet Daemon Instance
#
from eyed.single import SingleBACnetd
from property import EyedPresentValue

#
# オブジェクト の 登録
#
def addBACnetObject(name, object_id, instance_id):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = SingleBACnetd.getApplication()

	#
	# BACnet クライアント の 取得
	#
	bacnet = BACnetClient(app)

	#
	# オブジェクトの登録
	#
	if bacnet.addObject(name, object_id, instance_id) == False:
		return False
	return True

#
# プロパティ の 登録
#
def addBACnetProperty(name, object_id, instance_id, property_id):
	#
	# BACnet コマンド操作用インスタンス取得
	#
	app = SingleBACnetd.getApplication()

	#
	# BACnet クライアント の 取得
	#
	bacnet = BACnetClient(app)
	prop = EyedPresentValue(object_id, instance_id)

	#
	# プロパティ の 登録
	#
	if bacnet.addProperty(name, prop) == False:
		return False
	return True

#
# データベースに登録されているポイントの登録
#
def start_bacnet_emulation():
	#
	# ポイント名が既に利用されていないかを確認
	#
	session = createSession()
	objects = session.query(BACnetEmulationObject).all()
	for obj in objects:
		#
		# オブジェクト の 登録
		#
		addBACnetObject(obj.name, obj.object_id, obj.instance_id)
		for prop in obj.properties:
			#
			# プロパティの登録
			#
			addBACnetProperty(obj.name, obj.object_id, obj.instance_id, prop.property_id)

if __name__ == '__main__':
	start_bacnet_emulation()

