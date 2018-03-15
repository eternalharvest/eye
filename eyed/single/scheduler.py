#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Job Scheduler
#
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING

#
# Database 接続用
#
from eyed.model import TaskGroup
from eyed.db import createSession

#
# BACnet Driver
#
from eyed.driver.bacnet import BACnetClient

#
# Single Instances
#
from eyed.single import SingleBACnetd

#
# SingleScheduler
#
class SingleScheduler:
	_instance = None

	#
	# Initialize
	#
	def __init__(self):
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
		# スケジューラの開始
		#
		self.scheduler.start()

	#
	# get instance
	#
	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	#
	# addTaskGroup
	#
	def addTaskGroup(self, name, interval):
		#
		# 定期実行関数
		#
		def job_function(name):
			#
			# オブジェクト一覧の取得
			#
			session = createSession()
			taskGroup = session.query(TaskGroup).filter_by(name = name).first()
			if taskGroup == None: return

			#
			# BACnet コマンド操作用インスタンス取得
			#
			app = SingleBACnetd.getApplication()
			if app == None: return
			bacnet = BACnetClient(app)

			#
			# リクエストの実行
			#
			device_id	= 600
			object_id	= 0
			instance_id	= 0
			property_id	= 85
			value = bacnet.ReadPropertyRequest(device_id, object_id, instance_id, property_id)
			print name, value

		#
		# 定期実行ジョブの追加
		#
		self.scheduler.add_job(
			job_function,
			'interval',
			[name],
			name		= name,
			seconds		= interval,
			max_instances	= 1
		)

#
# Entry Point
#
if __name__ == '__main__':
	pass

