#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Network Interface Card の 情報を取得
#
import netifaces
from netaddr import IPAddress

#
# BACnet 接続用ドライバ
#
from eyed.driver.bacnet import BACnetd

#
# Database 接続用
#
from eyed.model import Config
from eyed.db import createSession

#
# BACnet デーモン管理用
#
from eyed.single import SingleBACnetd

#
# Start BACnetd
#
def start_bacnetd(interface, device_id):
	#
	# BACnet Daemon が 起動しているか確認
	#
	single = SingleBACnetd.getInstance()
	if not single.bacnetd == None:
		return False

	#
	# DB から BACNET INTERFACE を取得
	#
	session = createSession()
	bacnet_interface = session.query(Config).filter_by(key = 'BACNET_INTERFACE').first()
	if interface == None:
		if bacnet_interface == None: return False
		interface = bacnet_interface.value

	#
	# NIC の 情報取得
	#
	bacnet_address = None
	try:
		#
		# NIC から IPv4 アドレスの取得
		#
		iface_data = netifaces.ifaddresses(interface)
		ipv4 = iface_data.get(netifaces.AF_INET)
		if not ipv4 == None:
			prefix = IPAddress(ipv4[0]['netmask']).netmask_bits()
			bacnet_address = '%s/%d' %(ipv4[0]['addr'], prefix)

	#
	# NIC の情報が見つからなかった場合の処理
	#
	except ValueError:
		return False

	#
	# BACnet アドレスが定義されていない場合
	#
	if bacnet_address == None:
		return False

	#
	# BACnet Daemon の 起動
	#
	single.bacnetd = BACnetd(bacnet_address, device_id)
	single.bacnetd.start()

	#
	# DBへ の 登録
	#
	if bacnet_interface == None:
		session.add(Config('BACNET_INTERFACE', interface))
	else:
		bacnet_interface.value = interface
	session.commit()
	return True

#
# BACnetdService
#
class BACnetdService(object):
	#
	# BACnetd サービスの起動
	#
	def exposed_start(self, interface, device_id):
		return start_bacnetd(interface, device_id)

	#
	# BACnetd の 状態確認
	#
	def exposed_getStatus(self):
		#
		# BACnet Daemon が 起動しているか確認
		#
		single = SingleBACnetd.getInstance()
		if single.bacnetd == None:
			return False
		return True

	#
	# BACnetd サービスの停止
	#
	def exposed_stop(self):
		#
		# 既にサービスが起動していないかを確認
		#
		if self.exposed_getStatus() == False:
			return False

		#
		# BACnetd の 停止
		#
		single = SingleBACnetd.getInstance()
		single.bacnetd.stop()
		single.bacnetd = None
		return True

