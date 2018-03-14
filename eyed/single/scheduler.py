#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Job Scheduler
#
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING

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
	# get instance
	#
	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	#
	# start
	#
	def start(self):
		#
		# スケジューラの開始
		#
		self.scheduler.start()
		return True

#
# Entry Point
#
if __name__ == '__main__':
	SingleScheduler.getInstance().start()

