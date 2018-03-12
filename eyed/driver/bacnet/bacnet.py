#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.iocb import IOCB
from bacpypes.pdu import Address, GlobalBroadcast
from bacpypes.apdu import WhoIsRequest, ReadPropertyRequest, ReadPropertyACK
from bacpypes.object import get_object_class, get_datatype
from bacpypes.object import ObjectType, registered_object_types
from bacpypes.basetypes import PropertyIdentifier

#
# BACnet Client
#
class BACnetClient:
	#
	# BACnetClient 初期化処理
	#
	def __init__(self, application, auto_device_discovery = True):
		#
		# アプリケーションの取得
		#
		self.application = application

		#
		# デバイス の 探索を自動で実行するか？
		#
		self.auto_device_discovery = auto_device_discovery

	#
	# getAddressByDeviceID
	#
	def getAddressByDeviceID(self, device_id):
		#
		# デバイスマップの返却
		#
		if device_id in self.application.device_map:
			return self.application.device_map[device_id]
		return None

	#
	# WhoIsRequest
	#
	def WhoIsRequest(self, low_limit = 1, high_limit = 2000):
		#
		# WhoIsRequest の レスポンス(IAmRequest) を保存するキューをクリア
		#
		#self.application.clear()

		#
		# WhoIsRequest の 送信
		#
		self.application.who_is(low_limit, high_limit, GlobalBroadcast())

	#
	# ReadProperty
	#
	def _ReadPropertyRequest(self, device_id, objectIdentifier, propertyIdentifier):
		#
		# デバイスID から IPの取得
		#
		address = self.getAddressByDeviceID(device_id)
		if not address:
			#
			# デバイスの探索オプションの確認
			#
			if self.auto_device_discovery == False:
				return None

			#
			# デバイスの探索
			#
			self.WhoIsRequest()

		#
		# リクエスト作成
		#
		request = ReadPropertyRequest(
			destination		= address,
			objectIdentifier	= objectIdentifier,
			propertyIdentifier	= propertyIdentifier,
		)

		#
		# リクエストを送信 & 結果取得待ち
		#
		iocb = IOCB(request)
		self.application.request_io(iocb)
		iocb.wait()

		#
		# エラーがあるかを確認
		#
		if iocb.ioError:
			return None

		#
		# レスポンスの確認
		#
		elif iocb.ioResponse:
			#
			# レスポンスデータの取得
			#
			apdu = iocb.ioResponse

			#
			# ACKであるかの確認
			#
			if not isinstance(apdu, ReadPropertyACK):
				print 'ACK is not contain...'
				return None

			#
			# データタイプの取得
			#
			datatype = get_datatype(apdu.objectIdentifier[0], apdu.propertyIdentifier)
			if not datatype:
				print 'Unknown datatype...'
				return None

			#
			# データ種別と値の取得
			#
			return apdu, datatype

		#
		# 例外
		#
		else:
			print 'Response seems something wrong...'
			return None

	#
	# ReadProperty
	#
	def ReadPropertyRequest(self, device_id, object_id, instance_id, property_id):
		#
		# リクエストの作成
		#
		result = BACnetClient._ReadPropertyRequest(
			self,
			device_id		= device_id,
			objectIdentifier	= (object_id, instance_id),
			propertyIdentifier	= property_id
		)

		#
		# レスポンスの確認
		#
		if result == None:
			return None

		#
		# キャスト
		#
		apdu, datatype = result
		return apdu.propertyValue.cast_out(datatype)

	#
	# ReadDeviceProperty (デバイス関連の情報読み出し)
	#
	def _ReadDevicePropertyRequest(self, device_id, propertyIdentifier):
		#
		# リクエストの作成
		#
		result = BACnetClient._ReadPropertyRequest(
			self,
			device_id		= device_id,
			objectIdentifier	= ('device', device_id),
			propertyIdentifier	= propertyIdentifier
		)

		#
		# レスポンスの確認
		#
		if result == None:
			return None

		#
		# キャスト
		#
		apdu, datatype = result
		return apdu.propertyValue.cast_out(datatype)

	#
	# addObject (オブジェクト の 登録)
	#
	def addObject(self, obj):
		return self.application.add_object(obj)

	#
	# getObjectByID (オブジェクト の 取得)
	#
	def getObjectByID(self, objectIdentifier, instance_id):
		return self.application.get_object_id((objectIdentifier, instance_id))

