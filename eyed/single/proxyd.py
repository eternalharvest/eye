#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eyed.model import ProxyPoint
from eyed.db import createSession

#
# BACnet Client
#
from eyed.client.rpc.client import BACnetRPCClient

#
# Job Scheduler
#
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING

#
# Singletone Proxyd
#
class SingleProxyd:
	_instance = None

	#
	# Initialize
	#
	def __init__(self):
		self.device_id = 0
		self.bacnetd = None
		self.cache = {}
		self.scheduler = BackgroundScheduler({
			#
			# スレッドプールの設定
			#
			'apscheduler.executors.default' : {
				'class'		: 'apscheduler.executors.pool:ThreadPoolExecutor',
				'max_workers'	: '256'
			},
			'apscheduler.job_defaults.coalesce'		: 'false',
			'apscheduler.job_defaults.max_instances'	: '128',
			'apscheduler.timezone'				: 'UTC',
		})
		#self.scheduler = BlockingScheduler()

	#
	# get instance
	#
	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	#
	# Measure
	#
	def measure(self):
		print 'OK'
		session = createSession()
		client = BACnetRPCClient('127.0.0.1')
		for p in session.query(ProxyPoint).all():
			print p

			r = client.doReadPropertyRequest(
				p.des_device_id,
				p.des_object_id,
				p.des_instance_id,
				p.des_property_id
			)

			#
			# 値のキャッシュ
			#
			self.cache[p.id] = r['value']
		session.close()
		print self.cache
		pass

	#
	# start
	#
	def start(self, interval = 10, device_id = 1234):
		#
		# 起動しているかを確認する (2重起動の停止)
		#
		if self.scheduler.state == STATE_RUNNING:
			return False

		#
		# スケジューラにメソッドを登録
		#
		self.device_id = device_id
		self.scheduler.add_job(
			self.measure,
			'interval',
			seconds=interval,
			max_instances=1
		)

		#
		# スケジューラの開始
		#
		self.scheduler.start()
		return True

#
# Entry Point
#
if __name__ == '__main__':
	SingleProxyd.getInstance().start(5)

