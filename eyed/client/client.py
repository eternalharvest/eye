#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

#
# ベースクラス
#
class Client:
	#
	# URL組立用のベースパスの取得
	#
	def __init__(self, host, port):
		self.base_url = 'http://%s:%s' %(host, port)

#
# ICMPClient
#
class ICMPClient(Client):
	#
	# ICMP
	#
	def ping(self, ip, uuid = ''):
		#
		# URLの組立
		#
		url = '%s/api/icmp/' %(self.base_url)

		#
		# ICMPリクエストの実行
		#
		return requests.post(url, json = {
			'uuid'  : uuid,
			'ip'    : ip,
		}).json()

#
# BACnetClient
#
class BACnetClient(Client):
	#
	# BACnet デバイスのスキャン
	#
	def scanDevices(self, timeout = 3):
		#
		# URLの組立
		#
		url = '%s/api/bacnet/scan/' %(self.base_url)

		#
		# BACnet デバイス取得リクエスト送信
		#
		return requests.post(url, json = {
			'timeout'	: timeout
		})

	#
	# BACnet デバイスの取得
	#
	def getDevices(self):
		#
		# URLの組立
		#
		url = '%s/api/bacnet/devices/' %(self.base_url)

		#
		# BACnet デバイス取得リクエスト送信
		#
		return requests.post(url).json()

	#
	# BACnet デバイスの検索
	#
	def getDevice(self, device_id):
		#
		# URLの組立
		#
		url = '%s/api/bacnet/devices/%s' %(self.base_url, device_id)

		#
		# BACnet デバイス検索リクエストの送信
		#
		return requests.get(url).json()

#
# Entry Point
#
if __name__ == '__main__':
	#client = ICMPClient('localhost', '8888')
	#print client.ping('8.8.8.8')

	#
	# BACnet 通信の実行
	#
	client = BACnetClient('localhost', '8888')
	print client.scanDevices()
	for device in client.getDevices():
		device_id = device['device_id']
		print client.getDevice(device_id)

