#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.iocb import IOCB
from bacpypes.pdu import Address, GlobalBroadcast
from bacpypes.apdu import WhoIsRequest
from bacpypes.apdu import ReadPropertyRequest, ReadPropertyACK
from bacpypes.object import get_object_class, get_datatype

class BACnetClient:
	#
	# BACnetClient 初期化処理
	#
	def __init__(self, application):
		self.application = application

	#
	# WhoIsRequest
	#
	def WhoIsRequest(self):
		#
		# WhoIsRequest の レスポンス(IAmRequest) を保存するキューをクリア
		#
		self.application.clear()

		#
		# WhoIsRequest の 送信
		#
		self.application.who_is(1, 2000, GlobalBroadcast())

	#
	# ReadProperty
	#
	def ReadPropertyRequest(self, address):
		#
		# リクエスト作成
		#
		request = ReadPropertyRequest(
			destination		= Address(address),
			objectIdentifier	= ('analogValue', 2),
			propertyIdentifier	= 75,
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
			pass

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
				raise Exception('ACK is not contain...')

			#
			# データタイプの取得
			#
			datatype = get_datatype(apdu.objectIdentifier[0], apdu.propertyIdentifier)
			if not datatype:
				raise TypeError('Unknown datatype...')

			#
			# データ種別と値の取得
			#
			type, value = apdu.propertyValue.cast_out(datatype)
			return {
				'result'	: True,
				'values'	: [{
					'name'	: type,
					'value'	: value
				}],
			}

		#
		# 例外
		#
		else:
			raise Exception('Response seems something wrong...')

