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
				# 結果
				'result'	: True,
				'values'	: [{
					# 送り先
					'name'		: 'destination',
					'value'		: r.destination,
				}, {
					# 送り先IP
					'name'		: 'destination_ip',
					'value'		: r.destination_ip,
				}, {
					# 最小往復秒
					'name'		: 'min_rtt',
					'value'		: r.min_rtt,
				}, {
					# 最大往復秒
					'name'		: 'max_rtt',
					'value'		: r.max_rtt,
				}, {
					# 平均往復秒
					'name'		: 'avg_rtt',
					'value'		: r.avg_rtt,
				}]
			}
		else:
			return {
				# 結果
				'result'	: False,
				'values'	: []
			}

if __name__ == '__main__':
	icmp = ICMP('8.8.8.8')
	print icmp.ping()

	icmp = ICMP('8.8.8.8')
	print icmp.ping()

