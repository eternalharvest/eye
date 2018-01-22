#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Network Interface Card の 情報を取得
#
import netifaces
from netaddr import IPNetwork

#
# System Service
#
class SystemService(object):
	def __init__(self):
		pass

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
				'interface'	: iface_name,
				'ipv4'		: ipv4,
				'ipv6'		: ipv6
			})

		#
		# NIC 情報を返す
		#
		return nics

