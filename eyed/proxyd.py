#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Job Scheduler
#
from apscheduler.schedulers.background import BlockingScheduler
#from apscheduler.schedulers.background import BackgroundScheduler


#
# BACnet 接続用ドライバ
#
from eyed.single import SingleBACnetd
from eyed.driver.bacnet import BACnetd

#
# EYED
#
from eyed.client.rpc import BACnetRPCClient
from eyed.rpc.bacnetd import BACnetdService, start_bacnetd

#
# BACnet サービスの起動
#
single = SingleBACnetd.getInstance()
single.bacnetd = BACnetd(bacnet_address, device_id)

#
# RPC 接続の実施
#
#client = BACnetRPCClient('127.0.0.1', 1413)
#client.scan()

#
# オブジェクトリストの取得
#
#device_id = 1234
#result = client.getObjectList(device_id)

#
# 値の保存用
#
#values = {}

#def function():
#	objects = [obj for obj in result['value']]
#	for obj in objects[1:]:
#		property_id = 85
#		object_type, instance_id = obj
#		r = client.doReadPropertyRequest(1234, object_type, instance_id, property_id)

#		values['%s:%d:%d' %(object_type, instance_id, property_id)] = r['value']
#	print values

sched = BlockingScheduler()
#sched.add_job(function, 'interval', seconds=10, max_instances=10)
sched.start()

#
# デーモンの起動
#
#def start():
#	pass

#
# Entrty Point
#
#if __name__ == '__main__':
#	start()

