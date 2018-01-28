#!/usr/bin/env python
# -*- coding: utf-8 -*-
from client import Client
import requests

#
# ICMPClient
#
class ICMPClient(Client):
	#
	# ICMP
	#
	def ping(self, ip):
		#
		# URLの組立
		#
		url = '%s/api/icmp/' %(self.base_url)

		#
		# ICMPリクエストの実行
		#
		return requests.post(url, json = {
			'ip'    : ip
		}).json()

#
# Entry Point
#
if __name__ == '__main__':
	#
	# ICMP Client の 設定取得
	#
	client = ICMPClient('localhost', '8888')
	print client.ping('8.8.8.8')

