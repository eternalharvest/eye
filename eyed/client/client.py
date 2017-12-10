#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

class Client:
	#
	# URL組立用のベースパスの取得
	#
	def __init__(self, host, port):
		self.base_url = 'http://%s:%s' %(host, port)

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
# Entry Point
#
if __name__ == '__main__':
	client = Client('localhost', '8888')
	print client.ping('8.8.8.8')

