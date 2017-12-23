#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
# Entry Point
#
if __name__ == '__main__':
	pass

