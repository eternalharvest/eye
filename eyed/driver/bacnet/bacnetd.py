#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
from bacpypes.pdu import Address
from bacpypes.app import BIPSimpleApplication
from bacpypes.service.device import LocalDeviceObject
from bacpypes import core
from app import App

#
# BACnet Server
#
class BACnetd(Thread):
	#
	# BACnet 初期化処理
	#
	def __init__(self, address):
		#
		# 親コンストラクタの呼び出し
		#
		Thread.__init__(self)

		#
		# デーモンの設定
		#
		self.daemon = True

		#
		# デバイスの設定情報の定義
		#
		self.device_name		= 'naoya@tuntunkun.com'
		self.device_id			= 65535
		self.vendor_name		= 'EYED'
		self.vendor_id			= 65535
		self.maxApduLengthAccepted	= 1024
		self.segmentationSupported	= 'segmentedBoth'

		#
		# デバイスの定義
		#
		self.device = LocalDeviceObject(
			objectName		= self.device_name,
			objectIdentifier	= ('device', self.device_id),
			maxApduLengthAccepted	= self.maxApduLengthAccepted,
			segmentationSupported	= self.segmentationSupported,
			vendorName		= self.vendor_name,
			vendorIdentifier	= self.vendor_id
		)

		#
		# アプリケーションの定義
		#
		#self.application = BIPSimpleApplication(self.device, Address(address))
		self.application = App(self.device, Address(address))

		#
		# サポートしているプロトコルの定義
		#
		services_supported = self.application.get_services_supported()
		self.device.protocolServicesSupported = services_supported

	#
	# デーモンの起動
	#
	def run(self):
		#
		# BACnetd の 起動
		#
		core.run()

	#
	# デーモンの停止
	#
	def stop(self):
		#
		# 通信ポート の クローズ
		#
		self.application.mux.directPort.handle_close()
		self.application.mux.broadcastPort.handle_close()

		#
		# BACnetd の 停止
		#
		core.deferred(core.stop)
		return True

