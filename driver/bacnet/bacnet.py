#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bacpypes.iocb import IOCB
from bacpypes.pdu import Address, GlobalBroadcast
from bacpypes.apdu import WhoIsRequest
from bacpypes.apdu import ReadPropertyRequest, ReadPropertyACK

class BACnetClient:
	#
	# BACnetClient 初期化処理
	#
	def __init__(self, application):
		self.application = application

	def WhoIsRequest(self):
		request = WhoIsRequest()

		request.pduDestination = GlobalBroadcast()
		request.deviceInstanceRangeLowLimit = 1
		request.deviceInstanceRangeHighLimit = 2000

		iocb = IOCB(request)
		self.application.request_io(iocb)
		iocb.wait()

		apdu = iocb.ioResponse
		print iocb.ioError
		print apdu

	def ReadPropertyRequest(self, address):
		#
		# リクエスト作成
		#
		request = ReadPropertyRequest(
			destination		= Address(address),
			objectIdentifier	= ('analogValue', 2),
			propertyIdentifier	= 75,
		)

		iocb = IOCB(request)
		self.application.request_io(iocb)
		iocb.wait()

		apdu = iocb.ioResponse

