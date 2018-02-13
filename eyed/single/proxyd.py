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
		#
		# RPC 接続
		#
		client = BACnetRPCClient('127.0.0.1')

		#
		# DB 接続用のセッション作成
		#
		session = createSession()
		for p in session.query(ProxyPoint).all():
			#
			# 値の読み込み実行
			#
			r = client.doReadPropertyRequest(
				p.des_device_id,
				p.des_object_id,
				p.des_instance_id,
				p.des_property_id
			)

			#
			# 値のキャッシュ
			#
			key = '%s:%s' %(p.src_object_id, p.src_instance_id)
			self.cache[key] = r['value']

		#
		# DB の セッション切断
		#
		session.close()

	#
	# start
	#
	def start(self, interval = 10):
		#
		# 起動しているかを確認する (2重起動の停止)
		#
		if self.scheduler.state == STATE_RUNNING:
			return False

		#
		# スケジューラにメソッドを登録
		#
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

