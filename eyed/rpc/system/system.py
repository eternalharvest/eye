#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# パッケージ管理ツール
#
from pkg_resources import get_distribution

#
# Network Interface Card の 情報を取得
#
import netifaces
from netaddr import IPNetwork

#
# System Service
#
class SystemService(object):
	#
	# VERSION の 確認
	#
	def exposed_getVersion(request):
		return get_distribution('eyed').version

	#
	# NIC の 情報を取得
	#
	def exposed_getNetworkInterfaces(request):
		#
		# NIC の 情報の取得
		#
		nics = []
		for iface_name in netifaces.interfaces():
			#
			# IPv4, IPv6 アドレスの取得
			#
			iface_data = netifaces.ifaddresses(iface_name)
			ipv4 = iface_data.get(netifaces.AF_INET)
			ipv6 = iface_data.get(netifaces.AF_INET6)

			#
			# NIC の 登録
			#
			nics.append({
				'name'	: iface_name,
				'ipv4'	: ipv4,
				'ipv6'	: ipv6
			})

		#
		# NIC 情報を返す
		#
		return nics

