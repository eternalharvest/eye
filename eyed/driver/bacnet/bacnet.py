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
	def __init__(self, application):
		#
		# アプリケーションの取得
		#
		self.application = application

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
		self.application.clear()

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
# BACnet を 簡単に使用可能とするクライアント
#
class BACnetSimpleClient(BACnetClient):
	#
	# コンストラクタ
	#
	def __init__(self, *args):
		BACnetClient.__init__(self, *args)
		self.WhoIsRequest()

	#
	# デバイスからプロパティの取得
	#
	def getDeviceProperty(self, name, device_id):
		propertyIdentifierDict = {
			#'vendor-name'				: 121,
			'vendor-name'				: 'vendorName',
			'vendor-identifier'			: 120,
			'model-name'				: 70,
			'firmware-revision'			: 44,
			'application-software-version'		: 12,
			'protocol-version'			: 98,
			'protocol-revision'			: 139,
			'protocol-services-supported'		: 97,
			'protocol-object-types-supported'	: 96,
			'object_list'				: 76,
		}
		pid = propertyIdentifierDict[name]
		return BACnetClient._ReadDevicePropertyRequest(self, device_id, pid)

