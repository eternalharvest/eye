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
		#
		# 接続先ホスト
		#
		self.host = ''

		#
		# 値のキャッシュ用変数
		#
		self.cache = {}

		#
		# 監視ポイントのキャシュ用変数
		#
		self.points = []
		self.update()

		#
		# スケジューラの設定
		#
		self.scheduler = BackgroundScheduler({
			#
			# スレッドプールの設定
			#
			'apscheduler.executors.default' : {
				'class'		: 'apscheduler.executors.pool:ThreadPoolExecutor',
				'max_workers'	: '256'
			},
			'apscheduler.job_defaults.coalesce'		: 'false',
			'apscheduler.job_defaults.max_instances'	: '1',
			'apscheduler.timezone'				: 'UTC',
		})

	#
	# get instance
	#
	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	#
	# 監視ポイントの更新
	#
	def update(self):
		#
		# DB 接続用のセッション作成
		#
		session = createSession()
		self.points = [p.to_dict() for p in session.query(ProxyPoint).all()]

		#
		# DB の セッション切断
		#
		session.close()

	#
	# Measure
	#
	def measure(self):
		#
		# RPC 接続
		#
		client = BACnetRPCClient(self.host)
		for p in self.points:
			#
			# 値の読み込み実行
			#
			r = client.doReadPropertyRequest(
				p['des_device_id'],
				p['des_object_id'],
				p['des_instance_id'],
				p['des_property_id']
			)

			#
			# 値のキャッシュ
			#
			key = '%s:%s' %(p['src_object_id'], p['src_instance_id'])
			self.cache[key] = r['value']

	#
	# start
	#
	def start(self, host, interval):
		#
		# 接続先の取得
		#
		self.host = host

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

