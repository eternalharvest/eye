#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
from bacpypes.apdu import WhoIsRequest, IAmRequest
from bacpypes.app import BIPSimpleApplication
from Queue import Queue
import sys

class App(BIPSimpleApplication):
	def __init__(self, *args):
		BIPSimpleApplication.__init__(self, *args)
		self.device_map = {}

		#
		# IAmRequest を 受けたデバイスIDを管理するキュー
		#
		self.iamr_responses = Queue()

	#
	# デバイスマップ、レスポンスキューのクリア
	#
	def clear(self):
		self.device_map = {}
		self.iamr_responses = Queue()

	def request(self, apdu):
		BIPSimpleApplication.request(self, apdu)

	def confirmation(self, apdu):
		print 'confirmation'
		#print apdu.__dict__
		BIPSimpleApplication.confirmation(self, apdu)

	def indication(self, apdu):
		#
		# IAmRequest の 解析
		#
		if isinstance(apdu, IAmRequest):
			#
			# デバイスID, IPアドレスの取得
			#
			ipaddr = apdu.pduSource
			device_type, device_instance = apdu.iAmDeviceIdentifier

			#
			# デバイスID と IPアドレスのマッピング管理
			#
			self.device_map[device_instance] = ipaddr

			#
			# IAmRequest を 取得したことを通知する
			#
			self.iamr_responses.put(device_instance)

		#
		# forward it along
		#
		BIPSimpleApplication.indication(self, apdu)
