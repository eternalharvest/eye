#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyping import ping

class ICMP:
	#
	# 初期化処理
	#
	def __init__(self, address):
		self.address = address

	#
	# ping
	#
	def ping(self):
		r = ping(self.address)

		#
		# コードの確認
		#
		if r.ret_code == 0:
			return {
				'result'	: True,			# 結果
				'destination'	: r.destination,	# 送り先
				'destination_ip': r.destination_ip,	# 送り先IP
				'min_rtt'	: r.min_rtt,		# 最小往復秒
				'max_rtt'	: r.max_rtt,		# 最大往復秒
				'avg_rtt'	: r.avg_rtt,		# 平均往復秒
			}
		else:
			return {
				'result'	: False,		# 結果
			}

if __name__ == '__main__':
	icmp = ICMP('8.8.8.8')
	print icmp.ping()

