#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

#
# ベースクラス
#
class Client(object):
	#
	# URL組立用のベースパスの取得
	#
	def __init__(self, host, port):
		self.base_url = 'http://%s:%s' %(host, port)

	#
	# NIC の 情報取得
	#
	def getNetworkInterfaces(self):
		#
		# URLの組立
		#
		url = '%s/api/system/network/interfaces' %(self.base_url)

		#
		# BACnet デバイス取得リクエスト送信
		#
		result = requests.get(url)

		#
		# 結果の確認
		#
		if result.status_code == 200:
			return result.json()
		return False

#
# Entry Point
#
if __name__ == '__main__':
	client = Client('127.0.0.1', 8888)
	print client.getNetworkInterfaces()

